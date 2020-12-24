# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/pyjznet/decorators.py
# Compiled at: 2014-12-11 03:57:09
from __future__ import print_function
import functools

def rpc_method(func, name=None):

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        attr_name = '__rpc_method_name_%s' % func.__name__
        attr_value = name
        if name is None:
            attr_value = func.__name__
        setattr(func.__objclass__, attr_name, attr_value)
        return func(*args, **kwargs)

    return wrapped