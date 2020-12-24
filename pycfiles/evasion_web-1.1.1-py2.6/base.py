# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\nmdev\src\branches\loyalty\evasion-web\evasion\web\lib\base.py
# Compiled at: 2010-05-18 09:51:54
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        return WSGIController.__call__(self, environ, start_response)