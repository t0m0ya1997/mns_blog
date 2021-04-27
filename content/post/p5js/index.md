---
title: "p5.js で遊んでみた"
description: "Processing ベースのグラフィックJavaScript ライブラリをいじってブログの背景にするまで"
date: 2020-12-31T14:44:09+09:00
tags: ["JavaScript", "p5.js"]
categories: ["blog"]
math: true
draft: true
---

# p5.js とは
p5.js はProcessingの本来の目的である、アーティストやデザイナー、教育者、初学者のためのコーディング環境を今日のWebにおいて再解釈するJavaScriptライブラリです（[公式サイト](https://p5js.jp)より）。
言うなれば、「Processing がJavaScriptでできますよ」ってことです。
Processing は電子アートとかビジュアルアートに関する言語です。

p5.jsを使うためには、ライブラリファイルを読み込む必要があります。
直接、[公式サイト](https://p5js.org/download/)からダウンロードして、`p5.js`などのファイルをローカルで読み込むことも可能です。
今回はネットワーク経由で読み込むため、以下の文をhtml中の`<script>`タグ内もしくはJavaScriptファイル内に書いておきます。

```JavaScript
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.7.2/p5.js"></script>
```

基本的にp5.js は2つの関数`setup()` と`draw()`があれば動きます。
`setup()`はページ読み込み時に１度だけ呼び出され、主に描写範囲などを設定します。
`draw()`はページ切り替えごとに呼び出され、デフォルトでは1/60秒おきに呼び出されますが`setup()`内で`frameRate(30)`などと書けば、フレームレートを変更したりできます。
こちらに主な描写処理を書いていきます。

# ブラウン運動の実装

実際にブラウン運動のような粒子の運動をシミュレーションしたものを描写してみます。
本サイトのトップページの背景もこの運動のシミュレーションになっています。

お手元のテキストエディタを開いて、以下のコードをコピペし、「sample.html」等の名前をつけて保存すればOKです。
そのファイルをブラウザなどで表示すると、なんか動き始めるはずです。

```html
<html>
    <head>
    <title>ブラウン運動</title>
    <!--ここでp5.js を読み込みます-->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.7.2/p5.js"></script>
    </head>
    <body>
<script>

// 描写する線の本数
const num = 2000;
// 粒子が移動するさいのスケールで大きくなるとより激しい運動になります
let range = 24;

const ax = [];
const ay = [];
const rs = [];
const gs = [];
const bs = [];

function setup() {
    // キャンバス（描画領域）のサイズを設定します
    // createCanvas(windowWidth, windowHeight)などとするとウィンドウサイズが設定されます
    createCanvas(800, 800);
    for (let i = 0; i < num; i++) {
        ax[i] = width / 2;
        ay[i] = height / 2;
        rs[i] = random(0, 255);
        gs[i] = random(0, 255);
        bs[i] = random(0, 255);
    }
    frameRate(30);
}

function draw() {
    background(0);
    // => 末尾の値のみ変わらず、ほかは１つ左に移動する
    for (let i = 1; i < num; i++) {
        ax[i - 1] = ax[i];
        ay[i - 1] = ay[i];
    }

    // 末尾の値に、-rangeからrangeの間の浮動小数点乱数を加算します
    ax[num - 1] += random(-range, range);
    ay[num - 1] += random(-range, range);

    // 末尾値を、描写領域の幅と高さに制限
    ax[num - 1] = constrain(ax[num - 1], 0, width);
    ay[num - 1] = constrain(ay[num - 1], 0, height);

    // 点を結んだ線を描写
    for (let j = 1; j < num; j++) {
        // valは10以上100未満の数値
        const val = j / num * 204.0 + 51;
        line(ax[j - 1], ay[j - 1], ax[j], ay[j]);
    }
}

</script>
</body>
</html>
```

**詳しい書き方については時間がある時に随時追記していきます…**申し訳ない。
参考サイトや「p5.js サンプル」などでググってみると結構出てくるはずです。

# hugoで作ったブログに組み込む
このサイトは静的サイトジェネレータのHugo を用いて作成しております。


## 参考