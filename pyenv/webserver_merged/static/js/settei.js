//選択された背景画像の番号を入れておく
var haikeinum=1


//要素が表示されているか高速判定するプラグイン if文に入れてT else Fの形
$.fn.isVisible = function() {
    return $.expr.filters.visible(this[0]);
};
//設定決定時ダイアログ

$("#kakunindialog").dialog({
    autoOpen: false,
    modal: true,
    open:function(){
        var esaVal = $("input[name='esaradio']:checked").val();
        var suiryuVal = $("input[name='suiryuradio']:checked").val();
        
        var led  = $("#ledcolor").val();
        var esaStr = "";
        if(esaVal === "1"){
            esaStr = "餌1";
        }else if (esaVal === "2"){
            esaStr = "餌2";
        }

        var suiryuStr = "";
        if (suiryuVal === "0"){
            suiryuStr = "弱い";
        }else if(suiryuVal === "1"){
            suiryuStr = "強い";
        }

        
        //var red = parseInt(led.substring(1,3),10);

        $("#nakami").html("<div>餌:" + esaStr +"</div><div>水流:" + suiryuStr + "</div><div>背景:" + haikeinum + "</div><div>LED:<input type='color' disabled value='" + led + "' " + led + "></div>");
    },
    buttons:[
        {
            text:"いいえ",
            click:function(){
                $(this).dialog("close");
            }
        },
        {
            text:"はい",
            click:function(){
                var esaVal = $("input[name='esaradio']:checked").val();
                var suiryuVal = $("input[name='suiryuradio']:checked").val();
               
                var led  = $("#ledcolor").val();
                var hiduke = new Date();

                var log = hiduke.getFullYear()+"/"+("0"+(hiduke.getMonth()+1)).slice(-2)+"/"+("0"+hiduke.getDay()).slice(-2)+" "+("0"+hiduke.getHours()).slice(-2)+":"+("0"+hiduke.getMinutes()).slice(-2)+"."+("0"+hiduke.getSeconds()).slice(-2);


                if(esaVal === undefined){
                    alert("餌を選択して下さい");
                    $(this).dialog("close");
                }else if(suiryuVal === undefined){
                    alert("水流を選択して下さい");
                    $(this).dialog("close");
                }else{
                    //送信用json形式記述
                    var suiryuInt = -1;
                    if (suiryuVal === "0"){
                         suiryuInt = 0;
                    }else if(suiryuVal === "1"){
                         suiryuInt = 1;
                    }

                    
                    
                    var rgb = [parseInt(led.substring(1,3), 16),parseInt(led.substring(3,5), 16),parseInt(led.substring(5,7), 16)]
                    
                    obj = '{"name":"set","date":"' + log + '", "setting":{"esa":' + esaVal +', "suiryu":' + suiryuInt + ', "haikei":' + haikeinum + ', "LED":[' + rgb + ']}}';
                    console.log(obj);
                    //webserverにobjを送る
                    console.log(ws);
                    ws.send(obj);

                    $("#json").html(obj);
                    $(this).dialog("close");
                    alert("送信しました");
                }
            }
        }
    ]
});

//設定ダイアログ　遷移と決定のボタンはここに記述している
$("#setteidialog").dialog({
    autoOpen: false,
    modal: true,
    height: 390,
    buttons:[
        {
            //前へボタン 表示されているものを検出してそれを隠した跡前の選択肢を表示する
            text: "前へ",
            click:function(){
                

                if($("#esaset").isVisible()){
                    //餌選択肢表示中
                    $.when(
                        $("#esaset").hide()
                    ).done(function(){
                        $("#ledset").show();
                    });
                    $("#settingpage").text("項目4/4");
                    $("#bar").progressbar("value", 4);
                }else if($("#suiryuset").isVisible()){
                    //水流選択肢表示中
                    $.when(
                        $("#suiryuset").hide()
                    ).done(function(){
                        $("#esaset").show();
                    });
                    $("#settingpage").text("項目1/4");
                    $("#bar").progressbar("value", 0);
                }else if($("#haikeiset").isVisible()){
                    //背景選択肢表示中
                    $.when(
                        $("#haikeiset").hide()
                    ).done(function(){
                        $("#suiryuset").show();
                    });
                    $("#settingpage").text("項目2/4");
                    $("#bar").progressbar("value", 1);
                }else if($("#ledset").isVisible()){
                    //LED選択肢表示中
                    $.when(
                        $("#ledset").hide()
                    ).done(function(){
                        $("#haikeiset").show();
                    });
                    $("#settingpage").text("項目3/4");
                    $("#bar").progressbar("value", 2);
                }
            }
        },
        {
            //決定ボタン　それぞれの要素を取得しjsonノカタチに整形して送る予定　今はコンソールに流している
            text: "決定",
            click:function(){
                $("#kakunindialog").dialog("open");


            }
        },
        {
            //次へボタン 前へボタンとほぼ同じ
            text: "次へ",
            click:function(){
                
                if($("#esaset").isVisible()){
                    //餌選択肢表示中
                    $.when(
                        $("#esaset").hide()
                    ).done(function(){
                        $("#suiryuset").show();
                    });
                    $("#settingpage").text("項目2/4");
                    $("#bar").progressbar("value", 1);
                }else if($("#suiryuset").isVisible()){
                    //水流選択肢表示中
                    $.when(
                        $("#suiryuset").hide()
                    ).done(function(){
                        $("#haikeiset").show();
                    });
                    $("#settingpage").text("項目3/4");
                    $("#bar").progressbar("value", 2);
                }else if($("#haikeiset").isVisible()){
                    //背景選択肢表示中
                    $.when(
                        $("#haikeiset").hide()
                    ).done(function(){
                        $("#ledset").show();
                    });
                    $("#settingpage").text("項目4/4");
                    $("#bar").progressbar("value", 3);
                }else if($("#ledset").isVisible()){
                    //LED選択肢表示中
                    $.when(
                        $("#ledset").hide()
                    ).done(function(){
                        $("#esaset").show();
                    });
                    $("#settingpage").text("項目1/4");
                    $("#bar").progressbar("value", 0);
                }
            }
        }
    ],
    open:function(){
        $("#settingpage").text("項目1/4")
        $("#bar").progressbar("value", 0);
        
    }
});
//最初意外隠す
$("#button1").click(function(){
    $("#suiryuset,#haikeiset,#ledset").hide();
    $("#esaset").show();
});
$("#suiryuset,#haikeiset,#ledset").hide();


//餌
$("#esaset input").checkboxradio({
    icon: false
});

//水流
$("#suiryuset input").checkboxradio({
    icon: false
});


//背景
/*$("#haikeicolor").change(function(){
    var val = $(this).val();
    $("#haikeicolorcode").text(val);
});*/
$("#img1").show();
$("#img2").hide();
$("#img3").hide();



$("#previmg").button();
$("#previmg").click(function(){

    if($("#img1").isVisible()){
        haikeinum = 3;
        $("#img1").hide();
        $("#img3").show();
    }else if($("#img2").isVisible()){
        haikeinum = 1;
        $("#img2").hide();
        $("#img1").show();
    }else if($("#img3").isVisible()){
        haikeinum = 2;
        $("#img3").hide();
        $("#img2").show();
    }
});
$("#nextimg").button();
$("#nextimg").click(function(){
    if($("#img1").isVisible()){
        haikeinum = 2;
        $("#img1").hide();
        $("#img2").show();
    }else if($("#img2").isVisible()){
        haikeinum = 3;
        $("#img2").hide();
        $("#img3").show();
    }else if($("#img3").isVisible()){
        haikeinum = 1;
        $("#img3").hide();
        $("#img1").show();
    }
});

//LED
$("#ledcolor").change(function(){
    var val = $(this).val();
    $("#ledcolorcode").text(val);
});
//選択ページ数
$("#bar").progressbar({
    max: 3,
    value:0,

});
