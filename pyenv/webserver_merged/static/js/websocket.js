//ウェブソケットを開く
var ws;
ws = new WebSocket("ws://localhost:8080/websocket");
//ws = new WebSocket("ws://192.168.2.150:8080/websocket");

// メッセージを受けた時の処理
ws.onmessage = function(ev) {
  console.log(ev.data);
}

// メッセージ送り命令
function messageSend(msg){
  ws.send(msg);
}
