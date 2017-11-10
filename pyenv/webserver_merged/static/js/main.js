/*
$( "#bt_1" ).button({
    icon: "ui-icon-gear",
    showLabel: true
});
*/
$("#button1").click(function(){
    $("#setteidialog").dialog("open");
});
/*
$("#bt_2").button({
    icon: "ui-icon-folder-open",
    showLabel: true
});
*/
$("#button2").click(function(){
    $("#kekkadialog").dialog("open");
    
});

$("#button3").click(function(){
    console.log("sent start signal");
    ws.send("start");
});
    
//$("#esa").text("餌2に決定しました")
