# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kushalkatta/workspace/Electron/SmartMirror/smart_mirror/smart_mirror/__init__.py
# Compiled at: 2018-09-14 05:22:22
# Size of source mod 2**32: 144 bytes
from flask import Flask
from flask_socketio import SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)