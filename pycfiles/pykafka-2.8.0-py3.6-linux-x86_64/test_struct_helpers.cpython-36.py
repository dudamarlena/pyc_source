# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pykafka/utils/test_struct_helpers.py
# Compiled at: 2018-08-15 14:22:35
# Size of source mod 2**32: 1041 bytes
import unittest2
from pykafka.utils import struct_helpers

class StructHelpersTests(unittest2.TestCase):

    def test_basic_unpack(self):
        output = struct_helpers.unpack_from('iiqhi', b'\x00\x00\x00\x01\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\n\x00<\x00\x00\x00\x04')
        self.assertEqual(output, (1, 10, 10, 60, 4))

    def test_string_encoding(self):
        output = struct_helpers.unpack_from('S', b'\x00\x04test')
        self.assertEqual(output, (b'test', ))

    def test_bytearray_unpacking(self):
        output = struct_helpers.unpack_from('Y', b'\x00\x00\x00\x04test')
        self.assertEqual(output, (b'test', ))

    def test_array_unpacking(self):
        output = struct_helpers.unpack_from('[i]', b'\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04')
        self.assertEqual(output, [1, 2, 3, 4])


if __name__ == '__main__':
    unittest2.main()