import werkzeug.exceptions
from flask import Flask, request, make_response, url_for, redirect
from os.path import join
from os import listdir
from bin import md5
from time import time
from json import loads, dumps

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'file/'
#r'F:/OneDrive/qlcbs2022China/Jiang_James/OneDrive - qlcbs2022china/web_file'
files={}
for i in listdir(app.config['UPLOAD_FOLDER']):
    files[md5(i)]=i


@app.route('/')
def a():
    return app.send_static_file('index.html')


@app.route('/<path:p>')
def b(p):
    try:
        return app.send_static_file(p)
    except werkzeug.exceptions.NotFound:
        return app.send_static_file('404.html')


@app.route('/cloud/upload', methods=['POST'])
def upload():
    f = request.files['a']
    f.save(join(app.config['UPLOAD_FOLDER'], f.filename))
    return f'成功上传文件{f.filename}'


@app.route('/cloud')
def dir():
    try:
        if request.cookies['user'] in loads(open('data.json').read())['users']:
            r = ''
            for i in listdir(app.config['UPLOAD_FOLDER']):
                files[md5(i)]=i
            for i in listdir(app.config['UPLOAD_FOLDER']):
                r += f"<a href='/dl?sign={md5(i)}'>{i}</a><br>"
            return r
        else:
            return redirect('/cloud/ua')
    except:
        return redirect('/cloud/ua')


@app.route('/cloud/dl', methods=['GET'])
def dl():
    return redirect(url_for('test', name=files[request.args['sign']], sign=md5(int(time()))))


@app.route('/cloud/dl/<sign>/<name>')
def test(name, sign):
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
                return app.send_static_file('l.htm')
        except:
            return app.send_static_file('l.htm')
    else:
        d =loads(request.data)
        print(d)
        u = loads(open('data.json').read())['users']
        if d['type'] == 'login':
            if d['user'] in u and d['pwd']==u[d['user']]:
                r = make_response('login success')
                r.set_cookie('user',d['user'])
                return r
            else:
                return 'user or password error'
        else:
            return 'error'


app.run("0.0.0.0", 80)
