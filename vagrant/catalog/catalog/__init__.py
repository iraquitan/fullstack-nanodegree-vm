# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * Project: catalog
 * Author name: Iraquitan Cordeiro Filho
 * Author login: pma007
 * File: __init__.py
 * Date: 2/23/16
 * Time: 14:38
 * To change this templates use File | Settings | File Templates.
"""
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)

if app.debug:
    log_file_handler = RotatingFileHandler(
        '../catalog/basic-logging.txt',
        maxBytes=10000, backupCount=0)
    app.logger.addHandler(log_file_handler)
from catalog.views import home
from catalog.models import User

app.jinja_env.globals['csrf_token'] = home.generate_csrf_token

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == user_id).first()
