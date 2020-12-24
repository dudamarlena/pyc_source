# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/types/bytearray.py
# Compiled at: 2017-06-28 12:32:16
# Size of source mod 2**32: 4384 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_type, verify_value
from wasp_general.types.binarray import WBinArray

class WFixedSizeByteArray:
    __doc__ = ' This class represent fixed-length byte-array. Where byte is WBinArray. Bytes are ordered as big-endian.\n\tIt means that the most significant byte has index 0.\n\n\tsee also https://en.wikipedia.org/wiki/Endianness\n\t'
    byte_size = 8

    @verify_type(size=int, value=(WBinArray, int, bytes, None))
    @verify_value(size=lambda x: x >= 0)
    def __init__(self, size=0, value=None):
        """ Construct new array.

                :param size: count of bytes
                :param value: value with which this sequence must be initialized (default 0)
                """
        self._WFixedSizeByteArray__array = []
        self._WFixedSizeByteArray__size = size
        for i in range(self._WFixedSizeByteArray__size):
            self._WFixedSizeByteArray__array.append(WBinArray(0, self.__class__.byte_size))

        if value is not None:
            if isinstance(value, (WBinArray, int)) is True:
                value = WBinArray(int(value), self._WFixedSizeByteArray__size * self.__class__.byte_size)
                value = value.split(self.__class__.byte_size)
        else:
            if self._WFixedSizeByteArray__size < len(value):
                raise OverflowError('Value is out of bound')
            for i in range(len(value)):
                self._WFixedSizeByteArray__array[i] = value[i]

    def bin_value(self):
        """ Return this sequence as single big WBinArray

                :return: WBinArray
                """
        return WBinArray.join(*self._WFixedSizeByteArray__array)

    def bin_array(self):
        """ Return this sequence as list of bytes (WBinArray)

                :return: list of WBinArray
                """
        return self._WFixedSizeByteArray__array

    def resize(self, size):
        """ Grow this array to specified length. This array can't be shrinked

                :param size: new length
                :return: None
                """
        if size < len(self):
            raise ValueError("Value is out of bound. Array can't be shrinked")
        current_size = self._WFixedSizeByteArray__size
        for i in range(size - current_size):
            self._WFixedSizeByteArray__array.append(WBinArray(0, self.__class__.byte_size))

        self._WFixedSizeByteArray__size = size

    def __len__(self):
        """ Return count of bytes

                :return: int
                """
        return self._WFixedSizeByteArray__size

    def __str__(self):
        """ Convert to string

                :return: str
                """
        return str([str(x) for x in self._WFixedSizeByteArray__array])

    def __getitem__(self, item):
        """ Return byte (WBinArray) at specified index

                :param item: item index
                :return: WBinArray
                """
        return self._WFixedSizeByteArray__array[item]

    @verify_type('paranoid', value=(WBinArray, int))
    @verify_type(key=int)
    def __setitem__(self, key, value):
        """ Set value for the given index. Specified value must resign within byte capability (must be non
                negative and be less then 2^<byte_size>).

                :param key: item index
                :param value: value to set
                :return: None
                """
        if key < 0 or key >= len(self):
            raise IndexError('Index out of range')
        self._WFixedSizeByteArray__array[key] = WBinArray(value, self.__class__.byte_size)

    def __bytes__(self):
        """ Convert to bytes

                :return: bytes
                """
        return bytes([int(x) for x in self._WFixedSizeByteArray__array])

    def swipe(self):
        """ Mirror current array value in reverse. Bytes that had greater index will have lesser index, and
                vice-versa. This method doesn't change this array. It creates a new one and return it as a result.

                :return: WFixedSizeByteArray
                """
        result = WFixedSizeByteArray(len(self))
        for i in range(len(self)):
            result[len(self) - i - 1] = self[i]

        return result