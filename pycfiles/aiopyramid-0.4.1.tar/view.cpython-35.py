# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/view.py
# Compiled at: 2014-12-06 15:08:06
# Size of source mod 2**32: 1134 bytes
import asyncio

class WebsocketConnectionView:
    __doc__ = ' :term:`view callable` for websocket connections. '

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @asyncio.coroutine
    def __call__(self, ws):
        self.ws = ws
        yield from self.on_open()
        while True:
            message = yield from self.ws.recv()
            if message is None:
                yield from self.on_close()
                break
            yield from self.on_message(message)

    @asyncio.coroutine
    def send(self, message):
        yield from self.ws.send(message)

    @asyncio.coroutine
    def on_message(self, message):
        """
        Callback called when a message is received.
        Default is a noop.
        """
        pass

    @asyncio.coroutine
    def on_open(self):
        """
        Callback called when the connection is first established.
        Default is a noop.
        """
        pass

    @asyncio.coroutine
    def on_close(self):
        """
        Callback called when the connection is closed.
        Default is a noop.
        """
        pass