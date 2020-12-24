# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/dustmaker/BitWriter.py
# Compiled at: 2015-10-01 18:56:07
# Size of source mod 2**32: 1650 bytes


class BitWriter:
    __doc__ = ' Allows integers to be written in little endian byte\n      order into a bytes object.\n  '

    def __init__(self):
        """ Create a new empty BitWriter. """
        self.pos = 0
        self.data = bytearray()

    def write(self, bits, val):
        """ Writes `val` as a `bits` bit integer in little endian order to the
        bit stream.

        bits -- The number of bits in `val`.
        val -- The value of the integer.
    """
        if val < 0:
            val += 1 << bits
        off = self.pos & 7
        self.pos += bits
        if off != 0:
            cnt = min(8 - off, bits)
            self.data[(-1)] |= (val & (1 << cnt) - 1) << off
            bits -= cnt
            val = val >> cnt
        while bits >= 8:
            self.data.append(val & 255)
            val = val >> 8
            bits -= 8

        if bits != 0:
            self.data.append(val & (1 << bits) - 1)

    def bytes(self):
        """ Returns a bytes object containing all written data so far. """
        return bytes(self.data)

    def byte_count(self):
        """ Returns the number of bytse written so far. """
        return len(self.data)

    def align(self, size=8):
        """ Aligns the bit stream to a given multiple of bits.
        Default alignment is 8-bit alignment.

        size -- The desired bit alignment.
    """
        self.pos += (size - self.pos % size) % size
        while len(self.data) * 8 < self.pos:
            self.data.append(0)

    def write_bytes(self, data):
        """ Write the bytes given by `data` to the stream.

        data -- The bytes to write to the stream.
    """
        if self.pos & 7 == 0:
            self.data += data
            self.pos += 8 * len(data)
        else:
            for x in data:
                self.write(8, x)