# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_protocol.py
# Compiled at: 2017-12-09 20:11:22
# Size of source mod 2**32: 1834 bytes
import random
from unittest.mock import Mock
from aio_dprcon.protocol import *

def test_ensure_bytes():
    if not ensure_bytes('hello') == 'hello':
        raise AssertionError
    elif not ensure_bytes('hello') == 'hello':
        raise AssertionError


def test_rcon_nosecure_packet():
    p = rcon_nosecure_packet('12345', 'status 1')
    assert p == QUAKE_PACKET_HEADER + 'rcon 12345 status 1'


def test_rcon_secure_time_packet():
    p = rcon_secure_time_packet('12345', 'status 1')
    if not p.startswith(QUAKE_PACKET_HEADER):
        raise AssertionError
    elif not 'srcon' in p:
        raise AssertionError


def test_parse_rcon_response():
    r = parse_rcon_response(b'\xff\xff\xff\xffnhello')
    assert r == 'hello'


class MockTransport:
    sendto = Mock()

    def get_extra_info(self, *args):
        return (
         '127.0.0.1', random.randint(10000, 60000))


def test_protocol_nosecure(dummy_status):
    received_callback = Mock()
    connected_callback = Mock()
    rp = create_rcon_protocol('12345', 0, received_callback, connected_callback)()
    rp.connection_made(MockTransport())
    if not connected_callback.called:
        raise AssertionError
    else:
        rp.datagram_received(RCON_RESPONSE_HEADER + dummy_status, ('127.0.0.1', 26000))
        assert received_callback.called
        assert received_callback.call_args[0][0] == dummy_status
        assert received_callback.call_args[0][1] == ('127.0.0.1', 26000)
        rp.send('status 1')
        assert rp.transport.sendto.called
        assert rp.transport.sendto.call_args[0][0] == QUAKE_PACKET_HEADER + 'rcon 12345 status 1'


def test_protocol_secure_time():
    received_callback = Mock()
    connected_callback = Mock()
    rp = create_rcon_protocol('12345', 1, received_callback, connected_callback)()
    rp.connection_made(MockTransport())
    rp.send('status 1')
    if not rp.transport.sendto.called:
        raise AssertionError
    else:
        msg = rp.transport.sendto.call_args[0][0]
        assert msg.startswith(QUAKE_PACKET_HEADER)
        assert 'srcon' in msg