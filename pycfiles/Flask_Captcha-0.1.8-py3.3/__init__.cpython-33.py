# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_captcha/__init__.py
# Compiled at: 2014-06-13 14:59:52
# Size of source mod 2**32: 685 bytes
import re
from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.captcha.models import db, CaptchaStore, CaptchaSequence
VERSION = (0, 1, 8)

class Captcha(object):
    ext_db = None

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        with app.app_context():
            self.ext_db = current_app.extensions['sqlalchemy'].db
            active_metadata = self.ext_db.metadata
            CaptchaStore.__table__ = CaptchaStore.__table__.tometadata(active_metadata)
            CaptchaSequence.__table__ = CaptchaSequence.__table__.tometadata(active_metadata)