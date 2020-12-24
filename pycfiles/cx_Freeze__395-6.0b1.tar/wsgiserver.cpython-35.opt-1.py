# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\importlib\wsgiserver.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 527 bytes
__doc__ = 'WSGI server example'
from __future__ import print_function
from gevent.pywsgi import WSGIServer

def application(env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [
         '<b>hello world</b>']
    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return [
     '<h1>Not Found</h1>']


if __name__ == '__main__':
    print('Serving on 8088...')
    WSGIServer(('127.0.0.1', 8088), application).serve_forever()