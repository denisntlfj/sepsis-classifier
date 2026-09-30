#!/usr/bin/env python3
from enum import Enum

import pandas as pd
import numpy as np

from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.model_selection import LeaveOneOut, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

class DataSet():
    #csv edit: place target 1st
    scaler = StandardScaler() #read about this one

    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.X = df.iloc[:,1:]
        self.y = df.iloc[:,0]

    def sample(self):
        keys = self.df.keys()[1:]
        empty_dict = {key: [0.0] for key in keys}
        empty_df = pd.DataFrame(empty_dict)
        return empty_df

    def evaluate(self,analysis, AccOnly = False):
        y_true = []
        y_pred = []

        #if df.shape[0] <= 60:
        #
        split_method = LeaveOneOut()
        #else:
        #	split_method = KFold()

        for train_idx, test_idx in split_method.split(self.X):
            X_train, X_test = self.X.iloc[train_idx], self.X.iloc[test_idx]
            y_train, y_test = self.y.iloc[train_idx], self.y.iloc[test_idx]


            #scaler only trains on train!
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

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


    def predict(self,tested_patient, analysis):
        X_tested = pd.DatiaFrame(tested_patient, index = [0])
        X_train_scaled = self.scaler.fit_transform(X)
        test_scaled = scaler.transform(X_tested)
        pred = analysis.predict(test_scaled)[0]
    #    prob = a.predict_proba(test_scaled)[0]
        return pred

    def most_accurate_method(self):
        lAccuracy = self.evaluate(LinearDiscriminantAnalysis(), True)
        qAccuracy = self.evaluate(QuadraticDiscriminantAnalysis(), True)

        if qAccuracy<lAccuracy:
            return LinearDiscriminantAnalysis()
        else:
            return QuadraticDiscriminantAnalysis()

    def predict_using_best(tested_patient):
        return Predict(tested_patient, MostAccurateMethod())

    def report(self):
        str = (
            'Линейный дискриминантный:\n'
            + 'точность - '
            + f'{self.evaluate(LinearDiscriminantAnalysis(), True):.2%}'
            + '\n\nКвадратичный дискриминантный:\n'
            + 'точность - '
            + f'{self.evaluate(QuadraticDiscriminantAnalysis(), True):.2%}'
            )

        return str
