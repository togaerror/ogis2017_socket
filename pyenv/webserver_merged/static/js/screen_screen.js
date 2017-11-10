/*
背景画像を変える関数
argument: imageID
*/
var img_id = 1;
const max = 3;
const min = 0;

function shotImage(){
  $("#mainBackgroundImage").show();
  $("#subBackgroundImageA").hide();
  $("#subBackgroundImageB").hide();
  $("#initScreen").show();  
}

// 1つの画像を表示する
function oneImage(imageId){
  $("#initScreen").hide();
  // javascript内では相対パスでの指定でいける
  $("#mainBackgroundImage").attr("src", "../static/img/backgroundImg_0" + imageId + ".jpg");
}

// 2つの画像を表示する
function twoImages(imageId_a, imageId_b){
  $("#initScreen").hide();  
  $("#mainBackgroundImage").hide();
  $("#subBackgroundImageA").show();
  $("#subBackgroundImageB").show();
  $("#subBackgroundImageA").attr("src", "../static/img/backgroundImg_0" + imageId_a + ".jpg");
  $("#subBackgroundImageB").attr("src", "../static/img/backgroundImg_0" + imageId_b + ".jpg");
}
