# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_alphanumeric.py
# Compiled at: 2016-08-01 02:33:02
# Size of source mod 2**32: 605 bytes
import unittest
from pyqart.qr.data.alphanumeric import AlphaNumeric

class TestAlphaNumeric(unittest.TestCase):

    def test_alphanumeric_odd(self):
        an = AlphaNumeric('AC-42', 9)
        self.assertEqual(an.output.as_string, '0010000000101' + '00111001110' + '11100111001' + '000010')

    def test_alphanumeric_even(self):
        an = AlphaNumeric('7S DREAM', 9)
        self.assertEqual(an.output.as_string, '0010000001000' + '00101010111' + '11001100001' + '10011001101' + '00111011000')