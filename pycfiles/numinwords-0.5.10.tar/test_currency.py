# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_currency.py
# Compiled at: 2020-04-17 01:12:15
from decimal import Decimal
from unittest import TestCase
from numinwords.currency import parse_currency_parts

class CurrencyTestCase(TestCase):

    def test_parse_currency_parts(self):
        self.assertEqual(parse_currency_parts(101), (1, 1, False))
        self.assertEqual(parse_currency_parts(-123), (1, 23, True))
        self.assertEqual(parse_currency_parts(101, is_int_with_cents=False), (
         101, 0, False))
        self.assertEqual(parse_currency_parts(-123, is_int_with_cents=False), (
         123, 0, True))
        self.assertEqual(parse_currency_parts(1.01), (1, 1, False))
        self.assertEqual(parse_currency_parts(-1.23), (1, 23, True))
        self.assertEqual(parse_currency_parts(-1.2), (1, 20, True))
        self.assertEqual(parse_currency_parts(0.004), (0, 0, False))
        self.assertEqual(parse_currency_parts(0.005), (0, 1, False))
        self.assertEqual(parse_currency_parts(0.006), (0, 1, False))
        self.assertEqual(parse_currency_parts(0.0005), (0, 0, False))
        self.assertEqual(parse_currency_parts(0.984), (0, 98, False))
        self.assertEqual(parse_currency_parts(0.989), (0, 99, False))
        self.assertEqual(parse_currency_parts(0.994), (0, 99, False))
        self.assertEqual(parse_currency_parts(0.999), (1, 0, False))
        self.assertEqual(parse_currency_parts(Decimal('1.01')), (1, 1, False))
        self.assertEqual(parse_currency_parts(Decimal('-1.23')), (1, 23, True))
        self.assertEqual(parse_currency_parts(Decimal('-1.233')), (
         1, 23, True))
        self.assertEqual(parse_currency_parts(Decimal('-1.989')), (
         1, 99, True))
        self.assertEqual(parse_currency_parts('1.01'), (1, 1, False))
        self.assertEqual(parse_currency_parts('-1.23'), (1, 23, True))
        self.assertEqual(parse_currency_parts('-1.2'), (1, 20, True))
        self.assertEqual(parse_currency_parts('1'), (1, 0, False))