# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/futurefinity/server.py
# Compiled at: 2016-06-10 18:06:56
# Size of source mod 2**32: 3714 bytes
"""
``futurefinity.server`` contains the FutureFinity HTTPServer Class used by
FutureFinity Web Application, which can parse http request, initialize
right RequestHandler and make response to client.
"""
from futurefinity.utils import ensure_str, ensure_bytes, FutureFinityError
from typing import Optional
import futurefinity
from futurefinity import protocol
import asyncio, ssl

class ServerError(FutureFinityError):
    __doc__ = '\n    FutureFinity Server Error.\n\n    All Errors from FutureFinity Server Side are based on this class.\n    '


class HTTPServer(asyncio.Protocol, protocol.BaseHTTPConnectionController):
    __doc__ = '\n    FutureFinity HTTPServer Class.\n\n    :arg allow_keep_alive: Default: `True`. Turn it to `False` if you want to\n      disable keep alive connection for `HTTP/1.1`.\n    '

    def __init__(self, *args, allow_keep_alive: bool=True, **kwargs):
        asyncio.Protocol.__init__(self)
        protocol.BaseHTTPConnectionController.__init__(self)
        self.transport = None
        self.use_tls = False
        self.connection = None
        self.use_h2 = False
        self.allow_keep_alive = allow_keep_alive
        self.sockname = None
        self.peername = None
        self.direct_receiver = None
        self.default_timeout_length = 10
        self._timeout_handler = None

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        context = self.transport.get_extra_info('sslcontext', None)
        if context:
            self.use_tls = True
            if ssl.HAS_ALPN:
                alpn_protocol = context.selected_alpn_protocol()
                if alpn_protocol in ('h2', 'h2-14', 'h2-15', 'h2-16', 'h2-17'):
                    self.use_h2 = True
        else:
            if alpn_protocol is not None:
                self.transport.close()
                raise ServerError('Unsupported Protocol')
            self.sockname = self.transport.get_extra_info('sockname')
            self.peername = self.transport.get_extra_info('peername')
            if self.use_h2:
                self.transport.close()
                raise ServerError('Unsupported Protocol')
            else:
                self.connection = protocol.HTTPv1Connection(controller=self, is_client=False, use_tls=self.use_tls, sockname=self.sockname, peername=self.peername, allow_keep_alive=self.allow_keep_alive)
        self.set_timeout_handler()

    def set_timeout_handler(self):
        self.cancel_timeout_handler()
        self._timeout_handler = self._loop.call_later(self.default_timeout_length, self.transport.close)

    def cancel_timeout_handler(self):
        if self._timeout_handler is not None:
            self._timeout_handler.cancel()
        self._timeout_handler = None

    def data_received(self, data: bytes):
        self.connection.data_received(data)

    def connection_lost(self, exc: Optional[tuple]):
        self.connection.connection_lost(exc)
        self.cancel_timeout_handler()