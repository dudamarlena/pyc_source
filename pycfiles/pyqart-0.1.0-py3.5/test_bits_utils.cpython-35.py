# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_bits_utils.py
# Compiled at: 2016-08-03 05:22:46
# Size of source mod 2**32: 3070 bytes
import unittest
from pyqart.common.bit_funcs import one_at, zero_at, set_bit, bit_at

class TestBitUtils(unittest.TestCase):

    def test_one_at_normal(self):
        self.assertEqual(one_at(0), 128)
        self.assertEqual(one_at(3), 16)
        self.assertEqual(one_at(4), 8)
        self.assertEqual(one_at(7), 1)
        self.assertEqual(one_at(0, 12), 2048)
        self.assertEqual(one_at(5, 10), 16)
        self.assertEqual(one_at(8, 10), 2)

    def test_one_at_fail(self):
        with self.assertRaises(AssertionError):
            one_at(-1)
        with self.assertRaises(AssertionError):
            one_at(-2)
        with self.assertRaises(AssertionError):
            one_at(8)
        with self.assertRaises(AssertionError):
            one_at(10, 8)
        with self.assertRaises(AssertionError):
            one_at(10, 9)

    def test_zero_at_normal(self):
        self.assertEqual(zero_at(0), 127)
        self.assertEqual(zero_at(3), 239)
        self.assertEqual(zero_at(4), 247)
        self.assertEqual(zero_at(7), 254)
        self.assertEqual(zero_at(10, 12), 4093)
        self.assertEqual(zero_at(0, 12), 2047)
        self.assertEqual(zero_at(7, 8), 254)

    def test_zero_at_fail(self):
        with self.assertRaises(AssertionError):
            zero_at(-1)
        with self.assertRaises(AssertionError):
            zero_at(-2)
        with self.assertRaises(AssertionError):
            zero_at(8)
        with self.assertRaises(AssertionError):
            zero_at(10)
        with self.assertRaises(AssertionError):
            zero_at(10, 9)
        with self.assertRaises(AssertionError):
            zero_at(10, 10)

    def test_set_bit_normal(self):
        self.assertEqual(set_bit(74, 2, True), 106)
        self.assertEqual(set_bit(74, 6, False), 72)

    def test_set_bit_fail(self):
        with self.assertRaises(AssertionError):
            set_bit(0, -1, True)
        with self.assertRaises(AssertionError):
            set_bit(0, -2, True)
        with self.assertRaises(AssertionError):
            set_bit(0, 8, False)
        with self.assertRaises(AssertionError):
            set_bit(0, 9, False)

    def test_bit_at_normal(self):
        self.assertEqual(bit_at(12, 5, 0), False)
        self.assertEqual(bit_at(12, 5, 1), True)
        self.assertEqual(bit_at(45, 6, 1), False)
        self.assertEqual(bit_at(45, 6, 5), True)
        self.assertEqual(bit_at(247, 8, 4), False)
        self.assertEqual(bit_at(247, 8, 7), True)

    def test_bit_at_fail(self):
        with self.assertRaises(AssertionError):
            self.assertEqual(bit_at(0, 0, 0), False)
        with self.assertRaises(AssertionError):
            self.assertEqual(bit_at(0, -1, 0), False)
        with self.assertRaises(AssertionError):
            self.assertEqual(bit_at(0, -5, 0), False)