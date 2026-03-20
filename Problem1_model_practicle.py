import pandas as pd

# Dataset
data = pd.DataFrame({
    'Income': ['High', 'Medium', 'Low', 'Medium'],
    'CreditHistory': ['Good', 'Good', 'Bad', 'Bad'],
    'Default': [0, 0, 1, 1]
})

# Prior probabilities
P_default_1 = len(data[data['Default'] == 1]) / len(data)
P_default_0 = len(data[data['Default'] == 0]) / len(data)

# Likelihoods
def likelihood(feature, value, target):
    subset = data[data['Default'] == target]
    return len(subset[subset[feature] == value]) / len(subset)

# Example prediction: Income=Medium, CreditHistory=Good
p1 = P_default_1 * likelihood('Income', 'Medium', 1) * likelihood('CreditHistory', 'Good', 1)
p0 = P_default_0 * likelihood('Income', 'Medium', 0) * likelihood('CreditHistory', 'Good', 0)

print("P(Default=1):", p1)
print("P(Default=0):", p0)

if p1 > p0:
    print("Prediction: Default")
else:
    print("Prediction: No Default")