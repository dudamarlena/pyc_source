# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/business_tools/tests/test_money.py
# Compiled at: 2011-07-05 05:12:41
import unittest
from decimal import Decimal
from business_tools.money import Money

class TestMoney(unittest.TestCase):

    def test_repr(self):
        ref = Money(Decimal('123456.123456'))
        self.assertEqual(ref.__repr__(), '<Money: 123 456,12>')

    def test_str(self):
        ref = Money(Decimal('123456.123456'))
        self.assertEqual(str(ref), '123 456,12')

    def test_float(self):
        ref = Money(Decimal('123456.123456'))
        self.assertEqual(float(ref), float('123456.12'))

    def test_unicode(self):
        ref = Money(Decimal('123456.123456'))
        self.assertEqual(unicode(ref), '123 456,12')

    def test_human_format(self):
        alist = (
         (
          Decimal('123456.789012345'), '123 456,79'),
         ('123456,789012345', '123 456,79'),
         ('123456,789012345', '123 456,79'),
         (
          float('123456.789012345'), '123 456,79'),
         (
          int(Decimal('123456.789012345')), '123 456'),
         (
          Decimal('-123456.789012345'), '-123 456,79'),
         ('-123456,789012345', '-123 456,79'),
         ('-123456,789012345', '-123 456,79'),
         (
          float('-123456.789012345'), '-123 456,79'),
         (
          int(Decimal('-123456.789012345')), '-123 456'))
        for item in alist:
            self.assert_human_format(item[0], item[1])

    def assert_human_format(self, value, assert_value):
        ref = Money(value)
        self.assertEqual(assert_value, ref.human_format())

    def test_quantize(self):
        test_value = Decimal('987654321.987654321')
        ref = Money(test_value, quantize=None)
        self.assertEqual(test_value, ref.machine_format())
        self.assertEqual('987 654 321,987654321', ref.human_format())
        self.assertRaises(ValueError, Money, test_value, quantize=-2)
        return

    def test_dp(self):
        test_value = Decimal('987654321.987654321')
        ref = Money(test_value, dp=' XXX ')
        self.assertEqual('987 654 321 XXX 99', ref.human_format())

    def test_sep(self):
        test_value = Decimal('987654321.987654321')
        ref = Money(test_value, sep=' thousand ')
        self.assertEqual('987 thousand 654 thousand 321,99', ref.human_format())

    def test_curr(self):
        test_value = Decimal('987654321.987654321')
        ref = Money(test_value, curr='€')
        self.assertEqual('987 654 321,99€', ref.human_format())

    def test_pos_and_neg(self):
        test_value = Decimal('987654321.987654321')
        ref = Money(test_value, pos='POSITIVE: ')
        self.assertEqual('POSITIVE: 987 654 321,99', ref.human_format())
        ref = Money(-test_value, neg='NEGATIVE: ')
        self.assertEqual('NEGATIVE: 987 654 321,99', ref.human_format())

    def test_trailneg(self):
        test_value = Decimal('-987654321.987654321')
        ref = Money(test_value, trailneg='<<<<<')
        self.assertEqual('-987 654 321,99<<<<<', ref.human_format())