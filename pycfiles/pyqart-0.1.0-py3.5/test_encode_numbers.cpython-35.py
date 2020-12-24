# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_encode_numbers.py
# Compiled at: 2016-08-01 02:33:02
# Size of source mod 2**32: 880 bytes
import unittest
from pyqart.qr.data.numbers import Numbers

class TestNumbers(unittest.TestCase):

    def test_numbers_length_mod_3_is_0(self):
        numbers = Numbers('923576', 10)
        self.assertEqual(numbers.output.as_string, '00010000000110' + '1110011011' + '1001000000')

    def test_numbers_length_mod_3_is_1(self):
        numbers = Numbers('0123456789012345', 10)
        self.assertEqual(numbers.output.as_string, '00010000010000' + '0000001100' + '0101011001' + '1010100110' + '1110000101' + '0011101010' + '0101')

    def test_numbers_length_mod_3_is_2(self):
        numbers = Numbers('01234567', 10)
        self.assertEqual(numbers.output.as_string, '00010000001000' + '000000110001010110011000011')