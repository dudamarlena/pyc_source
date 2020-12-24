# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyquchk/utils.py
# Compiled at: 2013-09-15 12:54:08
from functools import wraps
import inspect

def optional_args(decor):
    """Decorator for decorators (sic) that are intended to take
    optional arguments.

    It supports decorators written both as classes or functions,
    as long as they are "doubly-callable".
    For classes, this means implementing ``__call__``, while
    functions must return a function that returns a function
    that accepts a function... which is obvious, of course.
    """

    @wraps(decor)
    def wrapped(*args, **kwargs):
        one_arg = len(args) == 1 and not kwargs
        if one_arg and inspect.isfunction(args[0]):
            return decor()(args[0])
        else:
            return decor(*args, **kwargs)

    return wrapped