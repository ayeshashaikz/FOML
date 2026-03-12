import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load dataset
data = pd.read_csv("car_price.csv")

# Features and target
X = data[['Year','Present_Price','Kms_Driven','Owner']]
y = data['Selling_Price']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train,y_train)

# Prediction
predictions = model.predict(X_test)

print("Predicted Prices:", predictions)

# Error
error = mean_absolute_error(y_test,predictions)
print("Mean Absolute Error:", error)
