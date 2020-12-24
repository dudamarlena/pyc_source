# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\crccheck\checksum.py
# Compiled at: 2016-03-31 03:34:51
""" Classes to calculated additive and XOR checksums.

  License::

    Copyright (C) 2015-2016 by Martin Scharrer <martin@scharrer-online.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from crccheck.base import CrccheckBase, CrccheckError

class ChecksumBase(CrccheckBase):
    """ Base class for all checksum classes.

        Args:
            initvalue (int): Initial value. If None then the default value for the class is used.
            byteorder ('big' or 'little'): byte order (endianness) used when reading the input bytes.
    """
    _width = 0
    _mask = 0
    _check_data = (222, 173, 190, 239, 170, 85, 194, 140)
    _check_result_littleendian = None

    def __init__(self, initvalue=0, byteorder='big'):
        super(ChecksumBase, self).__init__(initvalue)
        self._byteorder = byteorder

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        dataword = 0
        n = 0
        bigendian = self._byteorder == 'big'
        width = self._width
        mask = self._mask
        value = self._value
        for byte in data:
            if bigendian:
                dataword = dataword << 8 | byte
            else:
                dataword |= byte << n
            n += 8
            if n == width:
                value = mask & value + dataword
                dataword = 0
                n = 0

        self._value = value
        return self

    @classmethod
    def selftest(cls, data=None, expectedresult=None, byteorder='big'):
        """ Selftest method for automated tests.

            Args:
                data (bytes, bytearray or list of int [0-255]): data to process
                expectedresult (int): expected result
                byteorder ('big' or 'little'): byte order (endianness) used when reading the input bytes.

            Raises:
                CrccheckError: if result is not as expected
        """
        if data is None:
            data = cls._check_data
        if expectedresult is None:
            if byteorder == 'big':
                expectedresult = cls._check_result
            else:
                expectedresult = cls._check_result_littleendian
        result = cls.calc(data, byteorder=byteorder)
        if result != expectedresult:
            raise CrccheckError(hex(result))
        return


class Checksum32(ChecksumBase):
    """ 32-bit checksum.

        Calculates 32-bit checksum by adding the input bytes in groups of four.
        Input data length must be a multiple of four, otherwise the last bytes are not used.
    """
    _width = 32
    _mask = 4294967295
    _check_result = 2298708347
    _check_result_littleendian = 2088829832


class Checksum16(ChecksumBase):
    """ 16-bit checksum.

        Calculates 16-bit checksum by adding the input bytes in groups of two.
        Input data length must be a multiple of two, otherwise the last byte is not used.
    """
    _width = 16
    _mask = 65535
    _check_result = 2685
    _check_result_littleendian = 32776


class Checksum8(ChecksumBase):
    """ 8-bit checksum.

        Calculates 8-bit checksum by adding the input bytes.
    """
    _width = 8
    _mask = 255
    _check_result = 133
    _check_result_littleendian = _check_result


class ChecksumXorBase(ChecksumBase):
    """ Base class for all XOR checksum classes. """

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        dataword = 0
        n = 0
        bigendian = self._byteorder == 'big'
        width = self._width
        mask = self._mask
        value = self._value
        for byte in data:
            if bigendian:
                dataword = dataword << 8 | byte
            else:
                dataword |= byte << n
            n += 8
            if n == width:
                value = mask & (value ^ dataword)
                dataword = 0
                n = 0

        self._value = value
        return self


class ChecksumXor32(ChecksumXorBase):
    """ 32-bit XOR checksum.

        Calculates 32-bit checksum by XOR-ing the input bytes in groups of four.
        Input data length must be a multiple of four, otherwise the last bytes are not used.
    """
    _width = 32
    _mask = 4294967295
    _check_result = 1962441827
    _check_result_littleendian = 1669134452


class ChecksumXor16(ChecksumXorBase):
    """ 16-bit XOR checksum.

        Calculates 16-bit checksum by XOR-ing the input bytes in groups of two.
        Input data length must be a multiple of two, otherwise the last byte is not used.
    """
    _width = 16
    _mask = 65535
    _check_result = 2203
    _check_result_littleendian = 39688


class ChecksumXor8(ChecksumXorBase):
    """ 8-bit XOR checksum.

        Calculates 8-bit checksum by XOR-ing the input bytes.
    """
    _width = 8
    _mask = 255
    _check_result = 147
    _check_result_littleendian = _check_result


class Checksum(ChecksumBase):
    """ General additive checksum.

        Args:
            width (int): bit width of checksum. Must be positive and a multiple of 8.
            initvalue (int): Initial value. If None then the default value for the class is used.
            byteorder ('big' or 'little'): byte order (endianness) used when reading the input bytes.
    """
    _check_result = None
    _check_result_littleendian = None

    def __init__(self, width, initvalue=0, byteorder='big'):
        super(Checksum, self).__init__(initvalue, byteorder)
        width = int(width)
        if width <= 0 or width % 8 != 0:
            raise ValueError('width must be postive and a multiple of 8')
        self._width = width
        self._mask = (1 << width) - 1


class ChecksumXor(ChecksumXorBase):
    """ General XOR checksum.

        Args:
            width (int): bit width of checksum. Must be positive and a multiple of 8.
            initvalue (int): Initial value. If None then the default value for the class is used.
            byteorder ('big' or 'little'): byte order (endianness) used when reading the input bytes.
    """
    _check_result = None
    _check_result_littleendian = None

    def __init__(self, width, initvalue=0, byteorder='big'):
        super(ChecksumXor, self).__init__(initvalue, byteorder)
        width = int(width)
        if width <= 0 or width % 8 != 0:
            raise ValueError('width must be postive and a multiple of 8')
        self._width = width
        self._mask = (1 << width) - 1


ALLCHECKSUMCLASSES = (
 Checksum8, Checksum16, Checksum32,
 ChecksumXor8, ChecksumXor16, ChecksumXor32)