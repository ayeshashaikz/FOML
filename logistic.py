import csv
import math

X = []
y = []

# Read dataset
with open('LR.csv','r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        X.append(float(row[0]))
        y.append(int(row[1]))

w = 0
b = 0
learning_rate = 0.01
epochs = 1000

def sigmoid(z):
    return 1/(1+math.exp(-z))

# Training
for _ in range(epochs):
    dw = 0
    db = 0

    for i in range(len(X)):
        z = w*X[i] + b
        y_pred = sigmoid(z)

        dw += (y_pred - y[i]) * X[i]
        db += (y_pred - y[i])

    dw /= len(X)
    db /= len(X)

    w -= learning_rate * dw
    b -= learning_rate * db

def predict(x):
    z = w*x + b
    p = sigmoid(z)

    if p >= 0.5:
        return 1
    else:
        return 0

test_hours = 3

result = predict(test_hours)

print("Study Hours:", test_hours)
print("Prediction (0=Fail,1=Pass):", result)
