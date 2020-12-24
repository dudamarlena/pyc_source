# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/dustmaker/BitReader.py
# Compiled at: 2015-09-27 20:45:09
# Size of source mod 2**32: 1871 bytes


class BitReader:
    __doc__ = ' Allows integers to be read in little endian byte\n      order from a sequence of bytes.\n  '

    def __init__(self, data):
        """ Create a new BitReader using data.

        data -- An indexable list of bytes.
    """
        self.pos = 0
        self.data = data

    def read(self, bits, signed=False):
        """ Reads the next `bits` bits into an integer in little endian order.

        bits -- The number of bits to read.
        signed -- Indicates if the MSB is a sign bit.
    """
        result = 0
        ind = self.pos >> 3
        off = self.pos & 7
        if off != 0:
            result = self.data[ind] >> off
            ind += 1
        shift = 8 - off & 7
        while shift < bits:
            result |= self.data[ind] << shift
            ind += 1
            shift += 8

        result &= (1 << bits) - 1
        if signed:
            if result & 1 << bits - 1 != 0:
                result -= 1 << bits
        self.pos += bits
        return result

    def align(self, size=8):
        """ Aligns the bit stream to a given multiple of bits.
        Default alignment is 8-bit alignment.

        size -- The desired bit alignment.
    """
        self.pos += (size - self.pos % size) % size

    def skip(self, bits):
        """ Skips `bits` bits in the bit stream.

        bits -- the number of bits to skip.
    """
        self.pos += bits

    def more(self):
        """ Returns true if there are more bits to be read. """
        return self.pos < len(self.data) * 8

    def read_bytes(self, num):
        """ Returns a bytes object containing the next `num` bytes from the bit
        stream.

        num -- The number of bytes to extract from the bit stream.
    """
        if self.pos & 7 == 0:
            result = self.data[self.pos >> 3:(self.pos >> 3) + num]
            self.pos += num * 8
        else:
            result = bytearray()
            for i in range(num):
                result.append(self.read(8))

            result = bytes(result)
        return result