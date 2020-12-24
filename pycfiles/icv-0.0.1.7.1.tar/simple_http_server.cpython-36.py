# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/core/http/server/simple_http_server.py
# Compiled at: 2019-05-11 08:32:01
# Size of source mod 2**32: 742 bytes
try:
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
except ImportError:
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class IcvServer(object):

    def __init__(self, host='0.0.0.0', port=9527):
        self.host = host
        self.port = port
        self.server = None
        self.handler = IcvServer

    def run(self, handler_class):
        self.server = ThreadingSimpleServer((self.host, self.port), handler_class)
        self.server.serve_forever()