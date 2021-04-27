const num = 2000;
let range = 24;

const ax = [];
const ay = [];
const rs = [];
const gs = [];
const bs = [];

function setup() {
    var myCanvas = createCanvas(innerWidth, innerHeight);
    for (let i = 0; i < num; i++) {
        ax[i] = width / 2;
        ay[i] = height / 2;
        rs[i] = random(0, 255);
        gs[i] = random(0, 255);
        bs[i] = random(0, 255);
    }
    frameRate(30);
    myCanvas.class('backgroundsketch');
}

function draw() {
    background(255);
    // => 末尾の値のみ変わらず、ほかは１つ左に移動する
    for (let i = 1; i < num; i++) {
        ax[i - 1] = ax[i];
        ay[i - 1] = ay[i];
    }

    // 末尾の値に、-6から6の間のランダムな浮動小数点数を加算
    // => 新しい値になる。これが運動の変化をもたらす元
    ax[num - 1] += random(-range, range);
    ay[num - 1] += random(-range, range);

    // 加算した末尾の値を、キャンバスの幅と高さに制限
    ax[num - 1] = constrain(ax[num - 1], 0, width);
    ay[num - 1] = constrain(ay[num - 1], 0, height);

    // 点を結んで線を描く
    for (let j = 1; j < num; j++) {
        // valは10以上100未満の数値
        const val = j / num * 204.0 + 51;
        stroke(128, ax[j-1]/width*255, ay[j-1]/height*255, val);
        line(ax[j - 1], ay[j - 1], ax[j], ay[j]);
    }
}

function windowResized() {
    resizeCanvas(innerWidth, innerHeight);
}