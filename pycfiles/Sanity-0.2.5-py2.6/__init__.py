# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sanity/__init__.py
# Compiled at: 2010-06-27 15:14:05
"""
    Sanity
    ~~~~~~

    A quick and simple task manager built for teams in an intranet setting.
    It's very simple to use by just about anyone on a team.

    :copyright: (c) 2010 by Aaron Toth.
    :license: Apache License 2.0, see LICENSE for more details.
"""
from flask import Flask, g, session, redirect, url_for, request
from flaskext.sqlalchemy import SQLAlchemy
from sanity import config
app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_RECYCLE'] = 7200
db = SQLAlchemy(app)
from sanity.models import User

@app.before_request
def lookup_current_user():
    g.user = None
    if 'name' in session:
        g.user = User.query.filter_by(name=session['name']).first()
    return


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1', 'servererror@example.com', config.ADMINS, 'Sanity Failure')
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter('\n        Message type:       %(levelname)s\n        Location:           %(pathname)s:%(lineno)d\n        Module:             %(module)s\n        Function:           %(funcName)s\n        Time:               %(asctime)s\n\n        Message:\n\n        %(message)s\n    '))
    app.logger.addHandler(mail_handler)
from sanity.views.frontend import frontend
from sanity.views.admin import admin
from sanity.views.user import user
app.register_module(frontend)
app.register_module(admin, url_prefix='/admin')
app.register_module(user, url_prefix='/user')