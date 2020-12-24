# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/test_jsonutil.py
# Compiled at: 2019-06-26 11:58:00
import unittest
from decimal import Decimal
from pyutil import jsonutil
zero_point_one = Decimal('0.1')

class TestDecimal(unittest.TestCase):

    def test_encode(self):
        self.assertEqual(jsonutil.dumps(zero_point_one), '0.1')

    def test_decode(self):
        self.assertEqual(jsonutil.loads('0.1'), zero_point_one)

    def test_no_exception_on_convergent_parse_float(self):
        self.assertEqual(jsonutil.loads('0.1', parse_float=Decimal), zero_point_one)