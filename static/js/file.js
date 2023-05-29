function fs(){
f = document.getElementById('m').files;
document.getElementById('upload').innerHTML = "<tr><th name='name'>文件名</th><th>大小</th><th>类型</th></tr>"
if(f){
    var fs_;
    for(i=0;i<f.length;i++){
        if (f[i].size > 1024 * 1024){
            fs_ = (Math.round(f[i].size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
        }else{
            fs_ = (Math.round(f[i].size * 100 / 1024) / 100).toString() + 'KB';
        }
        document.getElementById('upload').innerHTML = document.getElementById('upload').innerHTML+"<tr><td>"+f[i].name+"</td><td>"+fs_+"</td><td>"+f[i].type+"</td></tr>";
    }
}
}
function sub(){
    f = document.getElementById('m').files;
    if(f){
        fd = new FormData();
        for (i=0;i<f.length;i++){
            fd.append(i.toString(), f[i]);
        }
        xhr = new XMLHttpRequest();
        xhr.upload.addEventListener('progress', function(ev){
            if(ev.lengthComputable){
                document.getElementById('ts').innerHTML = "传输进度: "+ Math.round(ev.loaded * 100/ev.total).toString()+'%';
            }
        }, false);
        xhr.addEventListener('load', function(ev){
            alert(ev.target.responseText);
        }, false);
        xhr.open('POST', '/api/upload');
        xhr.send(fd);
    }else{
        alert('未选择文件！');
    }
}