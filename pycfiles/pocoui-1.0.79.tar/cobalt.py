# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/cobalt.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = "\n    pocoo.pkg.core.cobalt\n    ~~~~~~~~~~~~~~~~~~~~~\n\n    Provides static content serving like mozilla's chrome:// scheme.\n\n    :copyright: 2006 by Armin Ronacher, Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n"
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