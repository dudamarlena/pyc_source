# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/direction_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 623 bytes
from .base import TypesBaseTest

class DirectionTest(TypesBaseTest):

    def test_some(self):

        def test(name, expected):
            actual = self.make('direction', name)['direction']
            self.assertEqual(actual, expected)

        test('up', (0, -1))
        test('r', (1, 0))
        test((-1, 0), (-1, 0))
        test([0, 1], (0, 1))
        with self.assertRaises(ValueError):
            self.make('direction', 'sideways')
        with self.assertRaises(ValueError):
            self.make('direction', None)
        with self.assertRaises(ValueError):
            self.make('direction', (-1, -1))