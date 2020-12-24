# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/conrad/prog/galileo-engineio/venv/lib/python3.6/site-packages/engineio/async_drivers/eventlet.py
# Compiled at: 2019-08-30 19:22:57
# Size of source mod 2**32: 981 bytes
from __future__ import absolute_import
from eventlet.green.threading import Thread, Event
from eventlet import queue
from eventlet import sleep
from eventlet.websocket import WebSocketWSGI as _WebSocketWSGI

class WebSocketWSGI(_WebSocketWSGI):

    def __init__(self, *args, **kwargs):
        (super(WebSocketWSGI, self).__init__)(*args, **kwargs)
        self._sock = None

    def __call__(self, environ, start_response):
        if 'eventlet.input' not in environ:
            raise RuntimeError('You need to use the eventlet server. See the Deployment section of the documentation for more information.')
        self._sock = environ['eventlet.input'].get_socket()
        return super(WebSocketWSGI, self).__call__(environ, start_response)


_async = {'thread':Thread, 
 'queue':queue.Queue, 
 'queue_empty':queue.Empty, 
 'event':Event, 
 'websocket':WebSocketWSGI, 
 'sleep':sleep}