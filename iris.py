import csv
import math
from collections import Counter

data = []

# Read dataset
with open('iris.csv') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        features = list(map(float,row[:4]))
        label = row[4]
        data.append(features + [label])


# Distance
def distance(p1,p2):

    sum_val = 0

    for i in range(4):
        sum_val += (p1[i]-p2[i])**2

    return math.sqrt(sum_val)


# KNN
def knn(data,test,k):

    distances = []

    for row in data:
        d = distance(row,test)
        distances.append((d,row[4]))

    distances.sort()

    neighbors = distances[:k]

    labels = [n[1] for n in neighbors]

    return Counter(labels).most_common(1)[0][0]


# Test flower
test_flower = [5.0,3.6,1.3,0.2]

prediction = knn(data,test_flower,3)

print("Test Flower:",test_flower)
print("Predicted Class:",prediction)
