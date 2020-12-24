# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authorize_middleware/pylons_func.py
# Compiled at: 2009-10-17 15:11:18
from decorator import decorator
from pylons import request
from errors import *
from auth import authorize_request

def authorize(function=None):
    """
    This is a decorator which can be used to decorate a Pylons controller action.
    It gives function ``function`` environ dictionary and executes it. Function
    should return either True or False.
    """

    def validate(func, self, *args, **kwargs):
        authorize_request(request.environ, function)
        return func(self, *args, **kwargs)

    return decorator(validate)


def authorized(function=None):
    """
    Similar to the ``authorize_request()`` function with no access to the
    request but rather than raising an exception to stop the request if a
    authorization check fails, this function simply returns ``False`` so that you
    can test permissions in your code without triggering a sign in. It can
    therefore be used in a controller action or template.

    Use like this::

        if authorized(function):
            return Response('You are authorized')
        else:
            return Response('Access denied')
 
    """
    try:
        authorize_request(request.environ, function)
    except (NotAuthorizedError, NotAuthenticatedError):
        return False

    return True