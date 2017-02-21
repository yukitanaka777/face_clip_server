var clm = new clm.tracker({useWebGL:true});
var fb = new faceDeformer();
var backView = new faceDeformer();
var masking_switch = false;
var dataCtn = 1;
var maskAnimDate
var canvas;
var FaceImgArr = {};
var mtx;
var Button;
var BV;
var btx;

$(function(){
  console.log($.cookie('Solaris_model_id'));
  canvas = document.getElementById('canvas');
  BV = document.getElementById('backView');
  clm.init(pModel);
  $.getJSON('./static/vector.json',function(data){
    maskAnimDate = data;
    loadImage(ImgURL, function (img) {
      drawImage(img);
      $("#loadingLine").css('width','0%').animate({width:'20%'},500);
    });
  });
  Button = $('#startButton');
  Button.css('display','none');

  Button.click(function(){
    $('canvas#model').css('opacity','0');
    Button.text('Scanning');
    Button = null;
    var SendInfo = {
      "img":FaceImgArr,
      "name":ImgName,
      "id":ImgId
    }
    $.ajax({
      type: 'POST',
      contentType: 'application/json',
      url: "http://192.168.1.6:9000/save_and_learn",
      crossDomain: true,
      dataType : 'json',
      data : JSON.stringify(SendInfo),
      success : function(result) {
        //location.href = "http://192.168.1.6:5000/takePicture";
        $.cookie('Solaris_model_id',result,{path:'/',domain:'192.168.1.6'});
        console.log(result);
      },error : function(result){
        console.log(result);
        //location.href = "http://192.168.1.6:5000/takePicture";
      }
    });
    rendering();
  });
  fb.init(canvas);
  backView.init(BV);
});

function rendering(){
  if(masking_switch && dataCtn < Object.keys(maskAnimDate).length){
    masking(maskAnimDate[dataCtn]);
    dataCtn++;
    requestAnimationFrame(rendering);
  }else if(dataCtn == Object.keys(maskAnimDate).length){
    console.log('finish');
    cancelAnimationFrame(rendering);
  }
}

function masking_init(maskingPos){
  var MaskImg = document.createElement("img");
  var resizeView = document.getElementById("resizeView");
  var rtx = resizeView.getContext('2d');
  MaskImg.onload = function(){
    fb.load(MaskImg,maskingPos,pModel);
    backView.load(MaskImg,maskingPos,pModel);
    drawRectMaskingPos(maskingPos);
    masking_switch = true;
    $("#loadingLine").css('width','40%').animate({width:'75%'},500);

    for(var i = 1; i < Object.keys(maskAnimDate).length; i++){
      var marksArr = new Array(71);
      for(var j = 0; j < maskingPos.length; j++){
        var x = maskingPos[j][0] + maskAnimDate[i][j][0];
        var y = maskingPos[j][1] + maskAnimDate[i][j][1];
        var marksPos = [x,y];
        marksArr[j] = marksPos
      }
      if((i % 15) == 0){
        backView.clear();
        //backView.draw(maskAnimDate[i]);
        backView.draw(marksArr);
        rtx.clearRect(0,0,120,90);
        rtx.drawImage(BV,0,0,120,90);
        var createImg = resizeView.toDataURL('image/jpg');
        FaceImgArr[i] = createImg;
      }
      maskAnimDate[i] = marksArr;
    }

    $("#loadingLine").css('width','75%').animate({width:'100%'},500,function(){
      $("#loading").css('display','none');
      Button.fadeIn("slow");
    }

  );
  }
  MaskImg.src = ImgURL;
}

function masking(masPos){
  if(masPos){
    fb.draw(masPos);
  }else{
    console.log(masPos);
  }
}

function drawImage(img) {
  var model = document.getElementById('model');
  var imgW = img.width;
  var imgH = img.height;

  mtx = model.getContext('2d');
  model.width = imgW;
  model.height = imgH;

  mtx.drawImage(img, 0, 0, imgW,imgH);
  clm.init(pModel);
  clm.start(model);
  certain_clm_pos();
}

function certain_clm_pos(){
  if(clm.getCurrentPosition()){
    maskingPos = clm.getCurrentPosition();
    masking_init(maskingPos);
    //console.log(mask_position);
    //console.log(maskingPos);
    $("#loadingLine").css('width','20%').animate({width:'40%'},500);
  }else{
    console.log("not get pos");
    setTimeout(function(){
    certain_clm_pos();
  },1000);
 }
}

function drawRectMaskingPos(pos){
  for(var i = 0; i < pos.length; i++){
    mtx.beginPath();
    mtx.arc(pos[i][0],pos[i][1],5,Math.PI*2,false);
    mtx.stroke();
    mtx.fill();
    mtx.closePath();
	}
}
