import xgboost as xgb
import pandas as pd
import pickle

print("Loading model and encoders...")
# 1. Load models and encoders
model = xgb.XGBClassifier()
model.load_model('xgboost_delivery_model.json')

with open('label_encoders.pkl', 'rb') as f:
    label_encoders = pickle.load(f)

# 2. Define Sample Input
sample_data = {
    'Warehouse_block': ['A', 'F'],
    'Mode_of_Shipment': ['Flight', 'Ship'],
    'Product_importance': ['high', 'low'],
    'Weight_in_gms': [1500, 4500],
    'Cost_of_the_Product': [250, 150],
    'Discount_offered': [10, 2]
}

df_sample = pd.DataFrame(sample_data)
print("\n--- Testing with sample data ---")
print(df_sample.to_string(index=False))

# 3. Preprocess the raw input
for col in ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance']:
    df_sample[col] = label_encoders[col].transform(df_sample[col])

# 4. Predict
predictions = model.predict(df_sample)
probabilities = model.predict_proba(df_sample)[:, 1]

print("\n--- Prediction Results ---")
for i, pred in enumerate(predictions):
    status = "Delayed ⚠️" if pred == 1 else "On Time ✅"
    print(f"Sample {i+1}: {status} (Delay Probability: {probabilities[i]:.2%})")
