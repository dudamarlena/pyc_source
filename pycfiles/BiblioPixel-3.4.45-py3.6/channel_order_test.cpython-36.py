# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/channel_order_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 988 bytes
from .base import TypesBaseTest
from bibliopixel.drivers import channel_order

class ChannelOrderTypesTest(TypesBaseTest):

    def test_some(self):

        def test(i, *cases):
            expected = channel_order.ChannelOrder.ORDERS[i]
            for case in cases:
                actual = self.make('c_order', case)['c_order']
                self.assertIs(expected, actual)

        test(0, 'rgb', (0, 1, 2), [0, 1, 2], '012')
        test(5, 'bgr', (2, 1, 0), [2, 1, 0], 'b1R')
        with self.assertRaises(IndexError):
            self.make('c_order', -1)
        with self.assertRaises(IndexError):
            self.make('c_order', 6)
        with self.assertRaises(KeyError):
            self.make('c_order', 'NONE')
        with self.assertRaises(ValueError):
            self.make('c_order', 'RGG')
        with self.assertRaises(ValueError):
            self.make('c_order', None)
        with self.assertRaises(ValueError):
            self.make('c_order', [1, 2])