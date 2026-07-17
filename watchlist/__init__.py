from flask import Flask
from sqlalchemy import select
from watchlist.extensions import db, login_manager
from watchlist.blueprints.main import main_bp
from watchlist.blueprints.auth import auth_bp
from watchlist.models import User
from watchlist.errors import register_errors
from watchlist.commands import register_commands
from watchlist.settings import config


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝本
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # 注册错误处理
    register_errors(app)

    # 注册自定义命令
    register_commands(app)

    # 模板上下文处理器
    @app.context_processor
    def inject_user():
        user = db.session.execute(select(User)).scalar()
        return dict(user=user)

    return app
