$("#kekkaimg1").hide();
$("#kekkaimg2").hide();
$("#kekkaimg3").hide();
$("#kekkadialog").dialog({
    autoOpen: false,
    modal: true
});
/*
$("#accordion").accordion({
    collapsible: true,
    active: false,
    event: "click"
});
*/

var receivedKekka　= {};

//メッセージ受信時
ws.onmessage = function(jusin){
    console.log(jusin.data);
    if (jusin.data.slice(0,1) === "{" && jusin.data.slice(-1) === "}"){
        //中括弧でくくられたもの(json)
        receivedKekka = $.parseJSON(jusin.data);
    }else{
        //json以外の何か変なもの
        console.log("json以外のデータです");
    }
}



$("#button2").click(function(){
    //データ受け取り済みの場合(キーが1個以上あるとき)
    if(Object.keys(receivedKekka) !== 0 ){
        
        $("#kekkaimg1").hide();
        $("#kekkaimg2").hide();
        $("#kekkaimg3").hide();
        var jsonData = receivedKekka;
        /*console.log(jsonData);
        console.log(jsonData.date);
        console.log(jsonData.setting.esa);
        console.log(jsonData.setting.suiryu);
        console.log(jsonData.setting.haikei);
        console.log(jsonData.setting.LED);*/
        $("#date").text("最終更新日:" + jsonData.date);
        $("#esa").text("餌"+String(jsonData.setting.esa));
        
        if(jsonData.setting.suiryu === 0){
            $("#suiryu").text("弱い");
        }else if(jsonData.setting.suiryu === 1){
            $("#suiryu").text("強い");
        }
        
        
        
        $("#haikei").hide();
        if(jsonData.setting.haikei === 1){
            $("#kekkaimg1").show();
        }else if(jsonData.setting.haikei === 2){
            $("#kekkaimg2").show();
        }else if(jsonData.setting.haikei === 3){
            $("#kekkaimg3").show();
        }
        var led = jsonData.setting.LED;
        
        var ledcode = "#" + ("0"+led[0].toString(16)).slice(-2) + ("0"+led[1].toString(16)).slice(-2) + ("0"+led[2].toString(16)).slice(-2);
        $("#led").html("<input type='color' id='kekkaled' disabled value='"+ledcode+"'>" + ledcode);
        
    }else{
        console.log("json not found")
    }
});