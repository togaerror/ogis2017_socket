var cs  = document.getElementById('animationCanvas');
const fishMax = 20;
var w_Width = window.innerWidth;
var w_Height = window.innerHeight;
fishImage = [];
initFishimage();
window.addEventListener('resize',canvas_resize,false);
canvas_resize();

function canvas_resize(){
  w_Width = window.innerWidth;
  w_Height = window.innerHeight;
  cs.setAttribute('width',w_Width);
  cs.setAttribute('height',w_Height);
}

function initFishimage(){
  var i = 0;
  var temp;
  while(i < fishMax){
    fishImage[i] = new Image();
    temp = Math.floor(Math.random()*4)+1;
    fishImage[i].direction =  Math.floor(Math.random()*2); // 0:left->right or 1:right->left 
    if(fishImage[i].direction == 0){
      fishImage[i].src = "../static/img/fish00" + temp +".png";
    }else{
      fishImage[i].src = "../static/img/fish00" + temp +"R.png";
    }
    fishImage[i].position_x = Math.floor(Math.random()* w_Width);
    fishImage[i].position_y = Math.floor(Math.random()* w_Height);
    fishImage[i].speed = Math.floor(Math.random()*5)+2; 
    i += 1;
  }
}

function drawLoopSquare() {
  var ctx = cs.getContext('2d');
  var w = cs.width;
  var h = cs.height;
  console.log(w,h);
  /* 描画フロー */
  function render() {
    // Canvas全体をクリア
    ctx.clearRect(0, 0, w, h);
    var i = 0;
    while(i < fishMax){
      ctx.drawImage(fishImage[i], fishImage[i].position_x,fishImage[i].position_y, 90,30);
      if(fishImage[i].direction == 0){
        if(fishImage[i].position_x > w) {
          fishImage[i].position_x = -90;
          fishImage[i].position_y = Math.floor(Math.random()*w_Height);
        }else{
          fishImage[i].position_x += fishImage[i].speed;
        }
      }else{
        if(fishImage[i].position_x < -90) {
          fishImage[i].position_x = w+90;
          fishImage[i].position_y = Math.floor(Math.random()*w_Height);
        }else{
          fishImage[i].position_x -= fishImage[i].speed;
        }
      }

      i += 1;
    }
  }
  setInterval(render, 50);
}
drawLoopSquare();
function goFS(){
  document.html.requestFullscreen();
}
goFS();