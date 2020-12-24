# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/tornado_tracker/httpserver.py
# Compiled at: 2016-06-30 06:13:10
"""this module is implement some wrapper for trace the tornado httpserver module

"""
import sys, logging, traceback
from tingyun.battlefield.tracer import Tracer
from tingyun.battlefield.proxy import proxy_instance
from tingyun.logistics.object_name import callable_name
from tingyun.logistics.basic_wrapper import FunctionWrapper
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.armoury.ammunition.function_tracker import FunctionTracker
console = logging.getLogger(__name__)

def request_environ(environ, request):
    """the environ in the default environ may not include our need environment variable when apply to wsgi application
    :param environ: returned environment from the container request.
    :param request:
    :return:
    """
    ret = dict(environ)
    ret['REQUEST_URI'] = request.uri
    ret['HTTP_REFERER'] = request.headers.get('Referer', '')
    ret['HTTP_X_QUEUE_START'] = request.headers.get('X-Queue-Start')
    if not environ:
        ret['PATH_INFO'] = request.path
        ret['SCRIPT_NAME'] = ''
        ret['QUERY_STRING'] = request.query
    return ret


def setup_func_for_async_trace(request, name, group='async.wait'):
    """used to suspend function between async call with function
    thread_mode: this indicate, relate the tracer to the thread.this should be used with resume_async_trace func

    request: the HTTPRequest for connection
    """
    tracer = getattr(request, '_self_tracer', None)
    if not tracer:
        console.warning('tracker lost when trace the request call chain with async, this trace for function time metric will be interrupted. %s', ('').join(traceback.format_stack()[:-1]))
        return
    else:
        if getattr(request, '_self_async_function_tracker', None):
            console.warning('The last tracker for time metric not finished, but this should not happened.this maybe some logical error in agent. %s', ('').join(traceback.format_stack()[:-1]))
            return
        request._self_async_function_tracker = FunctionTracker(tracer, name, group)
        request._self_async_function_tracker.__enter__()
        return


def finish_async_func_trace(request, group=None):
    """calculate the time metric for async call between func
    thread_mode: this indicate, relate the tracer to the thread.this should be used with setup_async_trace func

    request: the HTTPRequest for connection
    """
    tracer = getattr(request, '_self_tracer', None)
    if not tracer:
        console.warning('tracker lost when trace the request call chain with async, this trace for function time metric will be interrupted. %s', ('').join(traceback.format_stack()[:-1]))
        return
    else:
        try:
            if request._self_async_function_tracker:
                request._self_async_function_tracker.__exit__(None, None, None)
                tracer.async_func_trace_time += request._self_async_function_tracker.duration
        finally:
            request._self_async_function_tracker = None

        return tracer


def stop_request_tracer(request, exc_type=None, exc_val=None, exc_tb=None, segment=None):
    """
    """
    tracer = getattr(request, '_self_tracer', None)
    try:
        try:
            if not tracer:
                console.debug('tracker lost when trace the request call chain with async, this trace for function time metric will be interrupted. %s', ('').join(traceback.format_stack()[:-1]))
                return
            thread_tracer = current_tracker()
            if tracer == thread_tracer:
                tracer.finish_work(exc_type, exc_val, exc_tb, False)
            else:
                tracer.finish_work(exc_type, exc_val, exc_tb, True)
        except Exception as err:
            console.exception('Tornado raise error when stop the trace. %s, %s', segment, err)

    finally:
        request._self_request_finished = True
        request._self_tracer = None
        request._self_async_function_tracker = None

    return


def generate_tracer(request, framework='Tornado'):
    """
    :param request: the http request for client
    :return:
    """
    tracer = Tracer(proxy_instance(), request_environ({}, request), framework)
    if not tracer.enabled:
        return
    else:
        try:
            tracer.start_work()
            tracer.drop_tracker()
            request._self_request_finished = False
            request._self_tracer = tracer
            request._self_async_function_tracker = None
        except Exception as err:
            stop_request_tracer(request, *(sys.exc_info() + ('generate-tracker-exception', )))
            console.exception('Error occurred, when generate a tracker for tornado. %s', err)
            raise

        return tracer


def connection_on_headers_wrapper(wrapped):
    """if client request server without body, so the request in connection object maybe None at there
    """

    def wrapper(wrapped, adapter, args, kwargs):
        """
        :param wrapped: the wrapped function `HTTPConnection._on_headers`
        :param adapter: the instance of the `HTTPConnection`
        :param args: args for `HTTPConnection._on_headers`
        :param kwargs: kwargs for `HTTPConnection._on_headers`
        :return: return of `HTTPConnection._on_headers` method
        """
        tracer = current_tracker()
        if tracer:
            console.warning("Unexpected situation arise, but no side effect to use the agent. That's only indicate some illogicality tracker in tracer. if this continue, please report to us, thank u.")
            tracer.drop_tracker()
            return wrapped(*args, **kwargs)
        ret = wrapped(*args, **kwargs)
        if hasattr(adapter, 'stream') and adapter.stream.closed() or hasattr(adapter, '_request_finished') and adapter._request_finished:
            return ret
        if hasattr(adapter, 'connection') and adapter.connection.stream.closed():
            return ret
        if hasattr(adapter, 'connection'):
            request = adapter.request
        else:
            request = adapter._request
        if not request or hasattr(request, '_self_tracer'):
            return ret
        if hasattr(request, '_self_tracer'):
            return ret
        tracer = generate_tracer(request)
        if not tracer or not tracer.enabled:
            return ret

        def _stream_close_callback():
            if finish_async_func_trace(request, ''):
                return
            stop_request_tracer(request, segment='stream-close-callback')

        if hasattr(adapter, 'connection'):
            adapter.connection.stream._self_stream_close_callback = _stream_close_callback
        else:
            adapter.stream._self_stream_close_callback = _stream_close_callback
        tracer.set_tracker_name(callable_name(wrapped))
        setup_func_for_async_trace(request, 'connection.header-to-body')
        return ret

    return FunctionWrapper(wrapped, wrapper)


def connect_on_request_body_wrapper(wrapped):
    """
    """

    def wrapper(wrapped, adapter, args, kwargs):
        """
        """
        if hasattr(adapter, 'connection'):
            request = adapter.request
        else:
            request = adapter._request
        tracer = finish_async_func_trace(request, group='request-body-in')
        if not tracer:
            return wrapped(*args, **kwargs)
        try:
            ret = wrapped(*args, **kwargs)
        except Exception as err:
            console.exception('Tornado raise error in HTTPConnection on_request_body. %s', err)
            stop_request_tracer(request, *(sys.exc_info() + ('request-body-exception', )))
            raise
        else:
            if request._self_request_finished:
                return ret
            if not request.connection.stream.writing():
                stop_request_tracer(request, segment='stream-not-writing')
                return ret
            setup_func_for_async_trace(request, name='connection.body-to-finish')

        return ret

    return FunctionWrapper(wrapped, wrapper)


def connection_finish_request_wrapper(wrapped):
    """the wrapped function maybe called more than once.
    """

    def wrapper(wrapped, adapter, args, kwargs):
        """
        """
        if hasattr(adapter, 'connection'):
            request = adapter.request
        else:
            request = adapter._request
        tracer = getattr(request, '_self_tracer', None)
        if not tracer:
            return wrapped(*args, **kwargs)
        else:
            if request._self_request_finished:
                return wrapped(*args, **kwargs)
            tracer = finish_async_func_trace(request, 'request-finish-in')
            if not tracer:
                return wrapped(*args, **kwargs)
            try:
                ret = wrapped(*args, **kwargs)
            except Exception as _:
                stop_request_tracer(request, *(sys.exc_info() + ('connect-finished-with-exceptiono', )))
                raise

            if hasattr(adapter, 'connection'):
                stop_request_tracer(request, segment='finish-app-call')
            return ret

    return FunctionWrapper(wrapped, wrapper)


def iostream_close_callback_wrapper(wrapped):
    """if client communicate with server user keep-alive protocol, the callback can not be actived.
    """

    def wrapper(wrapped, instance, args, kwargs):
        """
        """
        if not instance.closed():
            return wrapped(*args, **kwargs)
        else:
            if instance._pending_callbacks != 0:
                return wrapped(*args, **kwargs)
            callback = getattr(instance, '_self_stream_close_callback', None)
            instance._self_stream_close_callback = None
            if callback:
                callback()
            return wrapped(*args, **kwargs)

    return FunctionWrapper(wrapped, wrapper)