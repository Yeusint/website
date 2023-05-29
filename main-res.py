from flask import (
    Flask,
    request,
    make_response,
    url_for,
    redirect,
    render_template,
    session,
)
from bin import file
import os, json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

#不要改我的代码

limiter = Limiter(key_func=get_remote_address, app=app)  # 根据访问者的IP记录访问次数


PATH = os.path.join(os.path.dirname(__file__), "file")
userfile = file.file(PATH)


@app.route("/")
def a():return app.send_static_file("index.html")


@app.route("/api/listdir", methods=["POST"])  # 以json返回文件夹下的所有文件，需要传入文件地址相对值
@limiter.limit("2/second")
def listdir():return userfile.listdir(str(request.data))


@app.route("/cloud/")
def name():#返回网盘的页面，一切显示文件夹的任务，都有前端直接访问后端接口完成，此接口只负责返回网页，别改我的代码！
    try:
        request.cookies["id"]
        return app.send_static_file('cloud.html')#此网页没有写
    except:
        return app.send_static_file("ua.html")
    

@app.route('/api/ua', methods=['POST'])#登录或注册的接口，只能通过post访问
@limiter.limit("1/second")
def ua_api():
    d =json.loads(request.data)
    u = json.loads(open('data.json').read())
    if d['type'] == 'login':
        if d['id'] in list(u) and d['pwd']==u[d['id']]["pwd"]:
            r = make_response('login success')
            r.set_cookie('id',d['id'],max_age=60*60*1)
            return r
        else:
            return 'user or password error'
    elif d['type'] == 'reg':
        try:
            id = (int(list(u.keys())[-1]) + 1)
        except:
            id = 1
        u[id]={"name":d['name'],"pwd":d['pwd']}
        open('data.json', 'w').write(json.dumps(u))
        os.makedirs(os.path.join(PATH,str(id)))
        return str(id)
        
    return 'error'


@app.route("/api/upload", methods=["POST"])  # 上传文件
@limiter.limit("2/second")
def upload_api():
    try:
        c = json.loads(open("data.json").read())
        if request.cookies["id"] in c:
            f = request.files
            for i in f:
                path = os.path.join(PATH,request.cookies["id"], f[i].filename)
                f[i].save(path)#存在个人的文件夹
            return '["type":"ok","path":'+request.cookies["id"] + "/" + f[i].filename+']'
        else:
            return '["type":"userError"]'
    except KeyError:
        return '["type":"error"]'


@app.route("/cloud/upload", methods=["GET"])#上传的页面
def upload():
    try:
        request.cookies["id"]
        return app.send_static_file('upload.html')
    except:
        return app.send_static_file("ua.html")


@app.route("/<path:p>")
def b(p):return app.send_static_file(p)


@app.route("/favicon.ico")
def icon():return app.send_static_file("pic/favicon.ico")


@app.errorhandler(404)
def _404(error):return f"<h1 style='color: red;text-align:center'>404这里什么也没有,你来错了-v-</h1>"


@app.errorhandler(500)
def _500(error):return f"<h1 style='color: red;text-align:center'>500哦豁,屑程序员的代码有bug!!!</h1>"


@app.errorhandler(403)
def _403(error):return f"<h1 style='color: red;text-align:center'>403你的权限跑哪去了?等你的权限拿到再来看看我吧...</h1>"


@app.errorhandler(400)
def _400(error):return f"<h1 style='color: red;text-align:center'>400哦豁,屑程序员的代码有bug!!!</h1>"


app.run("0.0.0.0", 80)
