# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Code/plpygis/plpygis/hex.py
# Compiled at: 2020-02-21 00:16:30
# Size of source mod 2**32: 2676 bytes
from binascii import hexlify, unhexlify
from struct import calcsize, unpack_from, pack

class HexReader:
    __doc__ = '\n    A reader for generic hex data. The current position in the stream of bytes\n    will be retained as data is read.\n    '

    def __init__(self, hexdata, order, offset=0):
        self._data = hexdata
        self._order = order
        self._ini_offset = offset
        self._cur_offset = offset

    def reset(self):
        """
        Start reading from the initial position again.

        :rtype: int
        """
        self._cur_offset = self._ini_offset

    def _get_value(self, fmt):
        value = unpack_from('{}{}'.format(self._order, fmt), self._data, self._cur_offset)[0]
        self._cur_offset += calcsize(fmt)
        return value

    def get_char(self):
        return self._get_value('B')

    def get_int(self):
        """
        Get the next four-byte integer from the stream of bytes.

        :rtype: int
        """
        return self._get_value('I')

    def get_double(self):
        """
        Get the next double from the stream of bytes.

        :rtype: int
        """
        return self._get_value('d')


class HexWriter:

    def __init__(self, order):
        self._fmts = []
        self._values = []
        self._order = order

    def _add_value(self, fmt, value):
        self._fmts.append(fmt)
        self._values.append(value)

    def add_order(self):
        if self._order == '<':
            self.add_char(1)
        else:
            self.add_char(0)

    def add_char(self, value):
        self._add_value('B', value)

    def add_int(self, value):
        self._add_value('I', value)

    def add_double(self, value):
        self._add_value('d', value)

    @property
    def data(self):
        fmt = self._order + ''.join(self._fmts)
        data = pack(fmt, *self._values)
        return HexBytes(data)


class HexBytes(bytes):
    __doc__ = 'A subclass of bytearray that represents binary WKB data.\n    It can be converted to a hexadecimal representation of the data using str()\n    and compared to a hexadecimal representation with the normal equality operator.'

    def __new__(cls, data):
        if not isinstance(data, (bytes, bytearray)):
            data = unhexlify(str(data))
        else:
            if data[:2] in (b'00', b'01'):
                data = unhexlify(data.decode('ascii'))
        return bytes.__new__(cls, data)

    def __str__(self):
        return hexlify(self).decode('ascii')

    def __eq__(self, other):
        if isinstance(other, str):
            if other[:2] in ('00', '01'):
                other = unhexlify(other)
        return super(HexBytes, self).__eq__(other)