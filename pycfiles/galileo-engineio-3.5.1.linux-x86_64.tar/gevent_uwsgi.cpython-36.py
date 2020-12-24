# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/async_drivers/gevent_uwsgi.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 5404 bytes
from __future__ import absolute_import
import six, gevent
from gevent import queue
from gevent.event import Event
import uwsgi
_websocket_available = hasattr(uwsgi, 'websocket_handshake')

class Thread(gevent.Greenlet):
    __doc__ = "\n    This wrapper class provides gevent Greenlet interface that is compatible\n    with the standard library's Thread class.\n    "

    def __init__(self, target, args=[], kwargs={}):
        (super(Thread, self).__init__)(target, *args, **kwargs)

    def _run(self):
        return self.run()


class uWSGIWebSocket(object):
    __doc__ = "\n    This wrapper class provides a uWSGI WebSocket interface that is\n    compatible with eventlet's implementation.\n    "

    def __init__(self, app):
        self.app = app
        self._sock = None

    def __call__(self, environ, start_response):
        self._sock = uwsgi.connection_fd()
        self.environ = environ
        uwsgi.websocket_handshake()
        self._req_ctx = None
        if hasattr(uwsgi, 'request_context'):
            self._req_ctx = uwsgi.request_context()
        else:
            from gevent.event import Event
            from gevent.queue import Queue
            from gevent.select import select
            self._event = Event()
            self._send_queue = Queue()

            def select_greenlet_runner(fd, event):
                while True:
                    event.set()
                    try:
                        select([fd], [], [])[0]
                    except ValueError:
                        break

            self._select_greenlet = gevent.spawn(select_greenlet_runner, self._sock, self._event)
        self.app(self)

    def close(self):
        """Disconnects uWSGI from the client."""
        uwsgi.disconnect()
        if self._req_ctx is None:
            self._select_greenlet.kill()
            self._event.set()

    def _send(self, msg):
        """Transmits message either in binary or UTF-8 text mode,
        depending on its type."""
        if isinstance(msg, six.binary_type):
            method = uwsgi.websocket_send_binary
        else:
            method = uwsgi.websocket_send
        if self._req_ctx is not None:
            method(msg, request_context=(self._req_ctx))
        else:
            method(msg)

    def _decode_received(self, msg):
        """Returns either bytes or str, depending on message type."""
        if not isinstance(msg, six.binary_type):
            return msg
        else:
            type = six.byte2int(msg[0:1])
            if type >= 48:
                return msg.decode('utf-8')
            return msg

    def send(self, msg):
        """Queues a message for sending. Real transmission is done in
        wait method.
        Sends directly if uWSGI version is new enough."""
        if self._req_ctx is not None:
            self._send(msg)
        else:
            self._send_queue.put(msg)
            self._event.set()

    def wait(self):
        """Waits and returns received messages.
        If running in compatibility mode for older uWSGI versions,
        it also sends messages that have been queued by send().
        A return value of None means that connection was closed.
        This must be called repeatedly. For uWSGI < 2.1.x it must
        be called from the main greenlet."""
        while self._req_ctx is not None:
            try:
                msg = uwsgi.websocket_recv(request_context=(self._req_ctx))
            except IOError:
                return
            else:
                return self._decode_received(msg)
            event_set = self._event.wait(timeout=3)
            if event_set:
                self._event.clear()
                msgs = []
                while True:
                    try:
                        msgs.append(self._send_queue.get(block=False))
                    except gevent.queue.Empty:
                        break

                for msg in msgs:
                    self._send(msg)

            try:
                msg = uwsgi.websocket_recv_nb()
            except IOError:
                self._select_greenlet.kill()
                return

            if msg:
                return self._decode_received(msg)


_async = {'thread':Thread, 
 'queue':queue.JoinableQueue, 
 'queue_empty':queue.Empty, 
 'event':Event, 
 'websocket':uWSGIWebSocket if _websocket_available else None, 
 'sleep':gevent.sleep}