# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/web2py_trakcer.py
# Compiled at: 2016-06-30 06:13:10
"""this module is implement the function detector for web2py

"""
import sys
from tingyun.armoury.ammunition.function_tracker import FunctionTracker
from tingyun.logistics.basic_wrapper import FunctionWrapper, wrap_object, import_module
from tingyun.logistics.object_name import callable_name
from tingyun.armoury.ammunition.tracker import current_tracker

def uncaught_exception_wrapper(wrapped):
    """
    :param wrapped:
    :return:
    """

    def wrapper(wrapped, instance, args, kwargs):
        tracker = current_tracker()

        def _wrapper(request, response, session):
            """
            """
            name = '%s.%s.%s.%s' % (request.application, request.controller, request.function, request.extension)
            tracker.set_tracker_name(name=name, group='web2py')
            wrapped(request, response, session)

        if tracker is None:
            return wrapped(*args, **kwargs)
        else:
            HTTP = import_module('gluon.http').HTTP
            try:
                return _wrapper(*args, **kwargs)
            except HTTP:
                raise
            except:
                tracker.record_exception(*sys.exc_info())
                raise

            return

    return FunctionWrapper(wrapped, wrapper)


def trace_serve_controller(module, object_path):
    """all application errors in web2py will raised in this function.
    :param module:
    :param object_path:
    :return:
    """
    wrap_object(module, object_path, uncaught_exception_wrapper)