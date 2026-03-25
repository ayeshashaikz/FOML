from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from route_optimizer import optimize_route
import xgboost as xgb
import pandas as pd
import pickle
import os
import csv
import secrets
import pickle

app = FastAPI(
    title="Delivery Delay Prediction API",
    description="API for predicting logistics delivery delays using XGBoost.",
    version="1.0.0"
)

# Enable CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# DATABASE SETUP (CSV)
# -----------------
USERS_DB_FILE = "users.csv"

def init_db():
    if not os.path.exists(USERS_DB_FILE):
        with open(USERS_DB_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])

init_db()

# -----------------
# AUTH ENDPOINTS
# -----------------
class UserAuth(BaseModel):
    username: str
    password: str

@app.post("/register")
def register_user(user: UserAuth):
    # Check if user exists
    with open(USERS_DB_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'].lower() == user.username.lower():
                raise HTTPException(status_code=400, detail="Username already exists")
    
    # Save new user
    with open(USERS_DB_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user.username, user.password])
        
    return {"message": "User registered successfully!"}

@app.post("/login")
def login_user(user: UserAuth):
    with open(USERS_DB_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == user.username and row['password'] == user.password:
                # Generate a simple fake session token
                token = secrets.token_hex(16)
                return {
                    "message": "Login successful", 
                    "token": token,
                    "username": user.username
                }
                
    raise HTTPException(status_code=401, detail="Invalid username or password")

# -----------------
# ML & ROUTING (Reloading Model)
# -----------------
print("Starting API and Loading Model...")
# Load model and encoders into memory
model = xgb.XGBClassifier()
model.load_model('xgboost_delivery_model.json')

with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

# Define request schema
class DeliveryRequest(BaseModel):
    Warehouse_block: str
    Mode_of_Shipment: str
    Product_importance: str
    Weight_in_gms: int
    Cost_of_the_Product: float

@app.post("/predict")
def predict_delay(request: DeliveryRequest):
    try:
        data = request.dict()
        df = pd.DataFrame([data])
        
        # Encode categorical variables
        for col in ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance']:
            # Validate input before encoding
            if data[col] not in label_encoders[col].classes_:
                raise HTTPException(status_code=400, detail=f"Invalid value for {col}. Must be one of {list(label_encoders[col].classes_)}")
            df[col] = label_encoders[col].transform(df[col])
            
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]
        
        status = "Delayed" if prediction == 1 else "On Time"
        
        return {
            "prediction": int(prediction),
            "status": status,
            "delay_probability": float(probability)
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class RouteOptimizationRequest(BaseModel):
    Warehouse_block: str
    packages: List[DeliveryRequest]

@app.post("/optimize-route")
def api_optimize_route(request: RouteOptimizationRequest):
    try:
        enriched_packages = []
        # First pass: Predict delays for every package in the batch!
        for i, pkg in enumerate(request.packages):
            pkg_dict = pkg.dict()
            df = pd.DataFrame([pkg_dict])
            
            for col in ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance']:
                if pkg_dict[col] not in label_encoders[col].classes_:
                    raise HTTPException(status_code=400, detail=f"Invalid value for {col}")
                df[col] = label_encoders[col].transform(df[col])
                
            # XGBoost Predict
            prediction = model.predict(df)[0]
            probability = float(model.predict_proba(df)[0][1])
            
            enriched_packages.append({
                "package_index": i,
                "data": pkg_dict,
                "delay_probability": probability,
                "delayed_warning": bool(prediction == 1)
            })

        # Second Pass: Send to OR-Tools for Distance Minimization and ML-Driven Priority Mapping
        route_result = optimize_route(request.Warehouse_block, enriched_packages)
        
        if not route_result:
            raise HTTPException(status_code=500, detail="Could not find optimal route")
            
        # Format the ultimate sequence response
        ordered_packages = []
        for routing_order, original_idx in enumerate(route_result["ordered_indices"]):
            pkg = enriched_packages[original_idx]
            # Attach map coordinate
            pkg["map_location"] = route_result["locations"][original_idx]
            pkg["routing_sequence_number"] = routing_order + 1
            ordered_packages.append(pkg)
            
        return {
            "warehouse_origin": request.Warehouse_block,
            "depot_map_location": route_result["depot_location"],
            "total_route_distance_km": route_result["total_distance_km"],
            "optimal_route": ordered_packages
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "API is up and running!"}

if __name__ == "__main__":
    import uvicorn
    # Make sure to run the API using: python api.py OR uvicorn api:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
