# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/async_drivers/gevent.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 1803 bytes
from __future__ import absolute_import
import gevent
from gevent import queue
from gevent.event import Event
try:
    import geventwebsocket
    _websocket_available = True
except ImportError:
    _websocket_available = False

class Thread(gevent.Greenlet):
    __doc__ = "\n    This wrapper class provides gevent Greenlet interface that is compatible\n    with the standard library's Thread class.\n    "

    def __init__(self, target, args=[], kwargs={}):
        (super(Thread, self).__init__)(target, *args, **kwargs)

    def _run(self):
        return self.run()


class WebSocketWSGI(object):
    __doc__ = "\n    This wrapper class provides a gevent WebSocket interface that is\n    compatible with eventlet's implementation.\n    "

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'wsgi.websocket' not in environ:
            raise RuntimeError('You need to use the gevent-websocket server. See the Deployment section of the documentation for more information.')
        self._sock = environ['wsgi.websocket']
        self.environ = environ
        self.version = self._sock.version
        self.path = self._sock.path
        self.origin = self._sock.origin
        self.protocol = self._sock.protocol
        return self.app(self)

    def close(self):
        return self._sock.close()

    def send(self, message):
        return self._sock.send(message)

    def wait(self):
        return self._sock.receive()


_async = {'thread':Thread, 
 'queue':queue.JoinableQueue, 
 'queue_empty':queue.Empty, 
 'event':Event, 
 'websocket':WebSocketWSGI if _websocket_available else None, 
 'sleep':gevent.sleep}