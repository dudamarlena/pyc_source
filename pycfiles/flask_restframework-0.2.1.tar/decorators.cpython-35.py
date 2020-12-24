# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/decorators.py
# Compiled at: 2017-06-17 09:38:23
# Size of source mod 2**32: 1455 bytes
from functools import wraps
from flask import jsonify
from flask.globals import request

def validate(serializerCls):

    def dec(view_func):

        @wraps(view_func)
        def inner(*a, **k):
            s = serializerCls(request.json)
            if not s.validate():
                out = jsonify(s.errors)
                out.status_code = 400
                return out
            return view_func(*a, **k)

        return inner

    return dec


def list_route(methods=None):
    methods = methods or ['GET']

    def dec(func):

        @wraps(func)
        def inner(*a, **k):
            return func(*a, **k)

        inner._is_view_function = True
        inner._methods = methods
        inner._name_part = func.__name__
        inner._route_part = '/{}'.format(inner._name_part)
        return inner

    return dec


def detail_route(methods=None):
    methods = methods or ['POST']

    def dec(func):

        @wraps(func)
        def inner(*a, **k):
            return func(*a, **k)

        inner._is_view_function = True
        inner._methods = methods
        inner._name_part = func.__name__
        inner._route_part = '/{}/<pk>'.format(inner._name_part)
        return inner

    return dec


def auth_backends(*backends):

    def dec(func):

        @wraps(func)
        def inner(*a, **k):
            return func(*a, **k)

        inner.authentication_backends = backends
        return inner

    return dec