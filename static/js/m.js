function login(){
    u = document.getElementById('user').value;
    p = document.getElementById('pwd').value;
    if (u === ''){
        alert('请输入用户名');
    }else if(p ===''){
        alert('请输入密码');
    }else{
        send_data('/api/ua', 'POST', true, {'type':'login','id':u,'pwd':p},function(ev){
            alert(ev);
            location.reload();
        });
    }
}
function reg(){
    u = document.getElementById('ruser').value;
    p = document.getElementById('rpwd').value;
    if (u === ''){
        alert('请输入用户名');
    }else if(p ===''){
        alert('请输入密码');
    }else if(p != document.getElementById('rep').value){
        alert('密码不一致');
    }else{
        send_data('/api/ua', 'POST', true, {'type':'reg','name':u,'pwd':p},function(ev){
            alert(ev);
        });
    }
}
