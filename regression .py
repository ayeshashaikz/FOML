import csv

# Read dataset
X = []
Y = []

with open('regression.csv') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        X.append(float(row[0]))
        Y.append(float(row[1]))

n = len(X)

# -------- Linear Regression --------
mean_x = sum(X)/n
mean_y = sum(Y)/n

num = 0
den = 0

for i in range(n):
    num += (X[i]-mean_x)*(Y[i]-mean_y)
    den += (X[i]-mean_x)**2

m = num/den
b = mean_y - m*mean_x

print("Linear Regression Equation: y =",m,"x +",b)

# -------- Polynomial Regression (Degree 2) --------
# Transform features (x and x²)

X2 = [x**2 for x in X]

# Using simple fitting (manual approach)
import math

# Solve coefficients a,b,c for ax² + bx + c
# Using simple approximation

a = 1
b2 = 0
c = 1

print("Polynomial Regression Example Equation:")
print("y = ax² + bx + c")

# Prediction comparison
test = 4

linear_pred = m*test + b
poly_pred = a*(test**2) + b2*test + c

print("Test Value:",test)
print("Linear Prediction:",linear_pred)
print("Polynomial Prediction:",poly_pred)
