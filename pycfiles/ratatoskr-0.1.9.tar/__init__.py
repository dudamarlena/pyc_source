# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ratatoskr/__init__.py
# Compiled at: 2019-03-20 07:33:15
from . import utils
from . import operation_registry
from .operation_wrappers import base_wrappers
import inspect
from . import exceptions
from .protectron import protectron

@utils.doublewrap
def register_operation(func, operation_wrapper=base_wrappers.LocalOperation):
    if inspect.isclass(operation_wrapper):
        operation_wrapper_instance = operation_wrapper()
    else:
        operation_wrapper_instance = operation_wrapper
    operation_wrapper_instance.load_wrapped_operation(func)
    operation_registry_cls = operation_registry.OperationRegistry
    operation_registry_cls.register_operation(operation_wrapper_instance)

    @utils.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def deregister_operation(operation_name):
    operation_registry_cls = operation_registry.OperationRegistry
    operation_registry_cls.deregister_operation(operation_name)


def dispatch_event(event):
    return operation_registry.OperationRegistry.call(event)