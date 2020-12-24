# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/Projects/ControllProxy/seed/mrpackage/udp.py
# Compiled at: 2018-05-29 07:18:43
# Size of source mod 2**32: 8582 bytes
"""Provide high-level UDP endpoints for asyncio.
Example:
async def main():
    # Create a local UDP enpoint
    local = await open_local_endpoint('localhost', 8888)
    # Create a remote UDP enpoint, pointing to the first one
    remote = await open_remote_endpoint(*local.address)
    # The remote endpoint sends a datagram
    remote.send(b'Hey Hey, My My')
    # The local endpoint receives the datagram, along with the address
    data, address = await local.receive()
    # This prints: Got 'Hey Hey, My My' from 127.0.0.1 port 8888
    print(f"Got {data!r} from {address[0]} port {address[1]}")
"""
__all__ = [
 'open_local_endpoint', 'open_remote_endpoint']
import asyncio, warnings

class DatagramEndpointProtocol(asyncio.DatagramProtocol):
    __doc__ = 'Datagram protocol for the endpoint high-level interface.'

    def __init__(self, endpoint):
        self._endpoint = endpoint

    def connection_made(self, transport):
        self._endpoint._transport = transport

    def connection_lost(self, exc):
        if exc is not None:
            msg = 'Endpoint lost the connection: {!r}'
            warnings.warn(msg.format(exc))
        self._endpoint.close()

    def datagram_received(self, data, addr):
        self._endpoint.feed_datagram(data, addr)

    def error_received(self, exc):
        msg = 'Endpoint received an error: {!r}'
        warnings.warn(msg.format(exc))


class BroadcastProtocol:

    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        print('started')
        self._endpoint._transport = transport
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def datagram_received(self, data, addr):
        self._endpoint.feed_datagram(data, addr)

    def broadcast(self, msg):
        print('broadcast:', msg)
        self._endpoint._transport.sendto(string.encode(), ('192.168.1.255', 9000))
        self.loop.call_later(5, self.broadcast)


class Endpoint:
    __doc__ = 'High-level interface for UDP enpoints.\n    Can either be local or remote.\n    It is initialized with an optional queue size for the incoming datagrams.\n    '

    def __init__(self, queue_size=None):
        if queue_size is None:
            queue_size = 0
        self._queue = asyncio.Queue(queue_size)
        self._closed = False
        self._transport = None

    def feed_datagram(self, data, addr):
        try:
            self._queue.put_nowait((data, addr))
        except asyncio.QueueFull:
            warnings.warn('Endpoint queue is full')

    def close(self):
        if self._closed:
            return
        else:
            self._closed = True
            if self._queue.empty():
                self.feed_datagram(None, None)
            if self._transport:
                self._transport.close()

    def send(self, data, addr):
        """Send a datagram to the given address."""
        if addr[0] == '<broadcast>':
            sock = self._transport.get_extra_info('socket')
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if self._closed:
            raise IOError('Enpoint is closed')
        self._transport.sendto(data, addr)

    async def receive(self):
        """Wait for an incoming datagram and return it with
        the corresponding address.
        This method is a coroutine.
        """
        if self._queue.empty():
            if self._closed:
                raise IOError('Enpoint is closed')
        data, addr = await self._queue.get()
        if data is None:
            raise IOError('Enpoint is closed')
        return (
         data, addr)

    def abort(self):
        """Close the transport immediately."""
        if self._closed:
            raise IOError('Enpoint is closed')
        self._transport.abort()
        self.close()

    @property
    def address(self):
        """The endpoint address as a (host, port) tuple."""
        return self._transport._sock.getsockname()

    @property
    def closed(self):
        """Indicates whether the endpoint is closed or not."""
        return self._closed


class LocalEndpoint(Endpoint):
    __doc__ = 'High-level interface for UDP local enpoints.\n    It is initialized with an optional queue size for the incoming datagrams.\n    '


class RemoteEndpoint(Endpoint):
    __doc__ = 'High-level interface for UDP remote enpoints.\n    It is initialized with an optional queue size for the incoming datagrams.\n    '

    def send(self, data):
        super().send(data, None)

    async def receive(self):
        data, addr = await super().receive()
        return data


async def open_datagram_endpoint(host, port, *, endpoint_factory=Endpoint, loop=None, remote=False, **kwargs):
    """Open and return a datagram endpoint.
    The default endpoint factory is the Endpoint class.
    The endpoint can be made local or remote using the remote argument.
    Extra keyword arguments are forwarded to `loop.create_datagram_endpoint`.
    """
    if not loop:
        loop = asyncio.get_event_loop()
    endpoint = endpoint_factory()
    kwargs['remote_addr' if remote else 'local_addr'] = (host, port)
    kwargs['protocol_factory'] = lambda : DatagramEndpointProtocol(endpoint)
    await (loop.create_datagram_endpoint)(**kwargs)
    return endpoint


async def open_local_endpoint(host='0.0.0.0', port=0, *, queue_size=None, **kwargs):
    """Open and return a local datagram endpoint.
    An optional queue size arguement can be provided.
    Extra keyword arguments are forwarded to `loop.create_datagram_endpoint`.
    """
    return await open_datagram_endpoint(
 host, port, remote=False, endpoint_factory=lambda : LocalEndpoint(queue_size), **kwargs)


async def open_remote_endpoint(host, port, *, loop=None, queue_size=None, **kwargs):
    """Open and return a remote datagram endpoint.
    An optional queue size arguement can be provided.
    Extra keyword arguments are forwarded to `loop.create_datagram_endpoint`.
    """
    return await open_datagram_endpoint(
 host, port, remote=True, loop=loop, endpoint_factory=lambda : RemoteEndpoint(queue_size), **kwargs)


try:
    import pytest
    pytestmark = pytest.mark.asyncio
except ImportError:
    pass

async def test_standard_behavior():
    local = await open_local_endpoint()
    remote = await open_remote_endpoint(*local.address)
    remote.send(b'Hey Hey')
    data, address = await local.receive()
    if not data == b'Hey Hey':
        raise AssertionError
    else:
        if not address == remote.address:
            raise AssertionError
        else:
            local.send(b'My My', address)
            data = await remote.receive()
            assert data == b'My My'
            local.abort()
            assert local.closed
        with pytest.warns(UserWarning):
            await asyncio.sleep(0.001)
            remote.send(b'U there?')
            await asyncio.sleep(0.001)
        remote.abort()
        assert remote.closed


async def test_closed_endpoint():
    local = await open_local_endpoint()
    future = asyncio.ensure_future(local.receive())
    local.abort()
    assert local.closed
    with pytest.raises(IOError):
        await future
    with pytest.raises(IOError):
        await local.receive()
    with pytest.raises(IOError):
        await local.send(b'test', ('localhost', 8888))
    with pytest.raises(IOError):
        local.abort()


async def test_queue_size():
    local = await open_local_endpoint(queue_size=1)
    remote = await open_remote_endpoint(*local.address)
    remote.send(b'1')
    remote.send(b'2')
    with pytest.warns(UserWarning):
        await asyncio.sleep(0.001)
        assert await local.receive() == (b'1', remote.address)
    remote.send(b'3')
    if not await local.receive() == (b'3', remote.address):
        raise AssertionError
    else:
        remote.send(b'4')
        await asyncio.sleep(0.001)
        local.abort()
        assert local.closed
        assert await local.receive() == (b'4', remote.address)
        remote.abort()
        assert remote.closed


if __name__ == '__main__':
    pytest.main([__file__])