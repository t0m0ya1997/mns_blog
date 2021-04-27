#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 23:05:36 2021

@author: t_hirakawa
"""

#%% import libs

import numpy as np
import multiprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.neural_network import MLPClassifier
cores = multiprocessing.cpu_count()

# make classification problem
X, y = make_classification(n_samples = 500, n_features = 64, n_informative = 16, n_classes = 2, random_state = 2021)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2021, stratify = y)

# definition of models
models = {
    ("RandomForest", RandomForestClassifier()),
    ("GradientBoosting", GradientBoostingClassifier()),
    ("NeuralNetwork", MLPClassifier(max_iter = 10000)),
    ("AdaBoost", AdaBoostClassifier())
    }

# validation score of each single model
for name, model in models:
    acc = accuracy_score(y_test, model.fit(X_train, y_train).predict(X_test))
    print("Accuracy of", name, ":", acc)

print("------------------------------------")

# construct stacking model
stacking = StackingClassifier(estimators = models, final_estimator = MLPClassifier(), n_jobs = cores)

# validation of Stacking model
acc = accuracy_score(y_test, stacking.fit(X_train, y_train).predict(X_test))
print("Accuracy of Stacking :", acc)