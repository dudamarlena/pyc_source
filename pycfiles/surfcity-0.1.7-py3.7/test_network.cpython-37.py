# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssb/shs/test_network.py
# Compiled at: 2018-08-07 15:08:49
# Size of source mod 2**32: 3960 bytes
import os
from asyncio import Event, wait_for
import pytest
from nacl.signing import SigningKey
from secret_handshake.util import AsyncBuffer

class DummyCrypto(object):
    __doc__ = 'Dummy crypto module, pretends everything is fine.'

    def verify_server_challenge(self, data):
        return True

    def verify_challenge(self, data):
        return True

    def verify_server_accept(self, data):
        return True

    def generate_challenge(self):
        return b'CHALLENGE'

    def generate_client_auth(self):
        return b'AUTH'

    def verify_client_auth(self, data):
        return True

    def generate_accept(self):
        return b'ACCEPT'

    def get_box_keys(self):
        return {'encrypt_key':b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 
         'encrypt_nonce':b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 
         'decrypt_key':b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 
         'decrypt_nonce':b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}

    def clean(self):
        pass


def _dummy_boxstream(stream, **kwargs):
    """Identity boxstream, no tansformation."""
    return stream


def _client_stream_mocker():
    reader = AsyncBuffer(b'xxx')
    writer = AsyncBuffer(b'xxx')

    async def _create_mock_streams(host, port):
        return (
         reader, writer)

    return (
     reader, writer, _create_mock_streams)


def _server_stream_mocker():
    reader = AsyncBuffer(b'xxx')
    writer = AsyncBuffer(b'xxx')

    async def _create_mock_server(cb, host, port):
        await cb(reader, writer)

    return (
     reader, writer, _create_mock_server)


@pytest.mark.asyncio
async def test_client(mocker):
    reader, writer, _create_mock_streams = _client_stream_mocker()
    mocker.patch('asyncio.open_connection', new=_create_mock_streams)
    mocker.patch('secret_handshake.boxstream.BoxStream', new=_dummy_boxstream)
    mocker.patch('secret_handshake.boxstream.UnboxStream', new=_dummy_boxstream)
    from secret_handshake import SHSClient
    client = SHSClient('shop.local', 1111, SigningKey.generate(), os.urandom(32))
    client.crypto = DummyCrypto()
    await client.open()
    reader.append(b'TEST')
    assert await client.read() == b'TEST'
    client.disconnect()


@pytest.mark.asyncio
async def test_server(mocker):
    from secret_handshake import SHSServer
    resolve = Event()

    async def _on_connect(conn):
        server.disconnect()
        resolve.set()

    reader, writer, _create_mock_server = _server_stream_mocker()
    mocker.patch('asyncio.start_server', new=_create_mock_server)
    mocker.patch('secret_handshake.boxstream.BoxStream', new=_dummy_boxstream)
    mocker.patch('secret_handshake.boxstream.UnboxStream', new=_dummy_boxstream)
    server = SHSServer('shop.local', 1111, SigningKey.generate(), os.urandom(32))
    server.crypto = DummyCrypto()
    server.on_connect(_on_connect)
    await server.listen()
    await wait_for(resolve.wait(), 5)