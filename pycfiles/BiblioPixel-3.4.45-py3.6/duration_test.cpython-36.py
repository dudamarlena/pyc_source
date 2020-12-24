# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/util/duration_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2157 bytes
import unittest
from bibliopixel.util import duration

class DurationTest(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(duration.parse('1'), 1)
        self.assertEqual(duration.parse('23.5'), 23.5)
        with self.assertRaises(ValueError):
            duration.parse('-23.5')

    def test_simple_units(self):
        self.assertEqual(duration.parse('1s'), 1)
        self.assertEqual(duration.parse('1 s'), 1)
        self.assertEqual(duration.parse('1 sec'), 1)
        self.assertEqual(duration.parse('2 seconds'), 2)
        self.assertEqual(duration.parse('2 seconds'), 2)

    def test_simple_failure(self):
        with self.assertRaises(ValueError):
            duration.parse('1ss')
        with self.assertRaises(ValueError):
            duration.parse('1secondss')
        with self.assertRaises(ValueError):
            duration.parse('1milisecond')
        with self.assertRaises(ValueError):
            duration.parse('1 killosecond')
        with self.assertRaises(ValueError):
            duration.parse('1 milliwombat')
        with self.assertRaises(ValueError):
            duration.parse('')

    def test_complex(self):
        self.assertEqual(duration.parse('2 hours, 3 minutes, 3.5 seconds'), 7383.5)
        self.assertEqual(duration.parse('2 hours, 3 minutes, 3.5 picoseconds'), 7380.000000000004)
        self.assertEqual(duration.parse('2hrs, 3 minutes, 3.5ps'), 7380.000000000004)

    def test_complex_failure(self):
        with self.assertRaises(ValueError):
            duration.parse('2 hourses, 3 minutes, 3.5 seconds')
        with self.assertRaises(ValueError):
            duration.parse('2 hours minutes, 3 minutes, 3.5 seconds')
        with self.assertRaises(ValueError):
            duration.parse('2 3 hours, 3 minutes, 3.5 seconds')
        with self.assertRaises(ValueError):
            duration.parse('hours, 3 minutes, 3.5 seconds')
        with self.assertRaises(ValueError):
            duration.parse('3 hours, 3 minutes, 3.5')