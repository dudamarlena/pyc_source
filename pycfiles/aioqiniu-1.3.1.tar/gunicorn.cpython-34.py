# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/config/gunicorn.py
# Compiled at: 2014-10-03 14:15:23
# Size of source mod 2**32: 2699 bytes
import asyncio, inspect, websockets, gunicorn
from pyramid.response import Response
from aiopyramid.config import AsyncioMapperBase

class HandshakeInterator:

    def __init__(self, app_iter):
        self.content = list(app_iter)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            try:
                return self.content[self.index]
            except IndexError:
                raise StopIteration

        finally:
            self.index += 1


class SwitchProtocolsResponse(Response):
    """SwitchProtocolsResponse"""

    def __init__(self, environ, switch_protocols):
        super().__init__()
        self.status_int = 101
        http_1_1 = environ['SERVER_PROTOCOL'] == 'HTTP/1.1'
        get_header = lambda k: environ[('HTTP_' + k.upper().replace('-', '_'))]
        key = websockets.handshake.check_request(get_header)
        if not http_1_1 or key is None:
            self.status_int = 400
            self.content = 'Invalid WebSocket handshake.\n'
        else:
            set_header = self.headers.__setitem__
            websockets.handshake.build_response(set_header, key)
            self.app_iter = HandshakeInterator(self.app_iter)
            self.app_iter.close = switch_protocols


class WebsocketMapper(AsyncioMapperBase):

    def launch_websocket_view(self, view):

        def websocket_view(context, request):
            if inspect.isclass(view):
                view_callable = view(context, request)
            else:
                view_callable = view

            @asyncio.coroutine
            def _ensure_ws_close(ws):
                yield from view_callable(ws)
                yield from ws.close()

            def switch_protocols():
                ws_protocol = websockets.WebSocketCommonProtocol()
                transport = request.environ['async.writer'].transport
                http_protocol = request.environ['async.protocol']
                http_protocol.connection_lost(None)
                transport._protocol = ws_protocol
                ws_protocol.connection_made(transport)
                asyncio.async(_ensure_ws_close(ws_protocol))

            response = SwitchProtocolsResponse(request.environ, switch_protocols)
            response.body = response.body
            return response

        return websocket_view

    def __call__(self, view):
        """ Accepts a view_callable class. """
        return self.launch_websocket_view(view)