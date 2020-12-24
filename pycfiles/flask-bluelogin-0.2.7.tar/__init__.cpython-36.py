# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-bluelogin/flask_bluelogin/__init__.py
# Compiled at: 2017-04-30 08:17:16
# Size of source mod 2**32: 382 bytes
"""
    Module flask_bluelogin
"""
__version_info__ = (0, 1, 1)
__version__ = '.'.join([str(val) for val in __version_info__])
__namepkg__ = 'flask-bluelogin'
__desc__ = 'Flask BlueLogin module'
__urlpkg__ = 'https://github.com/fraoustin/flask-bluelogin.git'
__entry_points__ = {}
from flask_bluelogin.main import *