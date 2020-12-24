# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\importlib\wsgiserver.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 527 bytes
"""WSGI server example"""
from __future__ import print_function
from gevent.pywsgi import WSGIServer

def application(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [
         b'<b>hello world</b>']
    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return [b'<h1>Not Found</h1>']


if __name__ == '__main__':
    print('Serving on 8088...')
    WSGIServer(('127.0.0.1', 8088), application).serve_forever()