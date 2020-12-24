# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/applications/emulate_simplecast.py
# Compiled at: 2009-05-11 19:02:38
"""
Emulate a simplecast webserver
"""
import time, os, BaseHTTPServer, socket
HOST_NAME = socket.gethostname()
PORT_NUMBER = 8181

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header('Content-type', 'text/plain')
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header('Content-type', 'text/plain')
        s.end_headers()
        s.wfile.write('ok ')


def main():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER)


if __name__ == '__main__':
    main()