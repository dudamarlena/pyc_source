# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/view.py
# Compiled at: 2014-12-06 15:08:06
# Size of source mod 2**32: 1134 bytes
import asyncio

class WebsocketConnectionView:
    """WebsocketConnectionView"""

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