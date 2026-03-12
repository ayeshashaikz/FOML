import csv
from collections import Counter

# Read dataset
data = []
with open('nb.csv','r') as file:
    reader = csv.reader(file)
    headers = next(reader)

    for row in reader:
        data.append(row)

# Split features and labels
X = [row[:-1] for row in data]
y = [row[-1] for row in data]

# Train Naive Bayes
def train_nb(X, y):
    model = {}
    class_counts = Counter(y)
    total = len(y)

    for c in class_counts:
        model[c] = {}

    for i in range(len(X[0])):
        values = set([x[i] for x in X])

        for c in class_counts:
            model[c][i] = {}

            for v in values:
                count = sum(1 for j in range(len(X)) if X[j][i] == v and y[j] == c)
                model[c][i][v] = (count + 1) / (class_counts[c] + len(values))

    priors = {c: class_counts[c]/total for c in class_counts}

    return model, priors


# Predict function
def predict(model, priors, sample):
    probs = {}

    for c in model:
        prob = priors[c]

        for i, val in enumerate(sample):
            prob *= model[c][i].get(val, 1e-6)

        probs[c] = prob

    return max(probs, key=probs.get)


# Train model
model, priors = train_nb(X, y)

# Predict dataset
predictions = []
for sample in X:
    predictions.append(predict(model, priors, sample))

# Confusion Matrix
TP = TN = FP = FN = 0

for actual, pred in zip(y, predictions):

    if actual == "Yes" and pred == "Yes":
        TP += 1

    elif actual == "No" and pred == "No":
        TN += 1

    elif actual == "No" and pred == "Yes":
        FP += 1

    elif actual == "Yes" and pred == "No":
        FN += 1

print("Confusion Matrix")
print("TP:", TP, "FP:", FP)
print("FN:", FN, "TN:", TN)

# Accuracy
accuracy = (TP + TN) / len(y)

print("Accuracy:", accuracy)
