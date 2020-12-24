# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/utils/functional.py
# Compiled at: 2010-05-12 10:25:54
"""
函数工具
=================================

索引
=================================

* :func:`once`
* :func:`synchronized`
* :func:`inspect_kargs`
* :func:`get_func_caller`

=================================

.. autofunction:: once
.. autofunction:: synchronized
.. autofunction:: inspect_kargs
.. autofunction:: get_func_caller
"""
import types, inspect, functools, threading
__all__ = [
 'once', 'synchronized', 'get_func_caller']

def once(func):
    u"""
    使函数或者方法只执行一次
    
    :param func: function or method to decorate
    """

    def wrapper(*args, **kwargs):
        if hasattr(func, '_once_result'):
            return func._once_result
        else:
            func._once_result = func(*args, **kwargs)
            return func._once_result

    return functools.update_wrapper(wrapper, func)


def synchronized(func):
    """
    synchronize function or method
    
    :param func: function or method to decorate
    """

    def wrapper(*__args, **__kw):
        if hasattr(func, 'im_self') and func.im_self:
            obj = func.im_self
        else:
            obj = func
        if not hasattr(obj, '_lock'):
            obj.__dict__['_lock'] = threading.Condition()
        obj._lock.acquire()
        try:
            return func(*__args, **__kw)
        finally:
            obj._lock.release()

    return functools.update_wrapper(wrapper, func)


def inspect_kargs(func, kargs):
    argspec = inspect.getargspec(func)
    if argspec[2]:
        args = kargs
    else:
        args = {}
        argnames = argspec[0][isinstance(func, types.MethodType) and 1 or 0:]
    for name in argnames:
        if name in kargs:
            args[name] = kargs[name]

    return args


def get_func_caller():
    return inspect.stack()[2][3]