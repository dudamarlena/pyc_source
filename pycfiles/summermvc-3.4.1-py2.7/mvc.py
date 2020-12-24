# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/decorator/mvc.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'request_mapping', 'is_request_mapping_present', 'get_request_mapping',
 'exception_handler', 'is_exception_handler_present', 'get_exception_handler',
 'rest_controller', 'is_rest_controller_present']
__authors__ = ['Tim Chow']
import types, inspect
from ..exception import InvalidArgumentError
from ..reflect import *
from .component import component

def request_mapping(uri, method=None, consumes=None, produce=None):

    def _inner(f):
        if isinstance(f, types.FunctionType):
            setattr(f, '__mvc_args__', {'uri': uri, 'method': method, 'consumes': isinstance(consumes, basestring) and [consumers] or consumes or [], 
               'produce': produce})
        elif inspect.isclass(f):
            setattr(f, '__mvc_args__', {'uri': uri})
        return f

    return _inner


def get_request_mapping(obj):
    if '__mvc_args__' not in get_declared_fields(obj, only_names=True):
        return None
    else:
        attr_value = getattr(obj, '__mvc_args__')
        if not isinstance(attr_value, dict) or 'uri' not in attr_value:
            return None
        return attr_value


def is_request_mapping_present(obj):
    return get_request_mapping(obj) is not None


def exception_handler(uri, exc):
    if not isinstance(uri, basestring) or not uri:
        raise InvalidArgumentError
    if not issubclass(exc, BaseException):
        raise InvalidArgumentError

    def _inner(f):
        if not isinstance(f, types.FunctionType):
            raise InvalidArgumentError
        setattr(f, '__mvc_exception_handler__', {'uri': uri, 'exc': exc})
        return f

    return _inner


def get_exception_handler(f, default=None):
    if not isinstance(f, types.MethodType):
        raise InvalidArgumentError
    annotation = getattr(f, '__mvc_exception_handler__', None)
    if annotation is None or not isinstance(annotation, dict) or 'uri' not in annotation or 'exc' not in annotation:
        return default
    return annotation


def is_exception_handler_present(f):
    return get_exception_handler(f, None) is not None


def rest_controller(*outer_args, **outer_kwargs):
    returning = component(*outer_args, **outer_kwargs)
    if inspect.isclass(returning):
        setattr(returning, '__rest_controller__', True)
        return returning

    def _inner(*inner_args, **inner_kwargs):
        cls = returning(*inner_args, **inner_kwargs)
        setattr(cls, '__rest_controller__', True)
        return cls

    return _inner


def is_rest_controller_present(cls):
    try:
        v = get_declared_attribute(cls, '__rest_controller__')
        return v == True
    except ValueError:
        return False