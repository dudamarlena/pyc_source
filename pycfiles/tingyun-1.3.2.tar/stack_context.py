# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/tornado_4/stack_context.py
# Compiled at: 2016-06-30 06:13:10
"""define detector for detect stack context module
"""
import logging
from tingyun.logistics.object_name import callable_name
from tingyun.logistics.basic_wrapper import wrap_function_wrapper
from tingyun.armoury.ammunition.tornado_4.utils import create_tracker_aware_fxn, obtain_current_tracker, record_exception
console = logging.getLogger(__name__)
fxn_cache = []

def trace_wrap(wrapped, instance, args, kwargs):
    """
    """

    def _fxn_arg_extractor(fn, *args, **kwargs):
        return fn

    unwrapped_fxn = _fxn_arg_extractor(*args, **kwargs)
    wrapped_fxn = wrapped(*args, **kwargs)
    should_trace = callable_name(unwrapped_fxn) not in fxn_cache
    if should_trace:
        fxn_cache.append(callable_name(unwrapped_fxn))
    tracker_aware_fxn = create_tracker_aware_fxn(wrapped_fxn, fxn_for_name=unwrapped_fxn, should_trace=should_trace)
    if tracker_aware_fxn is None:
        return wrapped_fxn
    else:
        tracker_aware_fxn._wrapped = True
        tracker_aware_fxn._self_tracker = obtain_current_tracker()
        return tracker_aware_fxn


def trace_handle_exception(wrapped, instance, args, kwargs):
    """
    """

    def _exc_extractor(tail, exc, *args, **kwargs):
        return exc

    exc = _exc_extractor(*args, **kwargs)
    record_exception(exc)
    return wrapped(*args, **kwargs)


def detect_stack_context(module):
    """
    """
    wrap_function_wrapper(module, 'wrap', trace_wrap)
    wrap_function_wrapper(module, '_handle_exception', trace_handle_exception)