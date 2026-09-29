#!/usr/bin/env python3
from enum import Enum

import pandas as pd
import numpy as np

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.model_selection import LeaveOneOut, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report


#csv edit: place target 1st
df = pd.read_csv("data.csv")
X = df.iloc[:,1:]
y = df.iloc[:,0]

scaler = StandardScaler()



def Sample():
    keys = df.keys()[1:]
    empty_dict = {key: [0.0] for key in keys}
    empty_df = pd.DataFrame(empty_dict)
    return empty_df

def Evaluate(analysis, AccOnly = False):
    y_true = []
    y_pred = []
    
    #if df.shape[0] <= 60:
    #	
    split_method = LeaveOneOut()
    #else:
    #	split_method = KFold()
	
    for train_idx, test_idx in split_method.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        
        #scaler only trains on train!
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        #print('X_test: ', X_test, '\nX_test_scaled: ', X_test_scaled)
        
        analysis.fit(X_train_scaled, y_train)
        #predicting our test unit
        pred = analysis.predict(X_test_scaled)[0]
        
        y_pred.append(pred)
        y_true.append(y_test.iloc[0])
    if AccOnly is False: 
	    return classification_report(y_true, y_pred, target_names = ['Сепсис', 'Не сепсис'])
    else:
	    return classification_report(y_true, y_pred, output_dict = True)['accuracy']


def Predict(tested_patient, analysis):
    X_tested = pd.DatiaFrame(tested_patient, index = [0])
    X_train_scaled = scaler.fit_transform(X)
    test_scaled = scaler.transform(X_tested)
    pred = analysis.predict(test_scaled)[0]
#    prob = a.predict_proba(test_scaled)[0]
    return pred

def MostAccurateMethod():
    lAccuracy = Evaluate(LinearDiscriminantAnalysis(), True)
    qAccuracy = Evaluate(QuadraticDiscriminantAnalysis(), True)

    if qAccuracy<lAccuracy:
        return LinearDiscriminantAnalysis()
    else:
        return QuadraticDiscriminantAnalysis()

def PredictUsingBest(tested_patient):
    return Predict(tested_patient, MostAccurateMethod())

def FullReport():
    str = (
        'Линейный дискриминантный:\n' 
        + Evaluate(analysis=LinearDiscriminantAnalysis())
        + '\nКвадратичный дискриминантный:\n'
        + Evaluate(analysis=QuadraticDiscriminantAnalysis())
        )

    return str

print(FullReport())
#print(Evaluate(MostAccurateMethod()))
