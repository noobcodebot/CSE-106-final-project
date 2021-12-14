 window.addEventListener("load", function () {
     var svgObject = document.getElementById('svg-campus').contentDocument; //grabs svg object from html
     let cobElement = svgObject.getElementById('cob1_path');
     let cob2Element = svgObject.getElementById('cob2_path_1');
     let cob2Element2 = svgObject.getElementById('cob2_path_2');
     let acsElement = svgObject.getElementById('acs_path');
     let adminElement = svgObject.getElementById('admin_path');
     let granElement = svgObject.getElementById('gran_path');
     let glcrElement = svgObject.getElementById('glcr_path');
     let seElement = svgObject.getElementById('se1_path_1');
     let seElement2 = svgObject.getElementById('se1_path_2');
     let se2Element = svgObject.getElementById('se2_path');
     let ssmElement = svgObject.getElementById('ssm_path_1');
     let ssmElement2 = svgObject.getElementById('ssm_path_2');
     let klElement = svgObject.getElementById('kl_path');
     let ssbElement = svgObject.getElementById('ssb_path_1');
     let sreElement = svgObject.getElementById('sre_path');


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
    granElement.onclick = function () {
        jumpToLink('building/gran/map');
    }
    glcrElement.onclick = function () {
        jumpToLink('building/glcr/map');
    }
    seElement.onclick = function () {
        jumpToLink('building/se1/map');
    }
    se2Element.onclick = function () {
        jumpToLink('building/se2/map');
    }
    seElement2.onclick = function () {
        jumpToLink('building/se1/map');
    }
    ssmElement.onclick = function () {
        jumpToLink('building/ssm/map');
    }
    ssmElement2.onclick = function () {
        jumpToLink('building/ssm/map');
    }
    klElement.onclick = function () {
        jumpToLink('building/kl/map');
    }
    ssbElement.onclick = function () {
        jumpToLink('building/ssb/map');
    }
    sreElement.onclick = function () {
        jumpToLink('building/sre/map');
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


