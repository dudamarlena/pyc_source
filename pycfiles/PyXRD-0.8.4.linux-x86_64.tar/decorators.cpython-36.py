# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/decorators.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3171 bytes
import types

def good_decorator(decorator):
    """This decorator makes decorators behave well wrt to decorated
    functions names, doc, etc."""

    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g

    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


def good_classmethod_decorator(decorator):
    """This decorator makes class method decorators behave well wrt
    to decorated class method names, doc, etc."""

    def new_decorator(cls, f):
        g = decorator(cls, f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g

    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


def good_decorator_accepting_args(decorator):
    """This decorator makes decorators behave well wrt to decorated
    functions names, doc, etc. 

    Differently from good_decorator, this accepts decorators possibly
    receiving arguments and keyword arguments.

    This decorato can be used indifferently with class methods and
    functions."""

    def new_decorator(*f, **k):
        g = decorator(*f, **k)
        if 1 == len(f):
            if isinstance(f[0], types.FunctionType):
                g.__name__ = f[0].__name__
                g.__doc__ = f[0].__doc__
                g.__dict__.update(f[0].__dict__)
        return g

    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    new_decorator.__module__ = decorator.__module__
    return new_decorator