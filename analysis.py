#!/usr/bin/env python3
from enum import Enum

import pandas as pd
import numpy as np

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import LeaveOneOut, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

class DataSet():
    #csv edit: place target 1st
    scaler = StandardScaler()
    lda = LinearDiscriminantAnalysis()

    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.X = self.df.iloc[:,1:]
        self.y = self.df.iloc[:,0]
        self.init_calculations()

    def init_calculations(self):
        self.acc = self.evaluate(True)

    def sample(self):
        keys = self.df.keys()[1:]
        empty_dict = {key: [0.0] for key in keys}
        empty_df = pd.DataFrame(empty_dict)
        return empty_df

    def evaluate(self, acc_only = False):
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

            self.lda.fit(X_train_scaled, y_train)
            pred = self.lda.predict(X_test_scaled)[0]

            y_pred.append(pred)
            y_true.append(y_test.iloc[0])
        if acc_only is False:
            return classification_report(y_true, y_pred, target_names = ['Сепсис', 'Не сепсис'])
        else:
            return classification_report(y_true, y_pred, output_dict = True)['accuracy']


    def predict(self,tested_patient):
        X_tested = pd.DataFrame(tested_patient, index = [0])
        test_scaled = self.scaler.transform(X_tested)
        pred = self.lda.predict(test_scaled)[0]
    #   prob = analysis.predict_proba(test_scaled)[0]
        return pred #0 or 1

    def report(self):
        str = (
            'Линейный дискриминантный анализ:\n'
            + 'точность - '
            + f'{self.acc:.2%}'
            )

        return str
