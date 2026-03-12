import csv
import math
from collections import Counter

# Read dataset
data = []
with open('knn.csv') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x = float(row[0])
        y = float(row[1])
        label = row[2]
        data.append([x, y, label])


# Euclidean distance
def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


# KNN function
def knn(data, test_point, k):
    distances = []

    for row in data:
        d = distance(row, test_point)
        distances.append((d, row[2]))

    distances.sort()

    neighbors = distances[:k]

    classes = [n[1] for n in neighbors]

    prediction = Counter(classes).most_common(1)[0][0]

    return prediction


# Test sample
test = [5,7]

k = 3

result = knn(data, test, k)

print("Test Point:", test)
print("Predicted Class:", result)
