# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/restin/lib/base.py
# Compiled at: 2007-05-04 19:49:10
from pylons import Response, c, g, cache, request, session
from pylons.controllers import WSGIController
from pylons.decorators import jsonify, validate
from pylons.templating import render, render_response
from pylons.helpers import abort, redirect_to, etag_cache
from pylons.i18n import N_, _, ungettext
import restin.models as restin_model, restin.lib.helpers as h, restler
RestController = restler.BaseController(restin_model)

class BaseController(WSGIController):
    __module__ = __name__


__all__ = [ __n for __n in locals().keys() if not __n.startswith('_') ]
__all__.append('_')