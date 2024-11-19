let ffmpeg = null

/*function setFFMPEG() {
	alert("dooooo");
	let ffmpeg = require("static/ffmpeg-webm.js.gz");
}*/

document.getElementById("volume-input").addEventListener("input", updateVol, false);

let volume = 50
let ringType = 1
let reset = 0

function updateVol(){
	document.getElementById("volume-output").innerHTML = this.value;
	volume = this.value;
}

function updatePattern1(){
	ringType = 1;
}

function updatePattern2(){
	ringType = 2;
}

function submit() {
	console.log("sent it");
	sendit();
}

function resett() {
	reset = 1;
	sendit();
}

async function sendit(){
	
    const response = await fetch("/update", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: '{"volume":'+volume.toString()+',"pattern":'+ringType.toString()+',"reset":'+reset.toString()+'}',
    });
    //console.log("{'volume':"+volume.toString()+",'pattern':"+ringType.toString()+",'reset':"+reset.toString()+"}")
    const data = await response.json();
    alert(data.message);
    if (data.success) window.location.href = "/";
    return data;
}
