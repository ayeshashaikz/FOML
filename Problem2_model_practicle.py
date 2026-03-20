from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Encode data
le = LabelEncoder()
data['Income'] = le.fit_transform(data['Income'])
data['CreditHistory'] = le.fit_transform(data['CreditHistory'])

X = data[['Income', 'CreditHistory']]
y = data['Default']

model = LogisticRegression()
model.fit(X, y)

# Prediction probabilities
probs = model.predict_proba(X)
print("Probabilities:\n", probs)