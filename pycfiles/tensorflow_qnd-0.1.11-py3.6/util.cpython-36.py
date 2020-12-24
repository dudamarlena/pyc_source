# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/util.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 621 bytes
import functools, inspect, tensorflow as tf

def func_scope(func):

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs):
        with tf.variable_scope(func.__name__):
            return func(*args, **kwargs)

    wrapped_func.__signature__ = inspect.signature(func)
    return wrapped_func


def are_instances(objects, klass):
    return all(isinstance(obj, klass) for obj in objects)