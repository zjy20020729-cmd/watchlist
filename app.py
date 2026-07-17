from flask import Flask, render_template, url_for
from markupsafe import escape

app = Flask(__name__)

# ----- 虚拟数据 -----
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

# ----- 主页路由 -----
@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)

# ----- 其他可选路由（可以保留，但为了聚焦，可暂时注释）-----
# 如果你还想保留之前测试的 /user/<name> 和 /test，可以保留，但建议先注释掉避免干扰
# @app.route('/user/<name>')
# def user(name):
#     return f'Hello, {escape(name)}!'

# @app.route('/test')
# def test_url_for():
#     print(url_for('index'))   # 注意这里改为 index
#     return 'Test page'
