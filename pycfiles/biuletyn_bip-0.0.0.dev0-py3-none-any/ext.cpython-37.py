# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jarek/work/bip/src/bip/ext.py
# Compiled at: 2019-09-03 16:37:30
# Size of source mod 2**32: 449 bytes
from authlib.flask.client import OAuth
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from utils.db import Model
db = SQLAlchemy(model_class=Model)
babel = Babel(default_locale='pl', default_timezone='Europe/Warsaw')
oauth = OAuth()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap()