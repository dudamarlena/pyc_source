# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/log/bin/release/sudosh/app/__init__.py
# Compiled at: 2014-06-03 11:14:08
import os
from flask import Flask
from flask_login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from config import basedir
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lms = LoginManager()
lms.init_app(app)
CsrfProtect(app)
lms.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app import views, models