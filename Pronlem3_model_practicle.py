from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

model = DecisionTreeClassifier()
model.fit(X, y)

plt.figure(figsize=(6,4))
plot_tree(model, feature_names=X.columns, class_names=['No Default', 'Default'], filled=True)
plt.show()