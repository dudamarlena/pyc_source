# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\TestLibs\np_rw_buffer\np_rw_buffer\utils.py
# Compiled at: 2018-05-10 15:31:22
# Size of source mod 2**32: 1559 bytes
import functools

def make_thread_safe(lock_varname='lock', func=None):
    """Decorate a function making it threadsafe by using the threading lock that matches the lock_varname.

    Args:
        lock_varname (str/method)['lock']: Threading lock variable name or
            a function to decorate with 'lock' variable being a threading.Lock
        func (function/method) [None]: Function to wrap.

    Returns:
        wrap (function): Function that was decorated/wrapped or a function that will decorate a function.
    """
    if not isinstance(lock_varname, str):
        func = lock_varname
        lock_varname = 'lock'
    if func is None:

        def real_decorator(func):
            return make_thread_safe(lock_varname, func)

        return real_decorator
    else:
        if isinstance(func, property):
            fget = None
            fset = None
            fdel = None
            if func.fget:
                fget = make_thread_safe(lock_varname, func.fget)
            if func.fset:
                fset = make_thread_safe(lock_varname, func.fset)
            if func.fdel:
                fdel = make_thread_safe(lock_varname, func.fdel)
            return property(fget, fset, fdel, func.__doc__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with getattr(args[0], lock_varname):
                return func(*args, **kwargs)

        return wrapper