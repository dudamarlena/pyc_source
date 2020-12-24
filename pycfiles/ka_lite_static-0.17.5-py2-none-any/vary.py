# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/views/decorators/vary.py
# Compiled at: 2018-07-11 18:15:30
from functools import wraps
from django.utils.cache import patch_vary_headers
from django.utils.decorators import available_attrs

def vary_on_headers(*headers):
    """
    A view decorator that adds the specified headers to the Vary header of the
    response. Usage:

       @vary_on_headers('Cookie', 'Accept-language')
       def index(request):
           ...

    Note that the header names are not case-sensitive.
    """

    def decorator(func):

        @wraps(func, assigned=available_attrs(func))
        def inner_func(*args, **kwargs):
            response = func(*args, **kwargs)
            patch_vary_headers(response, headers)
            return response

        return inner_func

    return decorator


def vary_on_cookie(func):
    """
    A view decorator that adds "Cookie" to the Vary header of a response. This
    indicates that a page's contents depends on cookies. Usage:

        @vary_on_cookie
        def index(request):
            ...
    """

    @wraps(func, assigned=available_attrs(func))
    def inner_func(*args, **kwargs):
        response = func(*args, **kwargs)
        patch_vary_headers(response, ('Cookie', ))
        return response

    return inner_func