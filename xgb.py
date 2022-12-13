import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

data = pd.read_csv("./data/data.csv")
data.drop(['Reference1', 'Dataset1', 'Reference2', 'Dataset2'], axis=1, inplace=True)
data = data.sample(frac=1).reset_index(drop=True)
y = data.Same.copy()
features = data.drop(['Same'], axis=1)

features_train, features_test, y_train, y_test = train_test_split(features, y, test_size=0.20, random_state=31)
model = XGBClassifier()
model.fit(features_train, y_train)
y_pred = pd.Series(model.predict(features_test))
y_test = y_test.reset_index(drop=True)


print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))
print("F1:", metrics.f1_score(y_test, y_pred))

model.save_model("./saved-models/xgb_model.json")
# future work for capstone only
# write the code for taking new input and getting similar samples
# decision trees, random forest, nn
# leave one out, k-fold, without cv
