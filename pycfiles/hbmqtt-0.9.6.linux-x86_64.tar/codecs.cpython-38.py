# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/codecs.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 3349 bytes
import asyncio
from struct import pack, unpack
from hbmqtt.errors import NoDataException

def bytes_to_hex_str(data):
    """
    converts a sequence of bytes into its displayable hex representation, ie: 0x??????
    :param data: byte sequence
    :return: Hexadecimal displayable representation
    """
    return '0x' + ''.join((format(b, '02x') for b in data))


def bytes_to_int(data):
    """
    convert a sequence of bytes to an integer using big endian byte ordering
    :param data: byte sequence
    :return: integer value
    """
    try:
        return int.from_bytes(data, byteorder='big')
    except:
        return data


def int_to_bytes(int_value: int, length: int) -> bytes:
    """
    convert an integer to a sequence of bytes using big endian byte ordering
    :param int_value: integer value to convert
    :param length: (optional) byte length
    :return: byte sequence
    """
    if length == 1:
        fmt = '!B'
    else:
        if length == 2:
            fmt = '!H'
    return pack(fmt, int_value)


@asyncio.coroutine
def read_or_raise(reader, n=-1):
    """
    Read a given byte number from Stream. NoDataException is raised if read gives no data
    :param reader: reader adapter
    :param n: number of bytes to read
    :return: bytes read
    """
    data = yield from reader.read(n)
    if not data:
        raise NoDataException('No more data')
    return data
    if False:
        yield None


@asyncio.coroutine
def decode_string(reader) -> bytes:
    """
    Read a string from a reader and decode it according to MQTT string specification
    :param reader: Stream reader
    :return: UTF-8 string read from stream
    """
    length_bytes = yield from read_or_raise(reader, 2)
    str_length = unpack('!H', length_bytes)
    if str_length[0]:
        byte_str = yield from read_or_raise(reader, str_length[0])
        try:
            return byte_str.decode(encoding='utf-8')
        except:
            return str(byte_str)

    else:
        return ''
    if False:
        yield None


@asyncio.coroutine
def decode_data_with_length(reader) -> bytes:
    """
    Read data from a reader. Data is prefixed with 2 bytes length
    :param reader: Stream reader
    :return: bytes read from stream (without length)
    """
    length_bytes = yield from read_or_raise(reader, 2)
    bytes_length = unpack('!H', length_bytes)
    data = yield from read_or_raise(reader, bytes_length[0])
    return data
    if False:
        yield None


def encode_string(string: str) -> bytes:
    data = string.encode(encoding='utf-8')
    data_length = len(data)
    return int_to_bytes(data_length, 2) + data


def encode_data_with_length(data: bytes) -> bytes:
    data_length = len(data)
    return int_to_bytes(data_length, 2) + data


@asyncio.coroutine
def decode_packet_id(reader) -> int:
    """
    Read a packet ID as 2-bytes int from stream according to MQTT specification (2.3.1)
    :param reader: Stream reader
    :return: Packet ID
    """
    packet_id_bytes = yield from read_or_raise(reader, 2)
    packet_id = unpack('!H', packet_id_bytes)
    return packet_id[0]
    if False:
        yield None


def int_to_bytes_str(value: int) -> bytes:
    """
    Converts a int value to a bytes array containing the numeric character.
    Ex: 123 -> b'123'
    :param value: int value to convert
    :return: bytes array
    """
    return str(value).encode('utf-8')