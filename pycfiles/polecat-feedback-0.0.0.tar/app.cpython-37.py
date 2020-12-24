# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/app.py
# Compiled at: 2019-07-25 22:51:52
# Size of source mod 2**32: 156 bytes
from polecat.project import App
from .admin import *
from .models import *
from .mutations import *

class AuthApp(App):
    pass