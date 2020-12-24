# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/tawhiri/manager.py
# Compiled at: 2016-11-26 12:39:04
# Size of source mod 2**32: 1463 bytes
"""
Command-line manager for API webapp

"""
import os
from flask import send_file, send_from_directory, redirect, url_for
from flask.ext.script import Manager
from .api import app
manager = Manager(app)

def main():
    if 'TAWHIRI_SETTINGS' in os.environ:
        app.config.from_envvar('TAWHIRI_SETTINGS')
    ui_dir = app.config.get('UI_DIR')
    if ui_dir is not None:

        @app.route('/ui/<path:path>')
        def send_ui(path):
            return send_from_directory(ui_dir, path)

        @app.route('/ui/')
        def send_index():
            return send_file(os.path.join(ui_dir, 'index.html'))

        @app.route('/')
        def send_ui_redirect():
            return redirect(url_for('send_index'))

    return manager.run()