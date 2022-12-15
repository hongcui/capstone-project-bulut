import shap
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

data = pd.read_csv("./data/data.csv")
data.drop(['Reference1', 'Dataset1', 'Reference2', 'Dataset2'], axis=1, inplace=True)
data = data.sample(frac=1).reset_index(drop=True)
y = data.Same.copy()
features = data.drop(['Same'], axis=1)

features_train, features_test, y_train, y_test = train_test_split(features, y, test_size=0.20, random_state=31)
model = XGBClassifier()
model.fit(features_train, y_train)

explainer = shap.Explainer(model)
shap_test = explainer(features_test)
shap.summary_plot(shap_test, features_test, feature_names=features_test.columns, show=False)
plt.show()
plt.savefig('./figures/shap.png')
