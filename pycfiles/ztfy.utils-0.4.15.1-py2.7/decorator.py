# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/decorator.py
# Compiled at: 2014-01-09 04:34:57
import functools, warnings

def deprecated(*msg):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    """

    def decorator(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn_explicit('Function %s is deprecated. %s' % (func.__name__, message), category=DeprecationWarning, filename=func.func_code.co_filename, lineno=func.func_code.co_firstlineno + 1)
            return func(*args, **kwargs)

        return new_func

    if len(msg) == 1 and callable(msg[0]):
        message = ''
        return decorator(msg[0])
    else:
        message = msg[0]
        return decorator