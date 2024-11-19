document.getElementById("volume-input").addEventListener("input", updateVol, false);
document.getElementById("file-input").addEventListener("change", updateFile, false);

let volume = 50
let ringType = 1
let reset = 0

function updateVol(){
	document.getElementById("volume-output").innerHTML = this.value;
	volume = this.value;
}

let file = null
function updateFile() {
	if(this.files[0].size<=409600) {
		file = this.files[0]
	}
	else {
		alert("File size can be at maximum 400kb")
	}
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
    if (file != null) {
        await fetch('/upload', {
         method: 'POST',
         body: file,
         headers: {
           'Content-Type': 'application/octet-stream',
           'Content-Disposition': `attachment; filename="${file.name}"`,
         },
        }).then(res => {
           alert("File uploaded successfully")
        });
    }
    
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
