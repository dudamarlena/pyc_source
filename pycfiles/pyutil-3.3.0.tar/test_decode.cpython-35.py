# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/json_tests/test_decode.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 542 bytes
import decimal
from unittest import TestCase
from pyutil import jsonutil as json

class TestDecode(TestCase):

    def test_decimal(self):
        rval = json.loads('1.1', parse_float=decimal.Decimal)
        self.assert_(isinstance(rval, decimal.Decimal))
        self.assertEqual(rval, decimal.Decimal('1.1'))

    def test_float(self):
        rval = json.loads('1', parse_int=float)
        self.assert_(isinstance(rval, float))
        self.assertEqual(rval, 1.0)