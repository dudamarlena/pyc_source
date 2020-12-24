# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/wrap.py
# Compiled at: 2019-08-19 15:09:29
""""""
__all__ = [
 'wraps', 'wrapped', 'is_wrapping', 'is_wrapped']
import weakref
from functools import wraps as _wraps
__WRAPPED = '__wrapped__'
__WRAPPER = '__wrapper__'

def wraps(wrapped, *args, **kwargs):
    """A wrap decorator which stores in the returned function a reference to
    the wrapped function (in member '__wrapped__')"""
    wrapper = _wraps(wrapped, *args, **kwargs)
    setattr(wrapper, __WRAPPED, weakref.ref(wrapped))
    setattr(wrapped, __WRAPPER, weakref.ref(wrapper))
    return wrapper


def is_wrapping(wrapper):
    """Determines if the given callable is a wrapper for another callable"""
    return hasattr(wrapper, __WRAPPED)


def is_wrapped(wrapped):
    """Determines if the given callable is being wrapped by another callable"""
    return hasattr(wrapped, __WRAPPER)


def wrapped(wrapper, recursive=True):
    """Returns the wrapped function around the given wrapper. If the given
    callable is not "wrapping" any function, the wrapper itself is returned"""
    if is_wrapping(wrapper):
        _wrapped = wrapper.__wrapped__()
    else:
        return wrapper
    if recursive:
        return wrapped(_wrapped)
    return _wrapped