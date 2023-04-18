from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
import numpy as np
import preprocess

def transform_data(data):
    data = preprocess.date_to_month_in_quarter(data, 3)
    data = preprocess.title_to_sentiment(data, 4)
    data = preprocess.title_to_sentiment(data, 0)
    return data


def train_model(X_train, y_train):
    model = LinearSVC(class_weight='balanced') 
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    yhat = model.predict(X_test) 

    accuracy = model.score(X_test, y_test) 
    
    precision = precision_score(y_test, yhat)
    recall = recall_score(y_test, yhat)
    f1 = f1_score(y_test, yhat)
    specificity = recall_score(y_test, yhat, pos_label=0)
    auc = roc_auc_score(y_test, yhat)

    # Store metrics in tuple and return
    metrics = (accuracy, precision, recall, specificity, f1, auc)
    return metrics
    
def mike_m1():
    headers, data, y = preprocess.main(1)
    data = transform_data(data)
    X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=.1, shuffle=True)
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)
    print(y_test.shape)
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    print(metrics)

mike_m1()