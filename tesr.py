from flask import Flask

app = Flask(__name__)

@app.route('/')
def a():
    return '你干嘛~'
    
@app.errorhandler(404)
def b(error):
    return '你知不知道404是什么东西?'

app.run(debug=True)