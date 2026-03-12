import csv
import math

# Load dataset
data = []
with open('iris_nb.csv') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        row[:-1] = [float(x) for x in row[:-1]]
        data.append(row)

# Separate by class
classes = {}
for row in data:
    label = row[-1]
    if label not in classes:
        classes[label] = []
    classes[label].append(row[:-1])

# Mean calculation
def mean(numbers):
    return sum(numbers) / len(numbers)

# Standard deviation
def stddev(numbers):
    avg = mean(numbers)
    variance = sum([(x-avg)**2 for x in numbers]) / len(numbers)
    return math.sqrt(variance)

# Summarize dataset
summary = {}
for label, rows in classes.items():
    summary[label] = [(mean(col), stddev(col)) for col in zip(*rows)]

# Gaussian probability
def probability(x, mean, std):
    exponent = math.exp(-(x-mean)**2 / (2*std**2))
    return (1/(math.sqrt(2*math.pi)*std)) * exponent

# Prediction
def predict(row):
    probs = {}
    for label, class_summary in summary.items():
        probs[label] = 1
        for i in range(len(class_summary)):
            mean, std = class_summary[i]
            probs[label] *= probability(row[i], mean, std)
    return max(probs, key=probs.get)

# Testing
test = [5.9,3.0,5.1,1.8]

result = predict(test)

print("Test Data:", test)
print("Predicted Class:", result)
