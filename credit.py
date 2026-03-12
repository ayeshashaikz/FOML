import csv
import math
from collections import defaultdict

data = []

# Read CSV file (TAB separated)
with open("credit.csv") as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)   # skip header
    for row in reader:
        income = int(row[0])
        debt = int(row[1])
        label = row[2]
        data.append([income, debt, label])

# Separate features and labels
X = [row[:2] for row in data]
y = [row[2] for row in data]

model = defaultdict(list)

for features, label in zip(X, y):
    model[label].append(features)

# Mean function
def mean(nums):
    return sum(nums) / len(nums)

# Variance function
def variance(nums):
    m = mean(nums)
    return sum((x-m)**2 for x in nums) / len(nums)

# Gaussian probability
def gaussian(x, m, v):
    return (1 / math.sqrt(2*math.pi*v)) * math.exp(-(x-m)**2/(2*v))

# Train statistics
stats = {}
for label, rows in model.items():
    incomes = [r[0] for r in rows]
    debts = [r[1] for r in rows]

    stats[label] = (
        mean(incomes), variance(incomes),
        mean(debts), variance(debts)
    )

# Prediction
def predict(income, debt):
    probs = {}

    for label, s in stats.items():
        p1 = gaussian(income, s[0], s[1])
        p2 = gaussian(debt, s[2], s[3])
        probs[label] = p1 * p2

    return max(probs, key=probs.get)

print("Predicted Credit Score:", predict(42,9))
