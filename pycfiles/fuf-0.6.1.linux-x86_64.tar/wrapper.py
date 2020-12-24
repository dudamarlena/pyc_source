# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msoucy/.virtualenv/fuf/lib/python2.7/site-packages/fuf/wrapper.py
# Compiled at: 2014-10-07 22:23:00
"""
Action Set class and demonstration
Matt Soucy

The main purpose of this file is to demonstrate some of the fun things
that can be done with functions in Python.

Particularly interesting are:
- `fdup`: Duplicates a function perfectly down to the signature
   that is stored internally and printed with using help()
- `wrapper`: Wrapper wrapper - apply as a decorator to a decorator to produce
   a decorator that generates perfect-forwarded functions

Ideas taken from:
- http://numericalrecipes.wordpress.com/2009/05/25/signature-preserving-function-decorators/
"""
import inspect
from functools import update_wrapper
from six import exec_

def wrapper(_wrap_):
    """Wrap a decorator with support for the perfect wrapper decorator"""

    def wrapper(_func_):
        """Create a perfect wrapper (including signature) around a function"""
        src = ('def _newfunc{0}: return _wrap_(func){0}').format(inspect.formatargspec(*inspect.getargspec(_func_)))
        evaldict = {'_wrap_': _wrap_, 'func': _func_}
        exec_(src, evaldict)
        ret = evaldict['_newfunc']
        update_wrapper(ret, _func_)
        ret.__wrapped__ = _func_
        return ret

    return wrapper


identity = lambda func: func
fdup = wrapper(identity)