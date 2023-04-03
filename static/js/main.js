function send_data(path, method="get",async, data, back) {
    var xmlhttp;
	if (window.XMLHttpRequest){
	    xmlhttp=new XMLHttpRequest();
	}
	else{
	    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
    xmlhttp.onreadystatechange = function(){
	    if (xmlhttp.readyState===4 && xmlhttp.status===200){
	    	back(xmlhttp.responseText);
	    }else if(xmlhttp.readyState===4 && (xmlhttp.status===404 || xmlhttp.status===500 || xmlhttp.status===400)){
            back({"type":"server_status","text":"failed"});
        }
	}
	xmlhttp.open(method,path,async);
    xmlhttp.send(JSON.stringify(data));
}