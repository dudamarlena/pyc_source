# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/tornado_4/http_server.py
# Compiled at: 2016-06-30 06:13:10
"""define some wrapper to wrapt some method in tornado http server
"""
import logging
from tingyun.logistics.basic_wrapper import wrap_function_wrapper
from tingyun.armoury.ammunition.tornado_4.utils import finish_tracker
console = logging.getLogger(__name__)

def trace_tracker_export(wrapped, instance, args, kwargs):
    """
    """
    request = instance.delegate.request if instance.delegate else instance.request
    if not request:
        console.warning('No request got in _ServerRequestAdapter object. this should not be happen. if this continue. please report us.')
        return wrapped(*args, **kwargs)
    else:
        tracker = getattr(request, '_self_tracker', None)
        if not tracker:
            return wrapped(*args, **kwargs)
        try:
            wrapped(*args, **kwargs)
        finally:
            setattr(tracker, '_can_finalize', True)
            finish_tracker(tracker)

        return


def detect_tracker_export(module):
    """detect the export of the tracker.
    :param module: tornado httpserver
    :return:
    """
    wrap_function_wrapper(module, '_ServerRequestAdapter.on_connection_close', trace_tracker_export)
    wrap_function_wrapper(module, '_ServerRequestAdapter.finish', trace_tracker_export)