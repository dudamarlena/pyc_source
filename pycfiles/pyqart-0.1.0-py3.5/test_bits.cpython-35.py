# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_bits.py
# Compiled at: 2016-07-29 09:24:11
# Size of source mod 2**32: 2560 bytes
import unittest
from pyqart.common.bits import Bits

class TestBits(unittest.TestCase):

    def test_bits_as_string_when_no_data(self):
        b = Bits()
        self.assertEqual(b.as_string, '')

    def test_bits_as_string_when_has_data(self):
        b = Bits()
        b.append(211, 8)
        self.assertEqual(b.as_string, '11010011')
        b.append(8, 4)
        self.assertEqual(b.as_string, '110100111000')

    def test_bits_as_int_when_no_data(self):
        b = Bits()
        self.assertEqual(b.as_int, -1)

    def test_bits_as_int_when_less_than_a_byte(self):
        b = Bits()
        b.append(1, 1)
        self.assertEqual(b.as_int, 1)

    def test_bits_as_int_when_between_one_and_two_byte(self):
        b = Bits()
        b.append(487, 9)
        self.assertEqual(b.as_int, 487)

    def test_bits_append_bit(self):
        b = Bits()
        b.append_bit(True)
        b.append_bit(True)
        b.append_bit(False)
        b.append_bit(False)
        self.assertEqual(b.as_int, 12)
        b.append_bit(True)
        b.append_bit(False)
        b.append_bit(False)
        b.append_bit(False)
        self.assertEqual(b.as_int, 200)

    def test_bits_append(self):
        b = Bits()
        b.append(172, 8)
        self.assertEqual(b.as_int, 172)
        b.append(15, 4)
        self.assertEqual(b.as_int, 2767)

    def test_bits_extend_all(self):
        b = Bits()
        b.extend(b'\xac')
        self.assertEqual(b.as_int, 172)
        b.extend(bytearray(b'\x1f'))
        self.assertEqual(b.as_int, 44063)

    def test_bits_extend_other_bits_all(self):
        b = Bits()
        b.extend(b'\xac')
        other_bits = Bits.copy_from(b)
        b.extend(other_bits)
        self.assertEqual(b.as_int, 44204)

    def test_bits_extend_other_bytes_0_to_not_end(self):
        b = Bits()
        b.extend(b'\x0f', count=6)
        self.assertEqual(b.as_int, 3)

    def test_bits_extend_other_bytes_not_start_to_end(self):
        b = Bits()
        b.extend(b'\x0f', 4)
        self.assertEqual(b.as_int, 15)

    def test_bits_extend_other_bytes_not_start_to_not_end(self):
        b = Bits()
        b.extend(b'\x0f', 4, 2)
        self.assertEqual(b.as_int, 3)

    def test_bits_xor(self):
        b = Bits(81, 9)
        o = Bits(22, 7)
        b.xor(o, 2, 3, 3)
        self.assertEqual(b.as_string, '001100001')
        b = Bits(81, 9)
        o = Bits(22, 7)
        b.xor(o, 2, 3)
        self.assertEqual(b.as_string, '001100001')