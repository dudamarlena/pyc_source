# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/gateway/gatewayhandler.py
# Compiled at: 2009-05-11 19:02:38
import BaseHTTPServer

class gatewayhandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header('Content-type', 'text/plain')
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        request_string = s.raw_requestline
        s.send_response(200)
        s.send_header('Content-type', 'text/plain')
        s.end_headers()
        s.wfile.write('ok ')