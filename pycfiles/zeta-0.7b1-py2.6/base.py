# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/base.py
# Compiled at: 2010-01-24 10:23:28
"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from zeta.model import meta

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()