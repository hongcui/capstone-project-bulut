from sklearn.model_selection import LeaveOneOut
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
import time


data = pd.read_csv("./data/data.csv")
data.drop(['Reference1', 'Dataset1', 'Reference2', 'Dataset2'], axis=1, inplace=True)
data = data.sample(frac=1).reset_index(drop=True)
y = data.Same.copy().to_numpy()
features = data.drop(['Same'], axis=1).to_numpy()

start = time.time()
loo = LeaveOneOut()
predictions = np.array([])
for train_index, test_index in loo.split(features):
    features_train, features_test = features[train_index], features[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model = LogisticRegression()
    model.fit(features_train, y_train)
    y_pred = model.predict(features_test)
    if predictions.size: # problem here 
        predictions = np.hstack((predictions,y_pred))
    else:
        predictions = y_pred
        print("first iteration")
end = time.time()
print(end - start)

print("results for logistic regression")
print("Accuracy:", metrics.accuracy_score(y, predictions))
print("Precision:", metrics.precision_score(y, predictions))
print("Recall:", metrics.recall_score(y, predictions))
print("F1:", metrics.f1_score(y, predictions))

start = time.time()
loo = LeaveOneOut()
predictions = np.array([])
ctr = 1
for train_index, test_index in loo.split(features):
    print(ctr)
    ctr += 1
    features_train, features_test = features[train_index], features[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model = MLPClassifier(hidden_layer_sizes=(150,100,50),
                        max_iter = 300,activation = 'relu',
                        solver = 'adam')
    model.fit(features_train, y_train)
    y_pred = model.predict(features_test)
    if predictions.size: # problem here 
        predictions = np.hstack((predictions,y_pred))
    else:
        predictions = y_pred
        print("first iteration")


end = time.time()
print(end - start)
print("results for neural networks")
print("Accuracy:", metrics.accuracy_score(y, predictions))
print("Precision:", metrics.precision_score(y, predictions))
print("Recall:", metrics.recall_score(y, predictions))
print("F1:", metrics.f1_score(y, predictions))


start = time.time()
loo = LeaveOneOut()
predictions = np.array([])
ctr = 1
for train_index, test_index in loo.split(features):
    print(ctr)
    ctr += 1
    features_train, features_test = features[train_index], features[test_index]
    y_train, y_test = y[train_index], y[test_index]
    model = XGBClassifier()
    model.fit(features_train, y_train)
    y_pred = model.predict(features_test)
    if predictions.size: # problem here 
        predictions = np.hstack((predictions,y_pred))
    else:
        predictions = y_pred
        print("first iteration")
        


end = time.time()
print(end - start)
print("results for xgboost")
print("Accuracy:", metrics.accuracy_score(y, predictions))
print("Precision:", metrics.precision_score(y, predictions))
print("Recall:", metrics.recall_score(y, predictions))
print("F1:", metrics.f1_score(y, predictions))
