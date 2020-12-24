# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/gamma_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 658 bytes
from .base import TypesBaseTest
from bibliopixel.colors import gamma

class GammaTypesTest(TypesBaseTest):

    def test_some(self):
        self.make('gamma', 'LPD8806', gamma.LPD8806)
        self.make('gamma', 'DEFAULT', gamma.DEFAULT)
        gam = self.make('gamma', {'gamma':2.5,  'offset':0.5})
        self.assertEqual(gam['gamma'].table, gamma.APA102.table)
        gam = self.make('gamma', [2.5, 0.5, 128])
        self.assertEqual(gam['gamma'].table, gamma.LPD8806.table)
        with self.assertRaises(TypeError):
            self.make('gamma', [0, 1, 2, 3])
        with self.assertRaises(ValueError):
            self.make('gamma', None)