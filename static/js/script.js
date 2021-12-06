function jumpToLink(endpoint) {
    const url = "http://127.0.0.1:5000/"+endpoint;
    window.open(url, "_self");
}

function loadClassMap(id) {
    const url = "http://127.0.0.1:5000/class/"+id+"/map";
        window.open(url, "_self");
}