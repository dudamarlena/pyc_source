# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\henrio\protocols.py
# Compiled at: 2017-12-17 23:46:07
# Size of source mod 2**32: 11642 bytes
import ssl, sys
from collections import defaultdict, deque
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, socket
from typing import Callable
from .yields import create_writer, create_reader, spawn, remove_writer, remove_reader, get_loop
from .io import async_connect, threaded_bind, ssl_do_handshake
from . import Future
if sys.platform == 'win32':
    from .windows import IOCPLoop
    import _overlapped
__all__ = [
 'ConnectionBase', 'ServerBase', 'SSLServer', 'connect', 'ssl_connect', 'create_server', 'create_ssl_server',
 'ServerSocket']

class ConnectionBase:

    def __init__(self, socket, host, bufsize):
        self.socket = socket
        self.host = host
        self.addr, self.port = host
        self._bufsize = bufsize
        self._writequeue = deque()
        self.closed = False

    async def _reader_callback(self):
        if not self.closed:
            try:
                received = self.socket.recv(self._bufsize)
                if received:
                    await spawn(self.data_received(received))
                    return
                await self._connection_lost()
                await spawn(self.eof_received())
                await spawn(self.connection_lost(None))
            except OSError as e:
                await self._connection_lost()
                await spawn(self.connection_lost(e))

    async def _writer_callback(self):
        while self._writequeue:
            future, data = self._writequeue.popleft()
            ans = self.socket.send(data)
            future.set_result(ans)

    async def _connect(self):
        await async_connect(self.socket, self.host)
        await spawn(self.connection_made())

    async def _connection_lost(self):
        self.closed = True
        loop = await get_loop()
        loop.unregister_reader(self.socket)
        if not isinstance(loop, IOCPLoop):
            await remove_writer(self.socket)
        self.socket.close()

    async def send(self, data):
        loop = await get_loop()
        if isinstance(loop, IOCPLoop):
            future = Future()
            ov = _overlapped.Overlapped(0)
            ov.WSASend(self.socket.fileno(), data, 0)
            loop._writers[ov.address] = future
            return await future
        else:
            future = Future()
            self._writequeue.append((future, data))
            return await future

    async def close(self):
        await self._connection_lost()

    async def connection_made(self):
        pass

    async def data_received(self, data):
        pass

    async def connection_lost(self, exc):
        if exc is not None:
            try:
                raise exc
            except:
                import traceback
                traceback.print_exc()

    async def eof_received(self):
        pass


class ServerBase:

    def __init__(self, socket, host, bufsize):
        self.host = host
        self.address, self.port = host
        self.socket = socket
        self._bufsize = bufsize
        self._writequeue = defaultdict(deque)
        self.connections = list()

    async def _reader_callback(self):
        client, addr = self.socket.accept()
        loop = await get_loop()
        wrapped = ServerSocket(self, client, loop)
        self.connections.append(wrapped)
        await create_reader(wrapped, self._client_readable, wrapped)
        await create_writer(wrapped, self._client_writable, wrapped)
        await spawn(self._connection_made(wrapped))
        await spawn(self.connection_made(wrapped))

    async def _client_writable(self, sock):
        while self._writequeue[sock]:
            future, data = self._writequeue[sock].popleft()
            ans = sock.send(data)
            future.set_result(ans)

    async def _client_readable(self, sock):
        error = None
        try:
            received = sock.recv(self._bufsize)
            if received:
                await spawn(self.data_received(sock, received))
                return
            await spawn(self.eof_received(sock))
        except OSError as e:
            error = e

        if sock in self.connections:
            await self._connection_lost(sock)
            await spawn(self.connection_lost(sock, error))

    async def _connection_made(self, sock):
        await ssl_do_handshake(sock)

    async def _connection_lost(self, sock):
        self.connections.remove(sock)
        await remove_reader(sock)
        await remove_writer(sock)
        sock.close()

    async def connection_made(self, socket):
        pass

    async def data_received(self, socket, data):
        pass

    async def connection_lost(self, socket, exc):
        pass

    async def eof_received(self, socket):
        pass

    async def close(self):
        await remove_reader(self.socket)
        self.socket.close()
        del self._writequeue[self.socket]


class SSLServer(ServerBase):

    def __init__(self, *args, wrap_attrs, **kwargs):
        (super().__init__)(self, *args, **kwargs)
        self.wrap_attrs = wrap_attrs

    async def _reader_callback(self):
        client, addr = self.socket.accept()
        client = (ssl.wrap_socket)(client, **self.wrap_attrs)
        loop = await get_loop()
        wrapped = ServerSocket(self, client, loop)
        self.connections.append(wrapped)
        await create_reader(wrapped, self._client_readable, wrapped)
        await create_writer(wrapped, self._client_writable, wrapped)
        await spawn(self.connection_made(wrapped))


async def connect(protocol_factory: Callable[(..., ConnectionBase)], address: str=None, port: int=None, family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None, bufsize: int=1024, sock: socket=None):
    if sock is not None:
        if fileno is not None:
            raise ValueError('You cannot specify a fileno AND a socket!')
        try:
            sock.getpeername()
            connected = False
        except OSError:
            if address is not None or port is not None:
                raise ValueError('You cannot specify both an address/port AND a connected socket!') from None
            connected = True

    else:
        sock = socket(family=family, type=type, proto=proto, fileno=fileno)
        connected = False
    connection = protocol_factory(socket=sock, host=(address, port), bufsize=bufsize)
    if not connected:
        await connection._connect()
    loop = await get_loop()
    if not isinstance(loop, IOCPLoop):
        await create_writer(sock, connection._writer_callback)
    else:
        if sock.fileno() not in loop._open_ports:
            _overlapped.CreateIoCompletionPort(sock.fileno(), loop._port, 0, 0)
            loop._open_ports.append(sock.fileno())
    await create_reader(sock, connection._reader_callback)
    return connection


async def ssl_connect(protocol_factory, address=None, port=None, bufsize=1024, ssl_context=None):
    if ssl_context is None:
        ssl_context = ssl.create_default_context()
    sock = socket()
    sock = ssl_context.wrap_socket(sock, server_hostname=address)
    connection = protocol_factory(socket=sock, host=(address, port), bufsize=bufsize)
    await connection._connect()
    await ssl_do_handshake(sock)
    await create_writer(sock, connection._writer_callback)
    await create_reader(sock, connection._reader_callback)
    return connection


async def create_server(protocol_factory: Callable[(..., ServerBase)], address, port, family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None, bufsize=1024, sock=None, backlog=None, sockopt: tuple=(
 SOL_SOCKET, SO_REUSEADDR, 1)):
    if sock is not None:
        if fileno is not None:
            raise ValueError('You cannot specify a fileno AND a socket!')
        bound = True
    else:
        sock = socket(family=family, type=type, proto=proto, fileno=fileno)
        bound = False
    connection = protocol_factory(socket=sock, host=(address, port), bufsize=bufsize)
    (sock.setsockopt)(*sockopt)
    await create_reader(sock, connection._reader_callback)
    if not bound:
        await threaded_bind(sock, (address, port))
        sock.listen(backlog) if backlog is not None else sock.listen()
    return connection


async def create_ssl_server(address, port, bufsize=1024, backlog=None, sockopt: tuple=(
 SOL_SOCKET, SO_REUSEADDR, 1), ssl_wrap_attributes=dict(server_side=True)):
    sock = socket()
    bound = False
    connection = SSLServer(socket=sock, host=(address, port), bufsize=bufsize, wrap_attrs=ssl_wrap_attributes)
    (sock.setsockopt)(*sockopt)
    await create_reader(sock, connection._reader_callback)
    if not bound:
        await threaded_bind(sock, (address, port))
        sock.listen(backlog) if backlog is not None else sock.listen()
    return connection


class ServerSocket:

    def __init__(self, protocol, socket, loop):
        """Wraps a socket with async send"""
        self._loop = loop
        self._protocol = protocol
        self._socket = socket

    def send(self, data):
        future = Future()
        self._protocol._writequeue[self].append((future, data))
        return future

    def close(self):
        self._socket.close()
        try:
            del self._protocol._writequeue[self]
        except:
            pass

    def fileno(self):
        return self._socket.fileno()

    def recv(self, bufsize):
        return self._socket.recv(bufsize)