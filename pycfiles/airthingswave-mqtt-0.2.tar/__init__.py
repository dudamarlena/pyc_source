# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\administrator\pycharmprojects\airtest_for_h9\airtest\webgui\__init__.py
# Compiled at: 2014-12-03 20:37:50
import os, flask
app = flask.Flask(__name__)
app.config['DEBUG'] = True
from .routers import home, api
app.register_blueprint(home.bp, url_prefix='')
app.register_blueprint(api.bp, url_prefix='/api')
serve = app.run
if __name__ == '__main__':
    serve()