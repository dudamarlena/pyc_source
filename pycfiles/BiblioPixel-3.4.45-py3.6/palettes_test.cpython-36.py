# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/colors/palettes_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 755 bytes
import unittest
from fractions import Fraction
from bibliopixel.colors import palettes
from bibliopixel.colors.classic import Black, White, Red, Green, Blue

class PalettesTest(unittest.TestCase):

    def test_empty(self):
        self.assertIs(palettes.get('no such name'), None)

    def test_simple(self):
        p = palettes.get('flag')
        self.assertEqual(p[0], Red)
        self.assertEqual(p[1], White)
        self.assertEqual(p[2], Blue)
        self.assertEqual(p.get(0), Red)
        self.assertEqual(p.get(0.99), Red)
        self.assertEqual(p.get(1), White)
        self.assertEqual(p.get(1.99), White)
        self.assertEqual(p.get(2), Blue)
        self.assertEqual(p.get(2.99), Blue)
        self.assertEqual(p.get(3), Red)