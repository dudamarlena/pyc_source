# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\crccheck\base.py
# Compiled at: 2016-04-03 03:40:14
__doc__ = ' Base class for CRC and checksum classes.\n\n  License::\n\n    Copyright (C) 2015-2016 by Martin Scharrer <martin@scharrer-online.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
import math
REFLECT_BIT_ORDER_TABLE = (0, 128, 64, 192, 32, 160, 96, 224, 16, 144, 80, 208, 48,
                           176, 112, 240, 8, 136, 72, 200, 40, 168, 104, 232, 24,
                           152, 88, 216, 56, 184, 120, 248, 4, 132, 68, 196, 36,
                           164, 100, 228, 20, 148, 84, 212, 52, 180, 116, 244, 12,
                           140, 76, 204, 44, 172, 108, 236, 28, 156, 92, 220, 60,
                           188, 124, 252, 2, 130, 66, 194, 34, 162, 98, 226, 18,
                           146, 82, 210, 50, 178, 114, 242, 10, 138, 74, 202, 42,
                           170, 106, 234, 26, 154, 90, 218, 58, 186, 122, 250, 6,
                           134, 70, 198, 38, 166, 102, 230, 22, 150, 86, 214, 54,
                           182, 118, 246, 14, 142, 78, 206, 46, 174, 110, 238, 30,
                           158, 94, 222, 62, 190, 126, 254, 1, 129, 65, 193, 33,
                           161, 97, 225, 17, 145, 81, 209, 49, 177, 113, 241, 9,
                           137, 73, 201, 41, 169, 105, 233, 25, 153, 89, 217, 57,
                           185, 121, 249, 5, 133, 69, 197, 37, 165, 101, 229, 21,
                           149, 85, 213, 53, 181, 117, 245, 13, 141, 77, 205, 45,
                           173, 109, 237, 29, 157, 93, 221, 61, 189, 125, 253, 3,
                           131, 67, 195, 35, 163, 99, 227, 19, 147, 83, 211, 51,
                           179, 115, 243, 11, 139, 75, 203, 43, 171, 107, 235, 27,
                           155, 91, 219, 59, 187, 123, 251, 7, 135, 71, 199, 39,
                           167, 103, 231, 23, 151, 87, 215, 55, 183, 119, 247, 15,
                           143, 79, 207, 47, 175, 111, 239, 31, 159, 95, 223, 63,
                           191, 127, 255)

def reflectbitorder(width, value):
    """ Reflects the bit order of the given value according to the given bit width.

        Args:
            width (int): bitwidth
            value (int): value to reflect
    """
    binstr = ('0' * width + bin(value)[2:])[-width:]
    return int(binstr[::-1], 2)


class CrccheckError(Exception):
    """General checksum error exception"""


class CrccheckBase(object):
    """ Abstract base class for checksumming classes.

        Args:
            initvalue (int): Initial value. If None then the default value for the class is used.
    """
    _initvalue = 0
    _check_result = None
    _check_data = None
    _file_chunksize = 512
    _width = 0

    def __init__(self, initvalue=None):
        if initvalue is None:
            self._value = self._initvalue
        else:
            self._value = initvalue
        return

    def reset(self, value=None):
        """ Reset instance.

            Resets the instance state to the initial value.
            This is not required for a just created instance.

            Args:
                value (int): Set internal value. If None then the default initial value for the class is used.

            Returns:
                self
        """
        if value is None:
            self._value = self._initvalue
        else:
            self._value = value
        return self

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        return self

    def final(self):
        """Return final check value.
           The internal state is not modified by this so further data can be processed afterwards.

           Return:
               int: final value
        """
        return self._value

    def finalhex(self, byteorder='big'):
        """Return final checksum value as hexadecimal string (without leading "0x"). The hex value is zero padded to bitwidth/8.
           The internal state is not modified by this so further data can be processed afterwards.

           Return:
               str: final value as hex string without leading '0x'.
        """
        asbytes = self.finalbytes(byteorder)
        try:
            return asbytes.hex()
        except AttributeError:
            return ('').join([ ('{:02x}').format(b) for b in asbytes ])

    def finalbytes(self, byteorder='big'):
        """Return final checksum value as bytes.
           The internal state is not modified by this so further data can be processed afterwards.

           Return:
               bytes: final value as bytes
        """
        bytelength = int(math.ceil(self._width / 8.0))
        asint = self.final()
        try:
            return asint.to_bytes(bytelength, byteorder)
        except AttributeError:
            asbytes = bytearray(bytelength)
            for i in range(0, bytelength):
                asbytes[i] = asint & 255
                asint >>= 8

            if byteorder == 'big':
                asbytes.reverse()
            return asbytes

    def value(self):
        """Returns current intermediate value.
           Note that in general final() must be used to get the a final value.

           Return:
               int: current value
        """
        return self._value

    @classmethod
    def calc(cls, data, initvalue=None, **kwargs):
        """ Fully calculate CRC/checksum over given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.
                initvalue (int): Initial value. If None then the default value for the class is used.

            Return:
                int: final value
        """
        inst = cls(initvalue, **kwargs)
        inst.process(data)
        return inst.final()

    @classmethod
    def calchex(cls, data, initvalue=None, byteorder='big', **kwargs):
        """Fully calculate checksum over given data. Return result as hex string.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.
                initvalue (int): Initial value. If None then the default value for the class is used.
                byteorder ('big' or 'little'): order (endianness) of returned bytes.

            Return:
                str: final value as hex string without leading '0x'.
        """
        inst = cls(initvalue, **kwargs)
        inst.process(data)
        return inst.finalhex(byteorder)

    @classmethod
    def calcbytes(cls, data, initvalue=None, byteorder='big', **kwargs):
        """Fully calculate checksum over given data. Return result as bytearray.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.
                initvalue (int): Initial value. If None then the default value for the class is used.
                byteorder ('big' or 'little'): order (endianness) of returned bytes.

            Return:
                bytes: final value as bytes
        """
        inst = cls(initvalue, **kwargs)
        inst.process(data)
        return inst.finalbytes(byteorder)

    @classmethod
    def selftest(cls, data=None, expectedresult=None, **kwargs):
        """ Selftest method for automated tests.

            Args:
                data (bytes, bytearray or list of int [0-255]): data to process
                expectedresult (int): expected result

            Raises:
                CrccheckError: if result is not as expected
        """
        if data is None:
            data = cls._check_data
            expectedresult = cls._check_result
        result = cls.calc(data, **kwargs)
        if result != expectedresult:
            raise CrccheckError(('{:s}: expected {:s}, got {:s}').format(cls.__name__, hex(expectedresult), hex(result)))
        return