 window.addEventListener("load", function () {
     var svgObject = document.getElementById('svg-campus').contentDocument;
     var svg = svgObject.getElementById('cob1_path');
     svg.onclick = function(){
         let endpoint = "/class/1/map"
        jumpToLink(endpoint);
     };
 })
function jumpToLink(endpoint) {
    const url = "http://127.0.0.1:5000/"+endpoint;
    window.open(url, "_self");
}

function loadClassMap(id) {
    const url = "http://127.0.0.1:5000/class/"+id+"/map";
    window.open(url, "_self");
}


