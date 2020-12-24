# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fragmap\http.py
# Compiled at: 2019-09-05 14:04:55
# Size of source mod 2**32: 728 bytes
from http.server import BaseHTTPRequestHandler, HTTPServer

class HtmlHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path not in ('', '/'):
            self.send_response(404)
            return
        html = self.server.html_callback()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str.encode(html))


def start_server(html_callback):
    port = 0
    server = HTTPServer(('127.0.0.1', port), HtmlHandler)
    server.html_callback = html_callback

    def serve_requests():
        server.serve_forever()

    import threading
    threading.Thread(target=serve_requests).start()
    return server