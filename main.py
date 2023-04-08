import werkzeug.exceptions
from flask import Flask, request, make_response, url_for, redirect, render_template
from os.path import join
from bin import md5
from time import time
from json import loads, dumps

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'F:\OneDrive\qlcbs2022China\Jiang_James\OneDrive - qlcbs2022china\web_file'



@app.route('/')
def a():
    return app.send_static_file('index.html')


@app.route('/<path:p>')
def b(p):
    return app.send_static_file(p)


@app.route('/cloud/upload', methods=['POST', 'GET'])
def upload():
    try:
        c = loads(open('data.json').read())
        if request.cookies['user'] in c['users']:
            if request.method == 'GET':
                 return app.send_static_file('upload.html')
            else:
                n = {'0':'','1':''}
                f = request.files
                for i in f:
                    f[i].save(join(app.config['UPLOAD_FOLDER'], f[i].filename))
                    c['users'][request.cookies['user']][1][md5(f[i].filename)] = f[i].filename
                    n['0'] += f'{md5(f[i].filename)},\n'
                    n['1'] += f'{f[i].filename},\n'
                open('data.json', 'w').write(dumps(c))
                return f'success upload!\nfile name:{n["1"]}md5:{n["0"]}'
        else:
            return redirect('/cloud/ua')
    except KeyError:
        return redirect('/cloud/ua')


@app.route('/cloud/')
def dir():
    try:
        if request.cookies['user'] in loads(open('data.json').read())['users']:
            d = loads(open('data.json').read())['users'][request.cookies['user']][1]
            return render_template('files.htm', result=d)
        else:
            return redirect('/cloud/ua')
    except KeyError:
        return redirect('/cloud/ua')


@app.route('/cloud/dl', methods=['GET'])
def dl():
    try:
        d = loads(open('data.json').read())['users']
        if request.cookies['user'] in d:
            if request.args['sign'] in d[request.cookies['user']][1]:
                return redirect(url_for('test', name=d[request.cookies['user']][1][request.args['sign']], sign=md5(int(time()))))
            else:
                return "error:You don't have this file!"
    finally:
        redirect('/cloud/ua')


@app.route('/cloud/dl/<sign>/<name>')
def dl2(name, sign):
    if md5(int(time())) == sign:
        r = make_response(open(f'file/{name}', 'rb').read())
        r.headers['Content-Type'] = 'byte/file'
        return r
    return 'time error!'


@app.route('/cloud/ua', methods=['POST', 'GET'])
def ua():
    if request.method == 'GET':
        try:
            if request.cookies['user'] in loads(open('data.json').read())['users']:
                return redirect('/cloud')
            else:
                return app.send_static_file('ua.htm')
        except:
            return app.send_static_file('ua.htm')
    else:
        d =loads(request.data)
        print(d)
        u = loads(open('data.json').read())
        if d['type'] == 'login':
            if d['user'] in u['users'] and d['pwd']==u['users'][d['user']][0]:
                r = make_response('login success')
                r.set_cookie('user',d['user'],expires=int(time())+174800)
                return r
            else:
                return 'user or password error'
        elif d['type'] == 'reg':
            if d['user'] in u['users']:
                return 'had same user'
            else:
                u['users'][d['user']]=[d['pwd'], {}]
                open('data.json', 'w').write(dumps(u))
                return 'success register'
        else:
            return 'type error'


@app.errorhandler(404)
def _404(error):
    return f"<h1 style='color: red;text-align:center'>这里什么也没有,你来错了-v-</h1>"


@app.errorhandler(500)
def _500(error):
    return f"<h1 style='color: red;text-align:center'>哦豁,屑程序员的代码有bug!!!</h1>"

@app.errorhandler(403)
def _403(error):
    return f"<h1 style='color: red;text-align:center'>你的权限跑哪去了?等你的权限拿到再来看看我吧...</h1>"


@app.errorhandler(400)
def _400(error):
    return f"<h1 style='color: red;text-align:center'>哦豁,屑程序员的代码有bug!!!</h1>"


app.run("0.0.0.0", 80)
