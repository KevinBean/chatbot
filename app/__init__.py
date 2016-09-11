# -*- coding=utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# login_view 属性设置登录页面 的端点。回忆一下,登录路由在蓝本中定义,因此要在前面加上蓝本的名字。


def create_app(config_name):
    app = Flask(__name__) # Flask 类的构造函数只有一个必须指定的参数,即程序主模块或包的名字。在大多数程序 中, Python 的 __name__ 变量就是所需的值。
    app.config.from_object(config[config_name])
    # 配置类在 config.py 文件中定义,其中保存 的配置可以使用 Flask app.config 配置对象提供的 from_object() 方法直接导入程序。
    # 至 于配置对象, 则可以通过名字从 config 字典中选择。
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # 注册蓝本时使用的 url_prefix 是可选参数。 如果使用了这个参数, 注册后蓝本中定义的 所有路由都会加上指定的前缀, 即这个例子中的 /auth。
    #  例如, /login 路由会注册成 /auth/ login, 在开发 Web 服务器中,完整的 URL 就变成了 http://localhost:5000/auth/login。

    return app
