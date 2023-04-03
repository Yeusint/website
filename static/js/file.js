function fs(){
f = document.getElementById('m').files[0];
if(f){
    var fs_;
    if (f.size > 1024 * 1024){
        fs_ = (Math.round(f.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
    }else{
        fs_ = (Math.round(f.size * 100 / 1024) / 100).toString() + 'KB';
    }
    document.getElementById('t').innerText = '大小: '+fs_;
}
}
function sub(){
    f = document.getElementById('m').files[0];
    if(f){
        fd = new FormData();
        fd.append('a', f);
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', function(ev){
            if(ev.lengthComputable){
                document.getElementById('ts').innerHTML = Math.round(ev.loaded * 100/ev.total).toString()+'%';
            }
        }, false);
        xhr.addEventListener('load', function(ev){
            alert(ev.target.responseText);
        }, false);
        xhr.open('POST', '/upload');
        xhr.send(fd);
    }else{
        alert('未选择文件！');
    }
}