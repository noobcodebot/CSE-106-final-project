 window.addEventListener("load", function () {
     var svgObject = document.getElementById('svg-campus').contentDocument; //grabs svg object from html
    let cobElement = svgObject.getElementById('cob1_path');
    let cob2Element = svgObject.getElementById('cob2_path_1');
    let cob2Element2 = svgObject.getElementById('cob2_path_2');
    let acsElement = svgObject.getElementById('acs_path');
    let adminElement = svgObject.getElementById('admin_path')

    cobElement.onclick = function () {
        jumpToLink('building/cob1/map');
    }
    cob2Element.onclick = function () {
        jumpToLink('building/cob2/map');
    }
    cob2Element2.onclick = function () {
        jumpToLink('building/cob2/map');
    }
    acsElement.onclick = function () {
        jumpToLink('building/acs/map');
    }
    adminElement.onclick = function () {
        jumpToLink('building/admin/map'); //remember #ffff99 is the color of the classrooms for svg edit later
    }
 })
function jumpToLink(endpoint) {
    const url = "http://127.0.0.1:5000/"+endpoint;
    window.open(url, "_self");
}

function loadClassMap(id) {
    const url = "http://127.0.0.1:5000/class/"+id+"/map";
    window.open(url, "_self");
}


