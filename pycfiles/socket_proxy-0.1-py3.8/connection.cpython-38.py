# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socket_proxy/connection.py
# Compiled at: 2020-05-03 05:07:12
# Size of source mod 2**32: 1931 bytes
import asyncio, logging
from .base import CLIENT_NAME_SIZE, InvalidPackage
from .package import ClientDataPackage, Package
_logger = logging.getLogger(__name__)

class Connection:

    def __init__(self, reader, writer, token=None, **kwargs):
        (super().__init__)(**kwargs)
        self.reader, self.writer = reader, writer
        self.token = token or b''
        self.bytes_in = self.bytes_out = 0

    @property
    def uuid(self):
        return self.token.hex()

    @classmethod
    async def connect(cls, host, port, token=None, **kwargs):
        streams = await (asyncio.open_connection)(host, port, **kwargs)
        return cls(*streams, **{'token': token})

    async def tun_data(self, token, data):
        if len(token) != CLIENT_NAME_SIZE:
            raise InvalidPackage()
        chunk_size = ClientDataPackage.MAX_SIZE
        for i in range(0, len(data), chunk_size):
            chunk = data[i:][:chunk_size]
            package = ClientDataPackage(chunk, token)
            self.write(package.to_bytes())
            await self.drain()

    async def close(self):
        self.reader.feed_eof()
        self.writer.close()
        await self.writer.wait_closed()

    async def tun_read(self):
        return await Package.from_reader(self)

    async def tun_write(self, package):
        self.write(package.to_bytes())
        await self.drain()

    async def readexactly(self, size):
        data = await self.reader.readexactly(size)
        self.bytes_in += size
        return data

    async def read(self, size):
        data = await self.reader.read(size)
        self.bytes_in += len(data)
        return data

    def write(self, data):
        self.bytes_out += len(data)
        return self.writer.write(data)

    async def drain(self):
        return await self.writer.drain()