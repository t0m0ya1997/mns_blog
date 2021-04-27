---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "YouTubeのAPIを叩いていく話"
subtitle: ""
summary: "今回はYouTube から提供されている `YouTube Data API` をポチポチ叩いて遊ぶという雑な記事です."
authors: []
tags: ["Python", "YouTube", "mp3"]
categories: ["tech"]
date: 2020-01-10T18:42:33+09:00
lastmod: 2020-01-10T18:42:33+09:00
featured: false
draft: true

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

こんにちは, hiratchi です.
今回はYouTube から提供されている `YouTube Data API` をポチポチ叩いて遊ぶという雑な記事です.
~~ココには書きませんが, 最終的にはYouTube 自炊を目標にしています.~~
基本的には Python で実装していきますが, 知らない人でもなんとなく解ると思います.

---
# 目次
1. [Youtube Data API って?](#1)
2. [準備](#2)
3. [](#3)
4. [](#4)
5. [youtube-dl の紹介](#5)
---

## 1. YouTube Data API って? {#1}
YouTubeが提供しているAPIで, 動画やチャンネル, プレイリストなどに関わる情報を取得し, 自分のWebサイトやアプリケーションなどの中で使用することができます.
使用するにあたってAPI キーを取得する必要があります.

## 2. 準備 {#2}
一応, 実験環境としてはPythonの最新使っときゃ大丈夫だと思います.
IDE は今回, 結構辞書型の中身を覗くことが多かったのでSpyder ってやつを使ってます.
Anaconda 入れるとデフォルトで入っていると思うので, 運のいい人は`$spyder` で起動するはず.

今回は, Python でAPI を利用していきますので, [コチラ](https://github.com/mabrownnyu/youtube-data-api)のライブラリを使用します.
README に従ってインストールしましょう.

```console 
$pip install youtube-data-api 
```
使用するのは簡単です.

```python: main.py
from youtube_api import YoutubeDataApi;

api_key = 'あなたの取得したAPIキー';
yt = YoutubeDataApi(api_key);
```
これで, `yt` というYoutubeDataAPI クラスのインスタンスが出来上がったので, こいつを使って色んな情報を取得していきましょう.

## 3. プログラム {#3}

## 4. 解説 {#4}
簡単なスクリプトなのですが, 以下の記事を参考にしました.
Easydict って, `.` でキーを参照することのできる結構便利な辞書型を提供してくれているライブラリで, `ImportError` が出た人は, コマンドラインで
```console
$pip install easydict
```
でインストールしましょう.
こうやって, 他人のコードから学習していくんですね.
あと, Python では `;` はつけなくて良いのですが, C とか C++ 書くときにつけ忘れちゃいそうなので, なるべく僕はつけるようにしています.

## 5. youtube-dl の紹介 {#5}
さて, 今回はデータの取得にとどめましたが, いろいろと応用できます.
Python には`youtube-dl` というライブラリがありまして, こいつ使えば動画をダウンロードできちゃうんですよ.
URLを指定する必要があるのですがそれは, この記事で扱ったAPI で取得できる`videoId` の値を利用して, `https://www.youtube.com/watch?v=【videoId】`という形で指定できます.
あとは自分でスクリプト書けば自炊できちゃいますねって話でした.
そこはなんか自分で調べてみましょう, google さんはすごいので.