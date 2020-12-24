# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/tornado_4/ioloop.py
# Compiled at: 2016-06-30 06:13:10
"""define a detector for tornado ioloop
"""
import sys, logging
from tingyun.armoury.ammunition.tornado_4.utils import finish_tracker, record_exception, obtain_current_tracker
from tingyun.armoury.ammunition.tornado_4.utils import current_thread_id, TrackerTransferContext
from tingyun.logistics.basic_wrapper import wrap_function_wrapper
console = logging.getLogger(__name__)

def trace_run_callback(wrapped, instance, args, kwargs):
    """
    """

    def _get_actually_callback(callback, *args, **kwargs):
        try:
            return callback.func
        except AttributeError:
            return

        return

    callback = _get_actually_callback(*args, **kwargs)
    tracker = getattr(callback, '_self_tracker', None)
    ret = wrapped(*args, **kwargs)
    if tracker:
        tracker._ref_count -= 1
        finish_tracker(tracker)
    return ret


def trace_handle_callback_exception(wrapped, instance, args, kwargs):
    """
    """
    record_exception(sys.exc_info())
    return wrapped(*args, **kwargs)


def _increment_ref_count(callback, wrapped, instance, args, kwargs):
    tracker = obtain_current_tracker()
    if hasattr(callback, '_self_tracker'):
        if callback._self_tracker is not None:
            if current_thread_id() != callback._self_tracker.thread_id:
                callback._self_tracker = None
                return wrapped(*args, **kwargs)
        if tracker is not callback._self_tracker:
            console.warning('Attempt to add callback to ioloop with different tracer attached than in the cache.if this continue, Please report to us.')
            callback._self_tracker = None
            return wrapped(*args, **kwargs)
    if tracker is None:
        return wrapped(*args, **kwargs)
    else:
        tracker._ref_count += 1
        return wrapped(*args, **kwargs)


def trace_add_callback(wrapped, instance, args, kwargs):
    """
    """

    def _get_actually_callback(callback, *args, **kwargs):
        return callback

    callback = _get_actually_callback(*args, **kwargs)
    return _increment_ref_count(callback, wrapped, instance, args, kwargs)


def trace_call_at(wrapped, instance, args, kwargs):
    """
    """
    with TrackerTransferContext(None):
        return wrapped(*args, **kwargs)
    return


def trace_add_handler(wrapped, instance, args, kwargs):
    """
    """
    with TrackerTransferContext(None):
        return wrapped(*args, **kwargs)
    return


def detect_ioloop(module):
    """
    :param module:
    :return:
    """
    wrap_function_wrapper(module, 'IOLoop._run_callback', trace_run_callback)
    wrap_function_wrapper(module, 'IOLoop.handle_callback_exception', trace_handle_callback_exception)
    wrap_function_wrapper(module, 'PollIOLoop.add_callback', trace_add_callback)
    wrap_function_wrapper(module, 'PollIOLoop.call_at', trace_call_at)
    wrap_function_wrapper(module, 'PollIOLoop.add_handler', trace_add_handler)