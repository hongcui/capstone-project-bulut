from sklearn.model_selection import LeaveOneOut
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics


data = pd.read_csv("./data/data.csv")
data.drop(['Reference1', 'Dataset1', 'Reference2', 'Dataset2'], axis=1, inplace=True)
data = data.sample(frac=1).reset_index(drop=True)
y = data.Same.copy().to_numpy()
features = data.drop(['Same'], axis=1).to_numpy()

loo = LeaveOneOut()
predictions = np.array([])
for train_index, test_index in loo.split(features):
    features_train, features_test = features[train_index], features[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model = LogisticRegression()
    model.fit(features_train, y_train)
    y_pred = model.predict(features_test)
    print(y_pred)
    if not predictions.any(): # problem here 
        predictions = y_pred
        print("first iteration")
    else:
        predictions = np.hstack((predictions,y_pred))




print("Accuracy:", metrics.accuracy_score(y, predictions))
print("Precision:", metrics.precision_score(y, predictions))
print("Recall:", metrics.recall_score(y, predictions))
print("F1:", metrics.f1_score(y, predictions))
