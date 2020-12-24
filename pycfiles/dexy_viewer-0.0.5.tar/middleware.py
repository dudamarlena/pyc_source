# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ana/dev/dexy-viewer/dexy_viewer/middleware.py
# Compiled at: 2013-08-03 02:31:40
import web, os

class CustomStaticApp(web.httpserver.StaticApp):

    def translate_path(self, path):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), path.lstrip('/'))


import posixpath, urllib

class StaticMiddleware:
    """WSGI middleware for serving static files."""

    def __init__(self, app, prefix='/static/'):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        path = self.normpath(path)
        if path.startswith(self.prefix):
            return CustomStaticApp(environ, start_response)
        else:
            return self.app(environ, start_response)

    def normpath(self, path):
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith('/'):
            path2 += '/'
        return path2