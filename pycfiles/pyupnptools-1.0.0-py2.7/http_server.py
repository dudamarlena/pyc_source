# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyupnptools/http_server.py
# Compiled at: 2018-09-02 07:07:26
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except:
    from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import SocketServer
except:
    import socketserver as SocketServer

import logging, traceback
logger = logging.getLogger(__name__)

class _S(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        try:
            _x = BaseHTTPRequestHandler.__mro__
            super(_S, self).__init__(*args, **kwargs)
        except AttributeError:
            BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            raise e

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_NOTIFY(self):
        length = int(self.headers['Content-Length'])
        xml = self.rfile.read(length)
        if self.server._handler:
            self.server._handler('NOTIFY', self.path, xml)
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write('<html><body><h1>get</h1></body></html>')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write('<html><body><h1>post</h1></body></html>')


class HttpServer:

    def __init__(self, port):
        addr = (
         '', port)
        self._httpd = HTTPServer(addr, _S)
        self._httpd._handler = None
        return

    def get_server_address(self):
        return self._httpd.server_address

    def register(self, handler):
        self._httpd._handler = handler

    def run(self):
        try:
            self._httpd.serve_forever()
        except Exception as e:
            logger.error(e)

    def finish(self):
        self._httpd.server_close()