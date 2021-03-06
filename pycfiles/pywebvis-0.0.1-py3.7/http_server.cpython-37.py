# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webvis/http_server.py
# Compiled at: 2019-11-05 21:15:15
# Size of source mod 2**32: 2093 bytes
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import requests, webvis
from pathlib import Path
path = webvis.__file__
print('path', path)
p = Path(path)
pywebvis_path = p.parent.parent.parent / 'web'

def get_path(path):
    if path in ('/', ''):
        path = './index.html'
    return str(pywebvis_path) + '/dist' + path


def fetch_addr(addr):
    r = requests.get(addr)
    return r.text


def stop():
    print('Stopping http not yet implemented')


def read_file(fname):
    with open(fname, 'rb') as (f):
        page = f.read()
    return page


class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        query = urlparse(self.path).path
        print('Client requested path', query)
        self._set_headers()
        try:
            path = get_path(query)
            try:
                page = read_file(path)
            except:
                page = read_file(get_path('/index.html'))

            self.wfile.write(page)
        except Exception as e:
            try:
                self.wfile.write(bytes(str(e), 'utf-8'))
            finally:
                e = None
                del e

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write('<html><body><h1>POST!</h1></body></html>')


def run(server_class=HTTPServer, handler_class=Server, port=80):
    global httpd
    server_address = ('', port)
    print('Starting http at', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def start_server(port):
    run(port=port)


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        run(port=(int(argv[1])))
    else:
        run()