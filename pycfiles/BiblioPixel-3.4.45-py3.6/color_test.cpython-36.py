# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/color_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1746 bytes
from .base import TypesBaseTest
from bibliopixel.util import colors
from bibliopixel.project import fields

class ColorTypesTest(TypesBaseTest):

    def test_color_names(self):
        for name in dir(colors):
            if name.istitle():
                c = getattr(colors, name)
                for n in (name, name.lower(), name.upper()):
                    self.make('color', n, c)

    def test_color_numbers(self):
        for i in range(256):
            self.make('color', hex(65793 * i), (i, i, i))

        for c in ([0, 0, 0], [127, 128, 255], [4, 200, 77]):
            self.make('color', c, tuple(c))

        for c in ((0, 0, 0), (127, 128, 255), (4, 200, 77)):
            self.make('color', c, c)
            self.make('color', str(c), c)

    def test_edge_cases(self):
        a = self.make('color', '[0, 0, 0]')
        b = self.make('color', '(0, 0, 0)')
        expected = {'color': (0, 0, 0)}
        self.assertEqual(a, expected)
        self.assertEqual(b, expected)

    def test_errors(self):
        with self.assertRaises(ValueError):
            self.make('color', -1)
        with self.assertRaises(ValueError):
            self.make('color', 256)
        with self.assertRaises(ValueError):
            self.make('color', '')
        with self.assertRaises(ValueError):
            self.make('color', 'dog')
        with self.assertRaises(ValueError):
            self.make('color', ())
        with self.assertRaises(ValueError):
            self.make('color', (1, ))
        with self.assertRaises(ValueError):
            self.make('color', (1, 2))
        self.make('color', (1, 2, 3))
        with self.assertRaises(ValueError):
            self.make('color', (1, 2, 3, 4))