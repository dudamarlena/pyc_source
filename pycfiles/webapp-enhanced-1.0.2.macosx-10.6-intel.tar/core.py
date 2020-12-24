# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/static/controllers/core.py
# Compiled at: 2014-04-11 19:16:24
from lib import server

class ParentController(server.BaseController):
    pass


class Controller(server.Controller, ParentController):
    pass


class ModelController(server.ModelController, ParentController):
    pass


class AJAXController(server.AJAXController, ParentController):
    pass