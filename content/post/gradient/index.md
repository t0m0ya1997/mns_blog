---
title: "最急降下法を画像を例に実感する"
description: ""
date: 2020-12-09T01:36:09+09:00
tags: ["gradient descent", "image processing", "勾配法", "画像処理", "Python"]
categories: ["research", "study"]
draft: false
math: true
---
# はじめに
深層学習でもよく使われる最適化手法「最急降下法」の原理を紹介し，画像処理に適用してみたという記事です．

# 最急降下法
そもそも最適化問題とは，「**与えられた制約の中で，目的関数値を最小化もしくは最大化させる解を求める問題**」のことです．
ここでいう制約や目的関数は様々で，例えば，「線形等式・不等式の制約下での線形な目的関数の最適化問題」は「[線形計画法](https://ja.wikipedia.org/wiki/線型計画法)(Linear Programming: LP)」と呼ばれたり，「線形等式・不等式の制約下での２次関数で表される目的関数の最適化問題」は「[２次計画法](https://ja.wikipedia.org/wiki/二次計画法)(Quadratic Programming: QP)」と呼ばれたりと様々な問題に分類できます．

最急降下法は最適化問題を解くための手法(最適化手法)で，そのシンプルさとは裏腹に，深層学習で用いられる[確率的勾配降下法](https://ja.wikipedia.org/wiki/確率的勾配降下法)(Stochastic Gradient Descent: SGD)などの様々な最適化手法の基礎となる重要な手法です．

目的関数を\\(f:\boldsymbol{x}\rightarrow y\\)とします．
ここで引数 \\(\boldsymbol{x}\in\mathbb R^d\\), 返り値 \\(y\in\mathbb R\\) とします．
関数 \\(f\\) の制約なしの最適化問題を考えます．
「関数 \\(f\\) を最小にする \\(\boldsymbol{x}\\) を \\(\boldsymbol{x}^\*\\)とする」すなわち
$$
\boldsymbol{x}^\* = \arg\min_x f(\boldsymbol{x})
$$
という問題を考えるわけです．

このような問題に対して，最急降下法では以下の操作を繰り返すことによって最適解 $\boldsymbol{x}^\*$ を求めます．
$$
\boldsymbol{x}^{(n+1)}\leftarrow \boldsymbol{x}^{(n)} - \nu\nabla_x f(\boldsymbol{x}^{(n)})
$$
ここで， \\(\boldsymbol{x}^{(n)}\\) は \\(n\\) 回目の更新での変数 \\(\boldsymbol{x}\\) の値を意味しています．
パラメータ \\(\nu\\) はステップサイズと呼びます．

反復ごとに効率的な目的関数の値を小さくするステップサイズ \\(\nu\\) を決めていく[直線探索](https://ja.wikipedia.org/wiki/直線探索)の話もするべきなのですが，今回は割愛します．

# 画像に対する最急降下法
さて，最急降下法の説明はここまでにして，実際に使ってみましょう．
今回は画像 \\(\boldsymbol{x}\in\mathbb R^d\\) を，何らかの画像 \\(\boldsymbol{t}\in\mathbb R^d\\) に最急降下法で近づけていくことを考えます．

今回はシンプルに目的関数を \\(\boldsymbol{x,t}\\) の２乗誤差を目的関数とし，
$$
\boldsymbol{x}^\* = \arg\min_x ||\boldsymbol{t}-\boldsymbol{x}||_2^2
$$
という問題を考えます．
目的関数が２次関数であるため，実はこの問題では最急降下法で大域的な最適解を得ることができますが，一般の問題に対しては最急降下法では局所解を求めるアルゴリズムであることに注意してください．
目的関数の勾配は
$$
\nabla_x f(\boldsymbol{x}) = -2(\boldsymbol{t}-\boldsymbol{x})
$$
であるので，最急降下法での更新式は
$$
\boldsymbol{x}^{(n+1)}\leftarrow \boldsymbol{x}^{(n)} +2\nu(\boldsymbol{t}-\boldsymbol{x}^{(n)})
$$
と導くことができます．

今回はPython, OpenCV を用いて実装を行いました．

```python

# import libraries
from tqdm import tqdm
import numpy as np
import cv2

# 目標とする画像t
t = np.float32(cv2.imread("path/to/terget.jpg"))
# 変数x の初期値として乱数を設定
x = np.random.rand(t.shape[0], t.shape[1], t.shape[2]) * 255

nu = 0.005

# 動画保存用
frame_rate = 24.0
size = (x.shape[0], x.shape[1])
fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
writer = cv2.VideoWriter('path/to/output.mp4', fmt, frame_rate, size)

# 最急降下法
for _ in tqdm(range(10000)):
    x = x + 2 * nu * (t - x) # 更新操作
    psnr = cv2.PSNR(x, t) # PSNRの算出
    writer.write(np.uint8(x))
    if psnr > 35.0: # PSNR が 35 以上であればループを抜ける
        break

writer.release()
cv2.destroyAllWindows()
```
上のコードを実行すると，mp4形式で砂嵐の初期画像 \\(\boldsymbol{x}^{(0)}\\) から，目標とする画像 \\(\boldsymbol{t}\\) へ近づいていく動画が保存されます．
[デモ](https://github.com/t0m0ya1997/gradient-descent)からダウンロードしていただくと簡単に実行できるので是非ご覧ください．

# まとめ
本記事では，最急降下法の紹介を画像の例を通して行いました．
時間があるときにこの記事自体も更新していきますのでよろしくお願いします．