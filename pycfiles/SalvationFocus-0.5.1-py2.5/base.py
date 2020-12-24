# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/lib/base.py
# Compiled at: 2008-02-28 15:45:46
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
from salvationfocus.model import Session
import salvationfocus.lib.helpers as h, salvationfocus.model as model

class BaseController(WSGIController):
    requires_auth = False

    def __before__(self):
        if self.requires_auth and 'user' not in session:
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(h.url_for(controller='login'))

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()


__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') or __name == '_'
          ]