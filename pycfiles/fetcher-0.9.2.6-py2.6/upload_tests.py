# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\upload_tests.py
# Compiled at: 2010-12-30 05:46:57
__created__ = '2009/09/27'
__author__ = 'xlty.0512@gmail.com'
__author__ = '牧唐 杭州'
from httplib import HTTPConnection
HTTPConnection.debuglevel = 5
from fetcher import *
from unittest import TestCase
import BaseHTTPServer, SimpleHTTPServer
from threading import Thread
import urllib, urlparse, logging
from cStringIO import StringIO

class MySimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        code = typex = leng = text = None
        if 'Content-Length' in self.headers:
            cl = int(self.headers['Content-Length'])
            ct = self.headers['Content-Type']
            data = self.rfile.read(cl)
            ps = data
            if 'multipart' in ct:
                cts = ct.split('; ')
                cc = []
                for c in cts:
                    if '=' in c:
                        cc.append(c.split('='))

                params = dict(cc)
                boundary = params['boundary']
                multis = data.split('--' + boundary)
                for m in multis:
                    if m.endswith('--\r\n'):
                        break
                    print 'parsed qs:>>', m
                    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'

        text = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>\n\n                            <title>Directory listing for</title>\n\n                            <body>\n                                                                    淘宝\n\n                                                                    中测定发生发生的发生的fsd发送方式地方\n                                                                我是中文我是中文, 巍峨哦是中\n                            <h2>Directory listing for</h2>\n\n                            <hr>\n<ul>\n\n                            <img src="./a.jpg"/>\n                            </body>\n                            </html>').encode('gb2312')
        leng = len(text)
        self.send_response(code or 200)
        self.send_header('r-type', 'post')
        self.send_header('Content-type', typex or 'text/plain')
        self.send_header('Content-Length', leng or 0)
        self.end_headers()
        self.wfile.write(text)
        self.wfile.close()
        return


def run():

    def run_while_true(server_class=BaseHTTPServer.HTTPServer, handler_class=MySimpleHTTPRequestHandler):
        server_address = ('', 8199)
        httpd = server_class(server_address, handler_class)
        while 1:
            httpd.handle_request()

    run_while_true()


t = Thread(target=run)
t.daemon = True
t.start()
fetcher = Fetcher()
d = fetcher.fetch('http://localhost:8080/upload', {'x': ('1', '2'), 'ty': ['xv', '123'], 'xx': '1454', 'myfile': (
            'test.txt', open('./__init__.py', 'rb')), 
   'myfile2': ('test2.txt', open('./__init__.py', 'rb'))})
print d
if __name__ == '__main__':
    import time
    time.sleep(3000)