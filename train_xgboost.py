import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import pickle
import warnings
warnings.filterwarnings('ignore')

# 1. Load the new dataset
print("Loading data...")
df = pd.read_csv('delivery_optimization_data.csv')

# 2. Preprocessing: Encode Categorical Features
categorical_cols = ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance']
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Save the label encoders for future predictions (e.g. backend API)
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

# 3. Split Features (X) and Target (y)
# Ensure we drop Discount_offered so the model doesn't train on it
X = df.drop(['Reached.on.Time_Y.N', 'Discount_offered'], axis=1, errors='ignore')
y = df['Reached.on.Time_Y.N']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Train the XGBoost Model
print("Training XGBoost Classifier...")
model = xgb.XGBClassifier(
    n_estimators=100, 
    learning_rate=0.1, 
    max_depth=5, 
    random_state=42, 
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# 5. Evaluate the Model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model Training Complete!")
print("-" * 30)
print(f"Accuracy: {accuracy * 100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 6. Save the Model
model_filename = 'xgboost_delivery_model.json'
model.save_model(model_filename)
print("-" * 30)
print(f"Model successfully saved to '{model_filename}'")
print("Label encoders saved to 'label_encoders.pkl'")
