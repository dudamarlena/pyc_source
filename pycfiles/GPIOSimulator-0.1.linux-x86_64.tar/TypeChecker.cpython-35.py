# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/prog/hoerkules/software/core/env/lib/python3.5/site-packages/RPiSim/TypeChecker.py
# Compiled at: 2016-05-24 16:59:52
# Size of source mod 2**32: 986 bytes
from inspect import signature
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):

    def decorate(func):
        if not __debug__:
            return func
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))

            return func(*args, **kwargs)

        return wrapper

    return decorate