# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/globals.py
# Compiled at: 2014-01-20 12:41:11
# Size of source mod 2**32: 1137 bytes
"""
    flask.globals
    ~~~~~~~~~~~~~

    Defines all the global objects that are proxies to the current
    active context.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from functools import partial
from werkzeug.local import LocalStack, LocalProxy

def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of request context')
    return getattr(top, name)


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return getattr(top, name)


def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of application context')
    return top.app


_request_ctx_stack = LocalStack()
_app_ctx_stack = LocalStack()
current_app = LocalProxy(_find_app)
request = LocalProxy(partial(_lookup_req_object, 'request'))
session = LocalProxy(partial(_lookup_req_object, 'session'))
g = LocalProxy(partial(_lookup_app_object, 'g'))