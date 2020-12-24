# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/op_callback_server.py
# Compiled at: 2020-04-19 19:55:58
from dez.http.application import HTTPApplication

def simple_app(environ, start_response):
    print 'POST DATA:'
    print environ['wsgi.input'].read()
    return []


def main(**kwargs):
    httpd = HTTPApplication(kwargs['domain'], kwargs['port'])
    httpd.add_wsgi_rule('/', simple_app)
    httpd.start()