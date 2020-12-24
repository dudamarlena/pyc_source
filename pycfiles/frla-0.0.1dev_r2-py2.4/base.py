# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/lib/base.py
# Compiled at: 2008-09-22 06:43:33
"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render
import frla.lib.helpers as h, frla.model as model

class BaseController(WSGIController):
    __module__ = __name__

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        return WSGIController.__call__(self, environ, start_response)


__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') or __name == '_' ]