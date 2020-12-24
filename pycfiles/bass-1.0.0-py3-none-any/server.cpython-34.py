# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bass/server.py
# Compiled at: 2015-09-11 15:14:22
# Size of source mod 2**32: 2833 bytes
"""
bass.server
-----
Simple web server for development and test purposes.
"""
import logging, os
from datetime import datetime
from .site import rebuild_site
from . import setting
try:
    from webob import Request, Response
    from webob.static import DirectoryApp

    class Monitor:
        __doc__ = 'class for generating WSGI middleware handler'

        def __init__(self, app, checklist, callback):
            self.wrapped = app
            self.timestamp = datetime.now()
            self.checklist = checklist
            self.callback = callback

        def changed(self):
            """return True if any file in one of the directories in self.checklist has changed
               since self.timestamp, otherwise False"""
            for checkdir in self.checklist:
                for dirpath, _, filenames in os.walk(checkdir):
                    for f in filenames:
                        path = os.path.join(dirpath, f)
                        if datetime.fromtimestamp(os.path.getmtime(path)) > self.timestamp:
                            logging.debug('%s has changed', path)
                            return True

            return False

        def __call__(self, environ, start_response):
            """this __call__ method turns an instance into a WSGI middleware handler"""
            request = Request(environ)
            if request.path.endswith('.html'):
                if self.changed():
                    logging.debug('Rebuilding site')
                    self.timestamp = datetime.now()
                    self.callback()
            response = request.get_response(self.wrapped)
            return response(environ, start_response)


    try:
        from waitress import serve
    except ImportError:
        from wsgiref.simple_server import make_server

        def serve(app, host, port):
            """serve: WSGI server with same interface as waitress.serve"""
            server = make_server(host, port, app)
            server.serve_forever()


    def http_server(host, port):
        """http_server: WSGI-based web server with same interface as in standard library"""
        static = DirectoryApp(setting.output, index_page=None)
        wrapped = Monitor(static, checklist=[setting.input, setting.layout], callback=rebuild_site)
        logging.debug('Starting HTTP server on port %d', port)
        serve(wrapped, host=host, port=port)


except ImportError:
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    def http_server(host, port):
        """http_server: basic web server based on standard library"""
        os.chdir(setting.output)
        httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
        logging.debug('Starting HTTP server on port %d', port)
        httpd.serve_forever()