# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattpease/DevTools/Workspaces/flask-spawn/flaskspawn/cookiecutters/small/{{cookiecutter.repo_name}}/application/views.py
# Compiled at: 2015-07-03 15:00:14
from application import app

@app.route('/health')
def check_status():
    return 'Status OK'