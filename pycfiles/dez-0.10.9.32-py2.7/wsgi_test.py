# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/wsgi_test.py
# Compiled at: 2015-11-19 18:49:54
from dez.http.application import HTTPApplication

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']


def main(**kwargs):
    httpd = HTTPApplication(kwargs['domain'], kwargs['port'])
    httpd.add_wsgi_rule('/', simple_app)
    httpd.start()