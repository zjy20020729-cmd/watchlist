from flask import Flask, render_template, url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import click
from pathlib import Path
import sys

# ----- 数据库配置 -----
class Base(DeclarativeBase):
    pass

SQLITE_PREFIX = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PREFIX + str(Path(app.root_path) / 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭追踪修改（提高性能）

db = SQLAlchemy(app, model_class=Base)

# ----- 数据库模型 -----
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

class Movie(db.Model):
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    year: Mapped[str] = mapped_column(String(4))

# ----- 自定义命令：初始化数据库 -----
@app.cli.command('init-db')
@click.option('--drop', is_flag=True, help='Create after drop.')
def init_database(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

# ----- 自定义命令：生成虚拟数据 -----
@app.cli.command('forge')
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()

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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

# ----- 主页路由（读取数据库） -----
@app.context_processor
def inject_user():
    user = db.session.execute(select(User)).scalar()
    return dict(user=user)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    user = db.session.execute(select(User)).scalar()
    movies = db.session.execute(select(Movie)).scalars().all()
    return render_template('index.html', user=user, movies=movies)

# ----- 其他路由（可选） -----
@app.route('/user/<name>')
def user(name):
    return f'Hello, {escape(name)}!'

@app.route('/test')
def test_url_for():
    print(url_for('index'))
    return 'Test page'
