# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\protocol.py
# Compiled at: 2017-03-02 20:32:37
# Size of source mod 2**32: 2539 bytes
"""A basic subclass of asyncio.Protocol using a buffer (for combined / split
irc messages, calls self.client.x for all callback events"""
import asyncio

class ClientProtocol(asyncio.Protocol):
    __doc__ = 'Default protocol, forewards all events to the client'

    def __init__(self, client):
        self.client = client
        self.buffer = bytes()
        self.sockname = None
        self.transport = None

    def connection_made(self, transport):
        """Called on a successful connection, calls client.connection_made"""
        self.sockname = transport.get_extra_info('sockname')
        self.transport = transport
        asyncio.ensure_future(self.client.connection_made())

    def connection_lost(self, exc):
        """Called on a lost connection, calls client.connection_lost"""
        asyncio.ensure_future(self.client.connection_lost(exc))

    def data_received(self, data):
        """Called when data is received, calls client.data_received"""
        self.buffer += data
        pts = self.buffer.split(b'\n')
        self.buffer = pts.pop()
        for el in pts:
            asyncio.ensure_future(self.client.data_received(el))

    async def send(self, message):
        """Send an unencoded message to the server, will be encoded"""
        self.transport.write(message.encode())

    async def send_raw(self, data):
        """Send raw bytes to the server"""
        self.transport.write(data)