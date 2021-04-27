---
title: "Optuna を使ってみた話"
description: "某機械学習コンペに参加した際に知った、ハイパラ最適化ツール「Optuna」を使ってみたという記事です。"
date: 2021-02-24T14:32:00+09:00
tags: ["ハイパラ調整", "Optuna", "Python", "scikit-learn"]
categories: ["機械学習"]
draft: false
---

# はじめに
先日、某社の短期インターンシップという名の、数週間にわたる機械学習コンペに参加しておりました。
コンペ初心者だった僕は、ハイパラ調整をGridSearchで行なっていましたが、「Optuna使ってみぃな」と言われました。
いざ実際に使ってみるとすごく便利だったので備忘録もかねて書き残しておきます。

# インストール・環境
インストールは、きちんと環境を管理できているのであれば
```
pip install optuna
```
というようにpipで一発です。
Python 環境の管理が面倒だよ、、、という方には[anyenv](https://qiita.com/rinpa/items/81766cd6a7b23dea9f3c)がおすすめです。

# 早速使ってみる：回帰問題編

回帰問題、分類問題で使用したコードは[こちら](optuna.py)

では早速、Lasso回帰問題で試してみることにします。
今回はscikit-learn、optuna、numpy を使用していきます。
今回は擬似的に回帰問題を生成し、その問題に対してLassoの正則化パラメータの`alpha`を最適化していきます。

まずは使用するライブラリのインストールから。

```python
import optuna
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_val_score, train_test_split
from matplotlib import pyplot as plt
# 並列処理用
import multiprocessing
cores = multiprocessing.cpu_count()
```

`sklearn.datasets`の`make_regression`を用いて回帰問題を生成します。
今回はデータ数が500、特徴量が64次元の問題を生成します。
`n_informative`で非ゼロ係数の個数を設定できるみたいです。

```python
# 回帰問題の生成
X, y, coef = make_regression(n_samples = 500, n_features = 64, n_informative = 32, noise = 0.1, coef = True)

# 正解となる回帰係数の可視化
plt.stem(np.where(coef)[0], coef[coef != 0], markerfmt = "x", use_line_collection=True)

# 訓練データと検証データを分割する
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2021)
```

チューニングなしのLassoによる予測です。
`X_train`、`y_train`という訓練データでLassoを学習させ、`X_test`に対して予測を行います。
評価指標として、`sklearn.metrics`の平均２乗誤差`mean_squared_error`を用います。

```python
# チューニングなしLassoの学習・予測
ans0  = Lasso().fit(X_train, y_train).predict(X_test)
mse0 = mean_squared_error(y_test, ans0)
```

では、本題のOptunaによるハイパラチューニングを行っていきましょう。

```python
# Lasso のチューニング
def tuningOfLasso(X, y):
    def objective(trial):
        # alpha をsuggest（提案）する範囲の指定
        alpha = trial.suggest_loguniform("alpha", 0.001, 10.0)
        reg = Lasso(alpha = alpha,
                        random_state = 2021,
                        max_iter = 1000)
        # 評価関数は平均２乗誤差の交差平均とする
        return cross_val_score(reg, X, y, n_jobs=cores, cv=5, scoring = "neg_mean_squared_error").mean()
    return objective

study = optuna.create_study(direction='maximize')
study.optimize(tuningOfLasso(X_train, y_train), n_trials=200)

trial = study.best_trial

print('Accuracy: {}'.format(trial.value))
print("Best hyperparameters: {}".format(trial.params))
```

こちらのコードを実行すると、`X_train`、`y_train`について、K-hold Cross Varidationしながら最適な`alpha`を探索してくれます。

```python
return cross_val_score(reg, X, y, n_jobs=cores, cv=5, scoring = "neg_mean_squared_error").mean()
```

の、`cv=5`の部分を任意の自然数に変更することで交差検証の分割を自由に変更することができます。

また、試行回数については

```python
study.optimize(tuningOfLasso(X_train, y_train), n_trials=200)
```

の、`n_trials=200`の部分を変更することで変更することができます。
探索するハイパラ数が増えたときは試行回数をあげた方が良いですね。

上記のコードを実行すると、

```console
[I 2021-03-01 18:09:48,360] Trial 0 finished with value: -0.6361886263369979 and parameters: {'alpha': 0.1089929580782823}. Best is trial 0 with value: -0.6361886263369979.
[I 2021-03-01 18:09:48,911] Trial 1 finished with value: -46.83685826162597 and parameters: {'alpha': 0.9457982360594444}. Best is trial 0 with value: -0.6361886263369979.
[I 2021-03-01 18:09:48,928] Trial 2 finished with value: -0.05752678116711631 and parameters: {'alpha': 0.02975376941756747}. Best is trial 2 with value: -0.05752678116711631.
[I 2021-03-01 18:09:48,941] Trial 3 finished with value: -10.435195110170392 and parameters: {'alpha': 0.4460940447672982}. Best is trial 2 with value: -0.05752678116711631.
[I 2021-03-01 18:09:48,971] Trial 4 finished with value: -3.78983984331537 and parameters: {'alpha': 0.2684712390509304}. Best is trial 2 with value: -0.05752678116711631.
:
:
:
```

のようにハイパラ探索が始まります。
最終的には以下のような出力が得られます。

```console
MSE: -0.012009973915115404
Best hyperparameters: {'alpha': 0.0011874315849132804}
```

この`alpha`を使用して検証データ`X_test`について予測を行ってみましょう。
そして、チューニングなしの結果`mse0`とチューニングした際の結果`mse1`を比較してみましょう。

```python
# lasso w/ tuning
ans1 = Lasso(random_state = 2021, alpha = 0.0011874315849132804).fit(X_train, y_train).predict(X_test)
mse1 = mean_squared_error(y_test, ans1)

print("mean squared error(MSE)")
print("lasso(default): ", mse0)
print("lasso(tuned): ", mse1)
```

結果がこちらです。

```
mean squared error(MSE)
lasso(default):  35.921399384461075
lasso(tuned):  0.013978818141855793
```

検証データに対する精度がかなり向上しました！
かなりハイパラ調整が効いていますね。


# 早速使ってみる：分類問題編

回帰問題、分類問題で使用したコードは[こちら](optuna.py)

分類問題では、Random Forest のハイパラを調整していきます。
Random Forest は「決定木のバギング」をベースとした学習器です。
今回は
* `n_estimators`:　用意する弱学習器の個数
* `max_features`:　条件分岐で使用する特徴量の数

をハイパラとして調整していきます。

まずは、必要なライブラリをインポートします。

```python
import optuna
import numpy as np
import multiprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, train_test_split
cores = multiprocessing.cpu_count()
```

`sklearn.datasets`の`make_classification`を使用して、分類問題を生成します。
今回はデータ数が500、特徴量が64次元の２値分類問題を生成します。
また、訓練データと検証データに分割を行います。

```python
X, y = make_classification(n_samples = 500, n_features = 64, n_informative = 32, n_classes = 2, random_state = 2021)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 2021, stratify = y)
```

まずはチューニングなしの Random Forest Classifier で分類問題を解いてみます。

```python
ans0 = RandomForestClassifier().fit(X_train, y_train).predict(X_test)
acc0 = accuracy_score(y_test, ans0)
```

また、先ほどと同様にチューニングを行っていきます。
`suggest_int`は整数値の提案を、`suggest_categorical`はカテゴリカルな提案を行います。
その他には、`suggest_loguniform`、`suggest_uniform`などがあり、調整したいハイパラの形式に合わせて適宜書き換えましょう、

```python
# Random Forest のチューニング
def tuningOfRF(X, y):

    def objective(trial):
        n_estimators = trial.suggest_int("n_estimators", 10, 500)
        max_features = trial.suggest_categorical("max_features", [int(np.sqrt(64)//2), int(np.sqrt(64)), int(np.sqrt(64)*2)])

        clf = RandomForestClassifier(random_state = 2021,
                                     n_estimators = n_estimators,
                                     n_jobs = cores//2)
    
        
        #ランダムフォレストモデルを交差検証してその平均スコア（今回はAccuracy）を返す
        return cross_val_score(clf, X, y, n_jobs=cores//2, cv=4, scoring = "accuracy").mean()
    return objective

# Optunaオブジェクトの作成 directionをmaximizeとすることで最大化
study = optuna.create_study(direction='maximize')
# 200回の試行で最適化をおこなう。
study.optimize(tuningOfRF(X_train, y_train), n_trials = 200)

trial = study.best_trial

# 最適パラメータ及びその交差検証結果の表示
print('Accuracy: {}'.format(trial.value))
print("Best hyperparameters: {}".format(trial.params))
```

結果が以下のようになりました。

```
Accuracy: 0.8275
Best hyperparameters: {'n_estimators': 312, 'max_features': 4}
```

RandomForestモデルのハイパラ調整の有無で検証精度を比較してみましょう。

```python
ans1 = RandomForestClassifier(random_state = 2021, n_estimators = 312, max_features = 4).fit(X_train, y_train).predict(X_test)
acc1 = accuracy_score(y_test, ans1)

print("Accuracy")
print("RandomForest(default): ", acc0)
print("RandomForest(tuned): ", acc1)
```

以下の結果となりました。

```
Accuracy
RandomForest(default):  0.88
RandomForest(tuned):  0.9
```

微妙〜〜〜〜にですが、精度が向上していることがわかります。

# まとめ

Optunaによるハイパラ調整を行いました。
回帰、分類の例で確かに学習器の能力向上が見受けられました。
しかしながら、必ずしも調整した学習器が性能が上ということにならないケースもあるようです。
他の学習器についても同様の形式でハイパラの調整ができるので、紹介したコードをいじりながら是非、他のモデルでのハイパラ調整も行ってみてください！

## 参考
1. [Optuna公式](https://optuna.readthedocs.io/en/stable/)
2. [optuna入門](https://qiita.com/studio_haneya/items/2dc3ba9d7cafa36ddffa)
3. [optunaによるrandom forestのハイパーパラメータ最適化](https://note.com/utaka233/n/ne71851e1d678)
4. [optunaでハイパーパラメータ最適化](https://qiita.com/illumination-k/items/d0d077af12931176fec3)