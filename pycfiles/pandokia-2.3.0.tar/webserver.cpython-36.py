# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/webserver.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 3150 bytes
import os
try:
    from http.server import CGIHTTPRequestHandler, HTTPServer
except ImportError:
    from CGIHTTPServer import CGIHTTPRequestHandler
    from BaseHTTPServer import HTTPServer

class my_handler(CGIHTTPRequestHandler):
    cgi_directories = [
     '/cgi-bin/']

    def __init__(self, request, client_address, server):
        CGIHTTPRequestHandler.__init__(self, request, client_address, server)

    def is_cgi(self):
        l = self.path.split('?', 1)
        if l[0].endswith('.cgi') or l[0].endswith('.bat'):
            cgi = l[0]
            if len(l) == 2:
                args = l[1]
            else:
                args = ''
            l = cgi.rsplit('/', 1)
            self.cgi_info = (
             l[0], l[1] + '?' + args)
            return True
        else:
            for x in self.cgi_directories:
                if self.path == x:
                    return False
                if self.path.startswith(x):
                    i = len(x)
                    self.cgi_info = (self.path[:i], self.path[i:])
                    return True

            return False

    def translate_path(self, path):
        if path.find('/../') >= 0:
            path = '/'
        path = CGIHTTPRequestHandler.translate_path(self, path)
        return path


def run(args=[]):
    if len(args) > 0:
        ip = args[0]
    else:
        import platform
        ip = platform.node()
    print('ip: %s' % ip)
    port = 7070
    try:
        f = open('cgi-bin/pdk.cgi', 'r')
    except IOError:
        try:
            f = open('pdk.cgi', 'r')
        except IOError:
            os.system('ln -s `which pdk` pdk.cgi')
        else:
            f.close()
    else:
        f.close()
    httpd = HTTPServer((ip, port), my_handler)
    sa = httpd.socket.getsockname()
    print('Serving HTTP on %s port %s ...' % (sa[0], sa[1]))
    while True:
        httpd.handle_request()


if __name__ == '__main__':
    run()