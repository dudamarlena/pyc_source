# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/app.py
# Compiled at: 2019-07-25 22:51:52
# Size of source mod 2**32: 156 bytes
from polecat.project import App
from .admin import *
from .models import *
from .mutations import *

class AuthApp(App):
    pass