# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/flask-bluelogin/flask_bluelogin/__init__.py
# Compiled at: 2017-09-02 06:35:17
"""
    Module flask_bluelogin
"""
__version_info__ = (0, 2, 7)
__version__ = ('.').join([ str(val) for val in __version_info__ ])
__namepkg__ = 'flask-bluelogin'
__desc__ = 'Flask BlueLogin module'
__urlpkg__ = 'https://github.com/fraoustin/flask-bluelogin.git'
__entry_points__ = {}
from flask_bluelogin.main import BlueLogin
from flask_bluelogin.models.user import User
from flask_bluelogin.models.users import Users
from flask_bluelogin.util import check_login