# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/types/ledtype_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 439 bytes
from bibliopixel.drivers.ledtype import LEDTYPE
from .base import TypesBaseTest

class LEDTYPETypesTest(TypesBaseTest):

    def test_some(self):
        self.make('ledtype', 'LPD8806')
        self.make('ledtype', 'GENERIC')
        self.make('ledtype', LEDTYPE.NEOPIXEL)
        with self.assertRaises(ValueError):
            self.make('ledtype', 2)
        with self.assertRaises(KeyError):
            self.make('ledtype', 'NONE')