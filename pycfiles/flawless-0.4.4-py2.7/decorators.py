# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/flawless/client/decorators.py
# Compiled at: 2017-12-21 19:44:14
import functools, inspect, flawless.client.client
from flawless.lib.utils import im_func, im_self

def wrap_function(func=None, error_threshold=None, reraise_exception=True, save_current_stack_trace=True):
    """ Wraps a function with reporting to errors backend """
    if func:
        return flawless.client.client._wrap_function_with_error_decorator(func=func, error_threshold=error_threshold, reraise_exception=reraise_exception, save_current_stack_trace=save_current_stack_trace)
    else:
        return functools.partial(flawless.client.client._wrap_function_with_error_decorator, error_threshold=error_threshold, reraise_exception=reraise_exception, save_current_stack_trace=save_current_stack_trace)


def wrap_class(cls, error_threshold=None):
    """ Wraps a class with reporting to errors backend by decorating each function of the class.
            Decorators are injected under the classmethod decorator if they exist.
    """
    methods = inspect.getmembers(cls, inspect.ismethod) + inspect.getmembers(cls, inspect.isfunction)
    for method_name, method in methods:
        wrapped_method = flawless.client.client._wrap_function_with_error_decorator(method if not im_self(method) else im_func(method), save_current_stack_trace=False, error_threshold=error_threshold)
        if im_self(method):
            wrapped_method = classmethod(wrapped_method)
        setattr(cls, method_name, wrapped_method)

    return cls


class WrapClassMetaclass(type):
    """Specify FlawlessMetaClass as the metaclass for your class if you want Flawless to wrap a base class
    that other classes inherit from. Only methods defined in the base class that uses this metaclass will be wrapped.
    (i.e. new methods defined only in the subclass will not be wrapped)"""

    def __init__(cls, name, bases, dct):
        cls = wrap_class(cls)
        return super(WrapClassMetaclass, cls).__init__(name, bases, dct)