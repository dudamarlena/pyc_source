# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/int_names_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 998 bytes
import unittest
from bibliopixel.util import int_names

class NamesTest(unittest.TestCase):

    def test_to_index(self):
        self.assertEqual(int_names.to_index('H'), 1)
        self.assertEqual(int_names.to_index('hydrogen'), 1)
        self.assertEqual(int_names.to_index('wed'), 3)
        self.assertEqual(int_names.to_index('wednesday'), 3)
        self.assertEqual(int_names.to_index('Pluto'), 9)
        with self.assertRaises(KeyError):
            int_names.to_index('Ploto')
        with self.assertRaises(KeyError):
            int_names.to_index('12.5')
        with self.assertRaises(KeyError):
            int_names.to_index(12.5)

    def test_to_names(self):
        expected = ['Mon', 'Monday', 'Jan', 'January', 'red', 'Mercury', 'H',
         'hydrogen']
        self.assertEqual(int_names.to_names(1), expected)
        self.assertEqual(int_names.to_names(98), ['Cf', 'californium'])
        with self.assertRaises(KeyError):
            int_names.to_names(126)