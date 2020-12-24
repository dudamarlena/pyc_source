# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/cobalt.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.pkg.core.cobalt
    ~~~~~~~~~~~~~~~~~~~~~

    Provides static content serving like mozilla's chrome:// scheme.

    :copyright: 2006 by Armin Ronacher, Georg Brandl.
    :license: GNU GPL, see LICENSE for more details.
"""
import os, time
from mimetypes import guess_type

class CobaltMiddleware(object):
    """
    The Cobalt middleware serves static files.
    """
    __module__ = __name__

    def __init__(self, app, ctx):
        self.app = app
        self.ctx = ctx

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        if path.startswith('/!cobalt/'):
            try:
                (pkgname, fname) = path[9:].split('/', 1)
                guessed_type = guess_type(fname)
                mime_type = guessed_type[0] or 'text/plain'
                imp = self.ctx.pkgmanager.importers[pkgname]
                result = imp.get_data(os.path.join('static', fname))
                expiry = time.time() + 3600
                expiry = time.asctime(time.gmtime(expiry))
                headers = [('Content-Type', mime_type), ('Cache-Control', 'public'), ('Expires', expiry)]
                start_response('200 OK', headers)
                if environ.get('REQUEST_METHOD', 'GET') == 'HEAD':
                    return []
                else:
                    return iter((result,))
            except (ValueError, KeyError, IOError):
                pass

        return self.app(environ, start_response)