# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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