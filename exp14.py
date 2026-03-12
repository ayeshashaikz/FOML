import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("house_price.csv")

# Features
X = data[['Area','Bedrooms','Bathrooms','Age']]
…predictions = model.predict(X_test)

print("Predicted House Prices:")
print(predictions)

# Model score
score = model.score(X_test,y_test)
print("Model Accuracy:", score)
