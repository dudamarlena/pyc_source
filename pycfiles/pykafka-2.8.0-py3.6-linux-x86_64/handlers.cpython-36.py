# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/handlers.py
# Compiled at: 2018-05-29 17:13:24
# Size of source mod 2**32: 7665 bytes
"""
Author: Keith Bourgoin, Emmett Butler
"""
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['ResponseFuture', 'Handler', 'ThreadingHandler', 'RequestHandler']
from collections import namedtuple
import logging, socket as pysocket
from socket import error as socket_error
from socket import gaierror
import sys as _sys, threading, time
try:
    import gevent, gevent.event, gevent.lock, gevent.queue, gevent.socket as gsocket
    from gevent.socket import error as gsocket_error
    from gevent.socket import gaierror as g_gaierror
except ImportError:
    gevent = None

from .utils.compat import Queue, Empty, Semaphore
log = logging.getLogger(__name__)

class ResponseFuture(object):
    __doc__ = 'A response which may have a value at some point.'

    def __init__(self, handler):
        """
        :type handler: :class:`pykafka.handlers.Handler`
        """
        self.handler = handler
        self.error = False
        self._ready = handler.Event()

    def set_response(self, response):
        """Set response data and trigger get method."""
        self.response = response
        self._ready.set()

    def set_error(self, error):
        """Set error and trigger get method."""
        self.error = error
        self._ready.set()

    def get(self, response_cls=None, timeout=None, **response_kwargs):
        """Block until data is ready and return.

        Raises an exception if there was an error.
        """
        self._ready.wait(timeout)
        if self.error:
            raise self.error
        if response_cls:
            return response_cls((self.response), **response_kwargs)
        else:
            return self.response


class Handler(object):
    __doc__ = 'Base class for Handler classes'

    def spawn(self, target, *args, **kwargs):
        """Create the worker that will process the work to be handled"""
        raise NotImplementedError


class ThreadingHandler(Handler):
    __doc__ = 'A handler that uses a :class:`threading.Thread` to perform its work'
    Queue = Queue
    Event = threading.Event
    Lock = threading.Lock
    Semaphore = Semaphore
    Socket = pysocket
    SockErr = socket_error
    GaiError = gaierror
    _workers_spawned = 0

    def sleep(self, seconds=0):
        time.sleep(seconds)

    def RLock(*args, **kwargs):
        kwargs['verbose'] = False
        try:
            return (threading.RLock)(*args[1:], **kwargs)
        except TypeError:
            kwargs.pop('verbose')
            return (threading.RLock)(*args[1:], **kwargs)

    def spawn(self, target, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['name'] = '{}: {}'.format(ThreadingHandler._workers_spawned, kwargs['name'])
        t = (threading.Thread)(args, target=target, **kwargs)
        t.daemon = True
        t.start()
        ThreadingHandler._workers_spawned += 1
        return t


if gevent:

    class GEventHandler(Handler):
        __doc__ = 'A handler that uses a greenlet to perform its work'
        Queue = gevent.queue.JoinableQueue
        Event = gevent.event.Event
        Lock = gevent.lock.RLock
        RLock = gevent.lock.RLock
        Semaphore = gevent.lock.Semaphore
        Socket = gsocket
        SockErr = gsocket_error
        GaiError = g_gaierror

        def sleep(self, seconds=0):
            gevent.sleep(seconds)

        def spawn(self, target, *args, **kwargs):
            if 'name' in kwargs:
                kwargs.pop('name')
            t = (gevent.spawn)(target, *args, **kwargs)
            return t


class RequestHandler(object):
    __doc__ = 'Uses a Handler instance to dispatch requests.'
    Task = namedtuple('Task', ['request', 'future'])
    Shared = namedtuple('Shared', ['connection', 'requests', 'ending'])

    def __init__(self, handler, connection):
        """
        :type handler: :class:`pykafka.handlers.Handler`
        :type connection: :class:`pykafka.connection.BrokerConnection`
        """
        self.handler = handler
        self.shared = self.Shared(connection=connection, requests=(handler.Queue()),
          ending=(handler.Event()))

    def __del__(self):
        self.stop()

    def request(self, request, has_response=True):
        """Construct a new request

        :type request: :class:`pykafka.protocol.Request`
        :param has_response: Whether this request will return a response
        :returns: :class:`pykafka.handlers.ResponseFuture`
        """
        future = None
        if has_response:
            future = ResponseFuture(self.handler)
        task = self.Task(request, future)
        self.shared.requests.put(task)
        return future

    def start(self):
        """Start the request processor."""
        self.t = self._start_thread()

    def stop(self):
        """Stop the request processor."""
        shared = self.shared
        self.shared = None
        if log:
            log.info('RequestHandler.stop: about to flush requests queue')
        if shared:
            shared.requests.join()
            shared.ending.set()

    def _start_thread(self):
        """Run the request processor"""
        shared = self.shared

        def worker():
            try:
                while not shared.ending.is_set():
                    try:
                        task = shared.requests.get(timeout=1)
                    except Empty:
                        continue

                    try:
                        try:
                            shared.connection.request(task.request)
                            if task.future:
                                res = shared.connection.response()
                                task.future.set_response(res)
                        except Exception as e:
                            if task.future:
                                task.future.set_error(e)

                    finally:
                        shared.requests.task_done()

                log.info('RequestHandler worker: exiting cleanly')
            except:
                if _sys is None:
                    return
                raise

        name = 'pykafka.RequestHandler.worker for {}:{}'.format(self.shared.connection.host, self.shared.connection.port)
        return self.handler.spawn(worker, name=name)