# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/colors/tables_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2100 bytes
import unittest
from bibliopixel.colors import tables, COLORS

class TablesTest(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(tables.get_color('RED'), (255, 0, 0))
        self.assertEqual(tables.get_name((255, 0, 0)), 'red')
        self.assertIs(tables.get_color('rod'), None)

    def test_new_colors(self):
        self.assertIs(tables.get_color('frog'), None)
        frog = (1, 255, 2)
        tables.set_user_colors({'Frog': frog})
        try:
            self.assertEqual(tables.get_color('RED'), (255, 0, 0))
            self.assertEqual(tables.get_name((255, 0, 0)), 'red')
            self.assertEqual(tables.get_color('frog'), frog)
            self.assertEqual(tables.get_name(frog), 'Frog')
        finally:
            tables.set_user_colors({})

        self.assertIs(tables.get_color('frog'), None)

    def test_override_colors(self):
        self.assertEqual(tables.get_color('RED'), (255, 0, 0))
        self.assertEqual(tables.get_name((255, 0, 0)), 'red')
        wrong_red = (6, 6, 6)
        tables.set_user_colors({'red': wrong_red})
        try:
            self.assertEqual(tables.get_color('RED'), wrong_red)
            self.assertEqual(tables.get_name(wrong_red), 'red')
            self.assertEqual(tables.get_name((255, 0, 0)), 'red')
        finally:
            tables.set_user_colors({})

        self.assertEqual(tables.get_color('RED'), (255, 0, 0))
        self.assertEqual(tables.get_name((255, 0, 0)), 'red')

    def test_all_named_colors(self):
        all_colors = sorted(COLORS)
        self.assertEqual(486, len(all_colors))
        actual = all_colors[:4] + all_colors[-4:]
        expected = [
         ('aliceblue', (240, 248, 255)),
         ('amethyst', (153, 102, 204)),
         ('antiquewhite', (250, 235, 215)),
         ('antiquewhite1', (255, 239, 219)),
         ('yellow2', (238, 238, 0)),
         ('yellow3', (205, 205, 0)),
         ('yellow4', (139, 139, 0)),
         ('yellowgreen', (154, 205, 50))]
        self.assertEqual(actual, expected)