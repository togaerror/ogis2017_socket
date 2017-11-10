/************************
connect.js
WebSocket sample appのためのクライアント側js
バック側が用意する関数
  orderGetLevel()：現在のレベルを返す．ただし，そんなことしなくてもレベルの変化があったらクライアント側に送る
  orderDown():下げ指示　<-多分使うのはこれだけ，任意のタイミングでこれを呼び出し
************************/
// IP固定されたサーバのIPアドレスの8080番ポート/wsに接続
var ws = new WebSocket("ws://localhost:8080/ws");
//var ws = new WebSocket("ws://192.168.11.8:8080/scws");
//var ws = new WebSocket("ws://192.168.2.150:8080/scws");
var count = 1;
//WebSocketのハンドシェイク成功時（初期動作）
ws.onopen = function(){
  console.log("Connection established!!");
  //intervalSender(); // デバッグ用JSON送信関数
};

// メッセージを受け取ったらJSON形式に変換して読み込む
ws.onmessage = function (rcv) {
  console.log(rcv.data);  //受信した文字列
  rcv = rcv.data.split(',');
  if(rcv.length == 1){
    if(rcv[0] == 0){
      shotImage();
    }else{
      // 1枚全画面
      oneImage(rcv[0]);
    }
  }else if(rcv.length == 2){
    if(rcv[0] == 0){
      shotImage();
    }else{
      // 2枚左右
      twoImages(rcv[0], rcv[1]);
    }
  }else{
    console.log("Error: Array index is over flow!!!");
  }
};

// デバッグ用
/*
// websocketメッセージ送り関数
function sendMessage(message){
  console.log("send: " + message);
  ws.send(message);
}

function intervalSender(){
  setInterval(function(){
    a = Math.floor(Math.random() * (max + 1 - min) ) + min;
    //a = Math.floor(Math.random() * (max + 1 - min) ) + min;
    b = Math.floor(Math.random() * (max + 1 - 1) ) + 1;
    while(a == b){
      b = Math.floor(Math.random() * (max + 1 - 1) ) + 1;
    }
    if(Math.floor(Math.random() * (10 + 1 - 1) ) + 1 > 5){
      // JSONデータ作成例 main
      message = a
    }else{
      // JSONデータ作成例 two
      message = a + "," + b;
    }
    ws.send(message);
  }, 5000);
}
*/