# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: class.py
# Compiled at: 2017-04-28 17:17:47
import unittest.mock

class ProductionClass:

    def method(self):
        self.something(1, 2, 3)

    def something(self, a, b, c):
        pass


real = ProductionClass()
real.something = MagicMock()
real.method()
real.something.assert_called_once_with(1, 2, 3)