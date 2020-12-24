# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/situation/situation/debug_app.py
# Compiled at: 2017-11-29 20:22:10
# Size of source mod 2**32: 682 bytes
from flask_diamond import Diamond, db
import os, json

class DebugApp(Diamond):
    pass


def create_app():
    application = DebugApp()
    application.facet('configuration')
    application.facet('logs')
    application.facet('database')
    application.facet('marshalling')
    return application.app


def reset_db():
    db.drop_all()
    db.create_all()


def quick():
    tmp_settings()
    app = create_app()
    reset_db()
    return app


def tmp_settings():
    os.environ['SETTINGS_JSON'] = json.dumps({'LOG':'/tmp/out.log', 
     'SQLALCHEMY_DATABASE_URI':'sqlite:////tmp/dev.db'})