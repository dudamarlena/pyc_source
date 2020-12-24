# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/windmill/dep/_simplejson/tests/test_decode.py
# Compiled at: 2011-01-13 01:48:00
import decimal
from unittest import TestCase
import simplejson as json

class TestDecode(TestCase):

    def test_decimal(self):
        rval = json.loads('1.1', parse_float=decimal.Decimal)
        self.assert_(isinstance(rval, decimal.Decimal))
        self.assertEquals(rval, decimal.Decimal('1.1'))

    def test_float(self):
        rval = json.loads('1', parse_int=float)
        self.assert_(isinstance(rval, float))
        self.assertEquals(rval, 1.0)

    def test_decoder_optimizations(self):
        rval = json.loads('{   "key"    :    "value"    ,  "k":"v"    }')
        self.assertEquals(rval, {'key': 'value', 'k': 'v'})