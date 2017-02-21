navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL;

var Tracker;
var clm = new clm.tracker({useWebGL:true});
var fb = new faceDeformer();
var webgl
var track_data = {};
clm.init(pModel);
var tracking_data = {};
var track_switch = true;
var masking_switch = false;
var dataCtn = 0;
var mtx;
var model;
var masPos;
var maskAnimDate

reading_ctn = 0;

$(function(){
	var video = document.getElementById('video');
	var canvas = document.getElementById('canvas');
	model = document.getElementById('model');
	var ctx = canvas.getContext('2d');
    mtx = model.getContext('2d');
    $.getJSON('./static/position.json',function(data){
	    maskAnimDate = data;
	});

    loadImage(ImgURL, function (img) {
      console.log("顔検出中...");
      drawImage(img);
    });

	webgl = document.getElementById('webgl');
	fb.init(webgl);
	//track_start(video,ctx);
});

function track_start(video,ctx){
	var video_option = {
		mandatory:{
			maxWidth:640,
			maxHeight:480
		}
	}

	navigator.getUserMedia(
		{audio:false,video:video_option},
		function(stream){
			video.src = URL.createObjectURL(stream);
			video.play();
			Tracker = new track_set(video,ctx);
			clm.start(document.getElementById('video'));
			rendering();
		},
		function(err){
			console.log(err);
		}
	);
}

function track_set(video,ctx){
	this.ctx = ctx;
	this.video = video;
}

track_set.prototype.tracking = function(){
	this.ctx.drawImage(this.video,0,0,640,480,0,0,640,480);

	if(clm.getCurrentPosition()){
		clm.draw(document.getElementById('canvas'));
		var positions = clm.getCurrentPosition();
        if(dataCtn == 1500){
			//console.log("finished_collect_data");
			//$.ajax({
    		//	type: 'POST',
    		//	contentType: 'application/json',
    		//	url: "http://localhost:8000/save_json",
    		//	dataType : 'json',
    		//	data : JSON.stringify(tracking_data),
    		//	success : function(result) {
    		//	},error : function(result){
       		//		console.log(result);
    		//	}
			//});
				
			//dataCtn++;
		}else{
			//tracking_data[dataCtn] = positions;
			//dataCtn++;
		}
		//track_data.pos = positions;
	}
}

function rendering(){
	//if(track_switch){
	//	Tracker.tracking();
	//}
	if(clm.getCurrentPosition()){
		masPos = clm.getCurrentPosition();
	}
	if(masking_switch){
		masking();
	}
	requestAnimationFrame(rendering);
}

function masking_init(){
    var MaskImg = document.createElement("img");
	MaskImg.onload = function(){
		console.log(pModel);
		fb.load(MaskImg,masPos,pModel);
	}
	MaskImg.src = ImgURL;

	masking_switch = true;
	//track_switch = false;
}

function masking(){
	if(masPos){
		fb.draw(masPos);
	}else{
	    console.log(masPos);
	}
}

  function drawImage(img) {
    var imgW = img.width;
    var imgH = img.height;

    mtx.drawImage(img, 0, 0, imgW,imgH);


    //ctrack.reset();
    clm.init(pModel);
    clm.start(model);
  }
