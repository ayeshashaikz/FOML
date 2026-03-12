import math
from collections import Counter

# Play Tennis Dataset
data = [
    ['Sunny','Hot','High','Weak','No'],
    ['Sunny','Hot','High','Strong','No'],
    ['Overcast','Hot','High','Weak','Yes'],
    ['Rain','Mild','High','Weak','Yes'],
    ['Rain','Cool','Normal','Weak','Yes'],
    ['Rain','Cool','Normal','Strong','No'],
    ['Overcast','Cool','Normal','Strong','Yes'],
    ['Sunny','Mild','High','Weak','No'],
    ['Sunny','Cool','Normal','Weak','Yes'],
    ['Rain','Mild','Normal','Weak','Yes'],
    ['Sunny','Mild','Normal','Strong','Yes'],
    ['Overcast','Mild','High','Strong','Yes'],
    ['Overcast','Hot','Normal','Weak','Yes'],
    ['Rain','Mild','High','Strong','No']
]

attributes = ['Outlook','Temperature','Humidity','Wind']


# Entropy Calculation
def entropy(data):
    labels = [row[-1] for row in data]
    total = len(labels)
    count = Counter(labels)
    ent = 0
    for c in count.values():
        p = c/total
        ent -= p * math.log2(p)
    return ent


# Information Gain
def information_gain(data, index):
    total_entropy = entropy(data)
    values = set([row[index] for row in data])
    weighted_entropy = 0

    for v in values:
        subset = [row for row in data if row[index] == v]
        weighted_entropy += (len(subset)/len(data)) * entropy(subset)

    return total_entropy - weighted_entropy


# ID3 Algorithm
def id3(data, attributes):
    labels = [row[-1] for row in data]

    # If all labels same
    if labels.count(labels[0]) == len(labels):
        return labels[0]

    # If no attributes left
    if not attributes:
        return Counter(labels).most_common(1)[0][0]

    gains = [information_gain(data, i) for i in range(len(attributes))]
    best_index = gains.index(max(gains))
    best_attr = attributes[best_index]

    tree = {best_attr: {}}

    values = set([row[best_index] for row in data])

    for v in values:
        subset = [row[:best_index] + row[best_index+1:]
                  for row in data if row[best_index] == v]

        new_attrs = attributes[:best_index] + attributes[best_index+1:]
        tree[best_attr][v] = id3(subset, new_attrs)

    return tree


# Build Tree
decision_tree = id3(data, attributes)

print("Decision Tree:")
print(decision_tree)
