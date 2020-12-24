# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/wsgid/test_app.py
# Compiled at: 2009-03-11 14:16:11
from glashammer.application import make_app
from glashammer.utils import Response
from werkzeug import Response, Request

def do_root(req):
    return Response('hello world')


def do_except(req):
    raise Exception


@Request.application
def app(req):
    print req.path
    if req.path == '/':
        return do_root(req)
    elif req.path == '/except':
        return do_except(req)