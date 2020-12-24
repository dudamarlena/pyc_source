# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/decorators.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = ' Decorators used in cxmanage_api '
from functools import wraps

def retry(count, allowed_errors=Exception):
    """ Create a decorator that retries a function call up to 'count' times.

    :param count: Max retry count
    :type count: integer
    :param allowed_errors: Types of errors to allow
    :type allowed_errors: Exception or iterable

    :return: Function decorator that retries the wrapped function
    :rtype: function

    """
    try:
        allowed_errors = tuple(allowed_errors)
    except TypeError:
        allowed_errors = (
         allowed_errors,)

    def decorator(function):
        """ The decorator """

        @wraps(function)
        def wrapper(*args, **kwargs):
            """ The wrapper function """
            for _ in range(count):
                try:
                    return function(*args, **kwargs)
                except tuple(allowed_errors):
                    pass

            else:
                return function(*args, **kwargs)

        return wrapper

    return decorator