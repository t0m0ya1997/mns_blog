#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 02:19:16 2021

@author: t_hirakawa
"""

#%% import libs 
import optuna
import numpy as np
import multiprocessing
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import cross_val_score, train_test_split
from matplotlib import pyplot as plt
cores = multiprocessing.cpu_count()
#%%
#%% Lasso experiment

X, y, coef = make_regression(n_samples = 500, n_features = 64, n_informative = 32, noise = 0.1, coef = True)
# plt.stem(np.where(coef)[0], coef[coef != 0], markerfmt = "x", use_line_collection=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2021)

# lasso w/o tuning
ans0  = Lasso().fit(X_train, y_train).predict(X_test)
mse0 = mean_squared_error(y_test, ans0)

# tuning of lasso
def tuningOfLasso(X, y):
    def objective(trial):
        alpha = trial.suggest_loguniform("alpha", 0.001, 10.0)
        reg = Lasso(alpha = alpha,
                        random_state = 2021,
                        max_iter = 1000)
    
        return cross_val_score(reg, X, y, n_jobs=cores, cv=5, scoring = "neg_mean_squared_error").mean()
    return objective

study = optuna.create_study(direction='maximize')
study.optimize(tuningOfLasso(X_train, y_train), n_trials=200)

trial = study.best_trial

print('Accuracy: {}'.format(trial.value))
print("Best hyperparameters: {}".format(trial.params))

"""
Accuracy: -0.00016161236996687297
Best hyperparameters: {'alpha': 0.001225057064820786}
"""

# lasso w/ tuning
ans1 = Lasso(random_state = 2021, **trial.params).fit(X_train, y_train).predict(X_test)
mse1 = mean_squared_error(y_test, ans1)

print("mean squared error(MSE)")
print("lasso(default): ", mse0)
print("lasso(tuned): ", mse1)

#%%
#%% RandomForest experiment
X, y = make_classification(n_samples = 500, n_features = 64, n_informative = 32, n_classes = 4, random_state = 2021)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2021, stratify = y)
ans0 = RandomForestClassifier().fit(X_train, y_train).predict(X_test)
acc0 = accuracy_score(y_test, ans0)
#%%
# tuning of Random Forest
def tuningOfRF(X, y):

    def objective(trial):
        n_estimators = trial.suggest_int("n_estimators", 10, 200)
        criterion = trial.suggest_categorical("criterion", ["gini", "entropy"])
        random_state = trial.suggest_int("random_state", 2021, 2021)

        clf = RandomForestClassifier(random_state = random_state,
                                     n_estimators = n_estimators,
                                     criterion = criterion,
                                     n_jobs = cores//2)
    
        
        #ランダムフォレストモデルを交差検証してその平均スコアを返す
        return cross_val_score(clf, X, y, n_jobs=cores//2, cv=4, scoring = "accuracy").mean()
    return objective

#Optunaオブジェクトの作成 directionをmaximizeとすることで最大化
study = optuna.create_study(direction='maximize')
#100回の試行で最適化をおこなう。
study.optimize(tuningOfRF(X_train, y_train), n_trials = 200)

#trialにベストのトライアル結果を入れる。
trial = study.best_trial

#ベストな結果、パラメータの表示
print('Accuracy: {}'.format(trial.value))
print("Best hyperparameters: {}".format(trial.params))

ans1 = RandomForestClassifier(**trial.params).fit(X_train, y_train).predict(X_test)
acc1 = accuracy_score(y_test, ans1)

print("Accuracy")
print("RandomForest(default): ", acc0)
print("RandomForest(tuned): ", acc1)