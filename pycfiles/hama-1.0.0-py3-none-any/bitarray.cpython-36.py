# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/dict/bitarray.py
# Compiled at: 2020-03-27 13:22:29
# Size of source mod 2**32: 2226 bytes
import math

class BitArray:
    __doc__ = 'Class representing large bit arrays.\n\n    Arrtibutes:\n        BUFF_SIZE: File read buffer size, in bytes.\n        ELEM_SIZE: Each int stored internally is 32 bits, or 4 bytes.\n\n        bits: Internal bit array.\n        size: Bit array size, in bits.\n    '
    BUFF_SIZE = 256
    ELEM_SIZE = 4

    def __init__(self, size):
        super().__init__()
        self.size = size
        bits_per_elem = BitArray.ELEM_SIZE * 8
        self.bits = [0] * math.ceil(self.size / bits_per_elem)

    def read(self, path):
        """Read bit array from file.

        Args:
            file (str): File path.
        """
        with open(path, 'rb') as (f):
            bs = BitArray.BUFF_SIZE
            es = BitArray.ELEM_SIZE
            elems_per_read = bs // es
            counter = 0
            byte = f.read(bs)
            while byte:
                for i in range(elems_per_read):
                    start = i * es
                    end = min(start + es, len(byte))
                    byte_slice = byte[start:end]
                    if byte_slice == b'':
                        break
                    bits_index = counter + i
                    self.bits[bits_index] = int.from_bytes(byte_slice, byteorder='big')

                counter += elems_per_read
                byte = f.read(bs)

    def at(self, index):
        """Returns bit at index

        Args:
            index (int): Index of bit array to query.

        Returns:
            1 is bit is set, 0 if not.
        """
        internal_index = index // 32
        byte_position = index // 8 % 4
        bit_position = 7 - index % 8
        int_bits = self.bits[internal_index]
        byte = int_bits.to_bytes(4, byteorder='big')[byte_position]
        bit = byte >> bit_position & 1
        return bit