# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/server/tornado_.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 901 bytes
from __future__ import unicode_literals, print_function
try:
    import tornado.ioloop, tornado.httpserver, tornado.wsgi
except ImportError:
    print("You must install the 'tornado' package.")
    raise
else:

    def serve(application, host='127.0.0.1', port=8080, **options):
        """Tornado's HTTPServer.
        
        This is a high quality asynchronous server with many options.  For details, please visit:
        
                http://www.tornadoweb.org/en/stable/httpserver.html#http-server
        """
        container = tornado.wsgi.WSGIContainer(application)
        http_server = (tornado.httpserver.HTTPServer)(container, **options)
        http_server.listen(int(port), host)
        tornado.ioloop.IOLoop.instance().start()