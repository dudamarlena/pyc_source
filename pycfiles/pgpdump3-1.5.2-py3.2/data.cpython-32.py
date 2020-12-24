# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgpdump/data.py
# Compiled at: 2015-08-26 05:57:45
from base64 import b64decode
from .packet import construct_packet
from .utils import PgpdumpException, crc24

class BinaryData(object):
    """The base object used for extracting PGP data packets. This expects fully
    binary data as input; such as that read from a .sig or .gpg file."""
    binary_tag_flag = 128

    def __init__(self, data):
        if not data:
            raise PgpdumpException('no data to parse')
        if len(data) <= 1:
            raise PgpdumpException('data too short')
        data = bytearray(data)
        if not bool(data[0] & self.binary_tag_flag):
            raise PgpdumpException('incorrect binary data')
        self.data = data
        self.length = len(data)

    def packets(self):
        """A generator function returning PGP data packets."""
        offset = 0
        while offset < self.length:
            total_length, packet = construct_packet(self.data, offset)
            offset += total_length
            yield packet

    def __repr__(self):
        return '<%s: length %d>' % (
         self.__class__.__name__, self.length)


class AsciiData(BinaryData):
    """A wrapper class that supports ASCII-armored input. It searches for the
    first PGP magic header and extracts the data contained within."""

    def __init__(self, data):
        self.original_data = data
        if not isinstance(data, bytes):
            data = data.encode()
        data = self.strip_magic(data)
        data, known_crc = self.split_data_crc(data)
        data = bytearray(b64decode(data))
        if known_crc:
            actual_crc = crc24(data)
            if known_crc != actual_crc:
                raise PgpdumpException('CRC failure: known 0x%x, actual 0x%x' % (
                 known_crc, actual_crc))
        super(AsciiData, self).__init__(data)

    @staticmethod
    def strip_magic(data):
        """Strip away the '-----BEGIN PGP SIGNATURE-----' and related cruft so
        we can safely base64 decode the remainder."""
        idx = 0
        magic = b'-----BEGIN PGP '
        ignore = b'-----BEGIN PGP SIGNED '
        while True:
            idx = data.find(magic, idx)
            if data[idx:len(ignore)] != ignore:
                break
            idx += 1

        if idx >= 0:
            nl_idx = data.find(b'\n\n', idx)
            if nl_idx < 0:
                nl_idx = data.find(b'\r\n\r\n', idx)
            if nl_idx < 0:
                raise PgpdumpException('found magic, could not find start of data')
            end_idx = data.find(b'-----', nl_idx)
            if end_idx:
                data = data[nl_idx:end_idx]
            else:
                data = data[nl_idx:]
        return data

    @staticmethod
    def split_data_crc(data):
        """The Radix-64 format appends any CRC checksum to the end of the data
        block, in the form '=alph', where there are always 4 ASCII characters
        correspnding to 3 digits (24 bits). Look for this special case."""
        data = data.rstrip()
        if data[(-5)] in (b'=', ord(b'=')):
            crc = b64decode(data[-4:])
            crc = [ord(c) if isinstance(c, str) else c for c in crc]
            crc = (crc[0] << 16) + (crc[1] << 8) + crc[2]
            return (
             data[:-5], crc)
        else:
            return (
             data, None)