# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/www/lib/base.py
# Compiled at: 2007-04-18 06:57:54
from pylons import Response, c, g, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, validate
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
from pylons.i18n import N_, _, ungettext
import econ.www.models as model, econ.www.lib.helpers as h

class BaseController(WSGIController):
    __module__ = __name__

    def __call__(self, environ, start_response):
        return WSGIController.__call__(self, environ, start_response)


__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') or __name == '_' ]