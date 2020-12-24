# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ssb/shs/test_boxstream.py
# Compiled at: 2018-08-07 15:08:49
# Size of source mod 2**32: 3577 bytes
import pytest
from secret_handshake.boxstream import HEADER_LENGTH, BoxStream, UnboxStream
from secret_handshake.util import AsyncBuffer, async_comprehend
from .test_crypto import CLIENT_ENCRYPT_KEY, CLIENT_ENCRYPT_NONCE
MESSAGE_1 = b'\xcev\xedE\x06l\x02\x13\xc8\x17V\xfa\x8bZ?\x88B%O\xb0L\x9f\x8e\x8c0y\x1dv\xc0\xc9\xf6\x9d\xc2\xdf\xdb\xee\x9d'
MESSAGE_2 = b"\x141\xd63\x13d\xd1\xecZ\x9b\xd0\xd4\x03\xcdR?'\xaa.\x89I\x92I\xf9guL\xaa\x06?\xea\xca/}\x88*\xb2"
MESSAGE_3 = b'\xcbYY\xf1\x0f\xa5O\x13r\xa6"\x15\xc5\x9d\r.*\x0b\x92\x10m\xa6(\x0c\x0c\xc61\x80j\x81)\x800\xed\xda\xad\xa1'
MESSAGE_CLOSED = b'\xb1\x14hU\'\xb5M\xa6"\x03\x9duy\xa1\xd4evW,\xdcE\x18\xe4+ C4\xe8h\x96\xed\xc5\x94\x80'

@pytest.mark.asyncio
async def test_boxstream():
    buffer = AsyncBuffer()
    box_stream = BoxStream(buffer, CLIENT_ENCRYPT_KEY, CLIENT_ENCRYPT_NONCE)
    box_stream.write(b'foo')
    buffer.seek(0)
    assert await buffer.read() == MESSAGE_1
    pos = buffer.tell()
    box_stream.write(b'foo')
    buffer.seek(pos)
    assert await buffer.read() == MESSAGE_2
    pos = buffer.tell()
    box_stream.write(b'bar')
    buffer.seek(pos)
    assert await buffer.read() == MESSAGE_3
    pos = buffer.tell()
    box_stream.close()
    buffer.seek(pos)
    assert await buffer.read() == MESSAGE_CLOSED


@pytest.mark.asyncio
async def test_unboxstream():
    buffer = AsyncBuffer(MESSAGE_1 + MESSAGE_2 + MESSAGE_3 + MESSAGE_CLOSED)
    buffer.seek(0)
    unbox_stream = UnboxStream(buffer, CLIENT_ENCRYPT_KEY, CLIENT_ENCRYPT_NONCE)
    assert not unbox_stream.closed
    assert await async_comprehend(unbox_stream) == [b'foo', b'foo', b'bar']
    assert unbox_stream.closed


@pytest.mark.asyncio
async def test_long_packets():
    data_size = 6144
    data = bytes((n % 256 for n in range(data_size)))
    buffer = AsyncBuffer()
    box_stream = BoxStream(buffer, CLIENT_ENCRYPT_KEY, CLIENT_ENCRYPT_NONCE)
    box_stream.write(data)
    assert buffer.tell() == data_size + HEADER_LENGTH * 2
    buffer.seek(0)
    unbox_stream = UnboxStream(buffer, CLIENT_ENCRYPT_KEY, CLIENT_ENCRYPT_NONCE)
    first_packet = await unbox_stream.read()
    assert first_packet == data[:4096]
    second_packet = await unbox_stream.read()
    assert second_packet == data[4096:]