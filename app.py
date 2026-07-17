from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return 'Welcome to My Watchlist!'

@app.route('/user/<name>')
def user(name):
    return f'Hello, {escape(name)}!'   # 使用 escape 防止 XSS 攻击（更安全）

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user', name='greyli'))
    print(url_for('user', name='peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'
