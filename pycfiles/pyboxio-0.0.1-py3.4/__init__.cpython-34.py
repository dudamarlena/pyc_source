# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\app\__init__.py
# Compiled at: 2015-08-19 16:40:45
# Size of source mod 2**32: 923 bytes
r"""app\__init__.py: This file initializes the Flask app."""
__author__ = 'dan'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)
    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')
    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    return app