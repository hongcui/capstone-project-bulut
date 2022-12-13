from xgboost import XGBClassifier
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

def split_data(df, ratio):
    df = df.sample(frac=1).reset_index(drop=True)
    y = df.cancer.copy()
    features = df.drop(['cancer'], axis=1)
    return train_test_split(features, 
                            y,
                            test_size=ratio,
                            random_state=31)

def encode_dataset(df):
    le = LabelEncoder()
    for colname in df.columns:
        df[colname] = le.fit_transform(df[colname])
    return df

def train(model, f_train, y_train):
    model.fit(f_train, y_train)
    return model

def evaluate(model, model_name, results, f_test, y_test, train_domain, test_domain):
    y_pred = pd.Series(model.predict(f_test))
    y_test = y_test.reset_index(drop=True)
    results['model'].append(model_name) 
    results['trained_on'].append(train_domain)
    results['tested_on'].append(test_domain)
    results['accuracy'].append(metrics.accuracy_score(y_test, y_pred))
    results['precision'].append(metrics.precision_score(y_test, y_pred))
    results['recall'].append(metrics.recall_score(y_test, y_pred))
    results['f1'].append(metrics.f1_score(y_test, y_pred))
    return results

def write_results_to_csv(results):
    results_df = pd.DataFrame(results)
    results_df.to_csv('./results/results.csv', index=False)