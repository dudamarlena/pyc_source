# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/maharishi/lib/base.py
# Compiled at: 2006-08-30 12:30:23
from pylons import Response, c, g, h, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, rest, validate
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
import maharishi.models as model

class BaseController(WSGIController):
    __module__ = __name__

    def __call__(self, environ, start_response):
        return WSGIController.__call__(self, environ, start_response)