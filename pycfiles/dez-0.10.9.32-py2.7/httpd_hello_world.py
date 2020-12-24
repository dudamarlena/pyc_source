# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dez/samples/httpd_hello_world.py
# Compiled at: 2015-11-19 18:49:54
import event
from dez.http.server import HTTPDaemon, HTTPResponse, RawHTTPResponse

def test_dispatch(request):
    r = HTTPResponse(request)
    r.write('Aloha Des!!')
    r.dispatch()


def noop():
    return True


def main(**kwargs):
    httpd = HTTPDaemon(kwargs['domain'], kwargs['port'])
    httpd.register_prefix('/index', test_dispatch)
    event.timeout(1, noop)
    event.dispatch()


def profile(**kwargs):
    import hotshot
    prof = hotshot.Profile('orbited_http_test.profile')
    prof.runcall(main, **kwargs)
    prof.close()