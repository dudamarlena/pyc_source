# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/config/gunicorn.py
# Compiled at: 2016-02-18 14:56:34
# Size of source mod 2**32: 3976 bytes
import asyncio, inspect, functools, websockets, gunicorn
from pyramid.response import Response
from aiopyramid.config import AsyncioMapperBase

def _connection_closed_to_none(func):
    """
    A backwards compatibility shim for websockets 3+. We need to
    still return `None` rather than throwing an exception in order
    to unite the interface with uWSGI even though the exception is
    more Pythonic.
    """

    @asyncio.coroutine
    @functools.wraps(func)
    def _connection_closed_to_none_inner(*args, **kwargs):
        try:
            msg = yield from func(*args, **kwargs)
        except websockets.exceptions.ConnectionClosed:
            msg = None

        return msg

    return _connection_closed_to_none_inner


def _use_bytes(func):
    """
    Encodes strings received from websockets to bytes to
    provide consistency with uwsgi since we don't have access
    to the raw WebsocketFrame.
    """

    @asyncio.coroutine
    @functools.wraps(func)
    def _use_bytes_inner(*args, **kwargs):
        data = yield from func(*args, **kwargs)
        if isinstance(data, str):
            return str.encode(data)
        else:
            return data

    return _use_bytes_inner


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

        def get_header(k):
            return environ[('HTTP_' + k.upper().replace('-', '_'))]

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
    use_bytes = False

    def launch_websocket_view(self, view):

        def websocket_view(context, request):
            if inspect.isclass(view):
                view_callable = view(context, request)
            else:
                view_callable = view

            @asyncio.coroutine
            def _ensure_ws_close(ws):
                if WebsocketMapper.use_bytes:
                    ws.recv = _use_bytes(ws.recv)
                ws.recv = _connection_closed_to_none(ws.recv)
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