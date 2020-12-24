# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/logistics/basic_wrapper.py
# Compiled at: 2016-06-30 06:13:10
""" define some logistics wrapper

"""
import logging, sys
from tingyun.packages.wrapt.wrappers import FunctionWrapper as _FunctionWrapper
from tingyun.packages.wrapt.wrappers import BoundFunctionWrapper as _BoundFunctionWrapper
from tingyun.packages.wrapt.wrappers import wrap_object as _wrap_object, wrap_function_wrapper as _wrap_function_wrapper
from tingyun.packages.wrapt.wrappers import function_wrapper as _function_wrapper
console = logging.getLogger(__name__)
wrap_object = _wrap_object
FunctionWrapper = _FunctionWrapper
BoundFunctionWrapper = _BoundFunctionWrapper
wrap_function_wrapper = _wrap_function_wrapper
function_wrapper = _function_wrapper

def import_module(name):
    """Import module, returning the module after the last dot."""
    __import__(name)
    return sys.modules[name]


def in_function(function):

    @function_wrapper
    def _wrapper(wrapped, instance, args, kwargs):
        if instance is not None:
            args, kwargs = function(instance, *args, **kwargs)
            return wrapped(*args[1:], **kwargs)
        else:
            args, kwargs = function(*args, **kwargs)
            return wrapped(*args, **kwargs)

    return _wrapper


def in_function_wrapper(wrapped, function):
    return in_function(function)(wrapped)


def trace_in_function(module, object_path, function):
    return wrap_object(module, object_path, in_function_wrapper, (function,))


def wrap_out_function(function):

    @function_wrapper
    def _wrapper(wrapped, instance, args, kwargs):
        return function(wrapped(*args, **kwargs))

    return _wrapper


def out_function_wrapper(wrapped, function):
    return wrap_out_function(function)(wrapped)


def trace_out_function(module, object_path, function):
    return wrap_object(module, object_path, out_function_wrapper, (function,))