# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/attrcheck/attrcheck.py
# Compiled at: 2011-10-10 02:26:33
import inspect
from functools import wraps

def attrcheck(**keywords):
    """attrcheck(keywords)(function) -> function

To declare attributions of arguments, use this idiom:

@attrcheck(x=['real'], y=['index', 'strip'], z=dir(list))
def foo(x, y, z=[]): pass"""
    errmsg = 'Error checking argument %r of function %r' + ": hasattr(%r, '%s') = False"

    def _(f):

        def check(k, v):
            if k in keywords:
                for n in keywords[k]:
                    if not hasattr(v, n):
                        raise AttributeError(errmsg % (k, f.__name__, v, n))

        spec = inspect.getargspec(f)
        if spec.defaults != None:
            n = len(spec.args) - len(spec.defaults)
            for i, v in enumerate(spec.defaults):
                check(spec.args[(n + i)], v)

        @wraps(f)
        def __(*args, **kw):
            for i, v in enumerate(args):
                k = spec.args[i]
                check(k, v)

            for k, v in kw.items():
                check(k, v)

            return f(*args, **kw)

        return __

    return _