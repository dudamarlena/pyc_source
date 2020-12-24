# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/view_decorators.py
# Compiled at: 2013-07-23 18:15:16
from functools import wraps
from django.utils.decorators import available_attrs

def header(name, value):

    def decorator(func):

        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            response[name] = value
            return response

        return inner

    return decorator


def headers(header_map):

    def decorator(func):

        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            for k in header_map:
                response[k] = header_map[k]

            return response

        return inner

    return decorator


allow_origin = lambda origin: header('Access-Control-Allow-Origin', origin)
allow_origin_all = allow_origin('*')