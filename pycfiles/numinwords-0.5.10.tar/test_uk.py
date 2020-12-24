# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_uk.py
# Compiled at: 2020-04-17 01:14:42
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsUKTest(TestCase):

    def test_to_cardinal(self):
        self.maxDiff = None
        self.assertEqual(numinwords(100, lang=b'uk'), b'сто')
        self.assertEqual(numinwords(110, lang=b'uk'), b'сто десять')
        self.assertEqual(numinwords(115, lang=b'uk'), b"сто п'ятнадцять")
        self.assertEqual(numinwords(123, lang=b'uk'), b'сто двадцять три')
        self.assertEqual(numinwords(1000, lang=b'uk'), b'одна тисяча')
        self.assertEqual(numinwords(2012, lang=b'uk'), b'двi тисячi дванадцять')
        self.assertEqual(numinwords(12519.85, lang=b'uk'), b"дванадцять тисяч п'ятсот дев'ятнадцять кома вiсiмдесят п'ять")
        return

    def test_and_join_199(self):
        self.assertEqual(numinwords(187, lang=b'uk'), b'сто вiсiмдесят сiм')

    def test_cardinal_for_float_number(self):
        self.assertEqual(numinwords(12.4, lang=b'uk'), b'дванадцять кома чотири')
        self.assertEqual(numinwords(17.31, lang=b'uk'), b'сiмнадцять кома тридцять одна')
        self.assertEqual(numinwords(14.13, lang=b'uk'), b'чотирнадцять кома тринадцять')
        self.assertEqual(numinwords(12.31, lang=b'uk'), b'дванадцять кома тридцять одна')

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'uk', to=b'ordinal')

    def test_to_currency(self):
        self.assertEqual(numinwords(1.0, lang=b'uk', to=b'currency', currency=b'UAH'), b'одна гривня, нуль копiйок')
        self.assertEqual(numinwords(1234.56, lang=b'uk', to=b'currency', currency=b'EUR'), b"одна тисяча двiстi тридцять чотири євро, п'ятдесят шiсть центiв")
        self.assertEqual(numinwords(1234.56, lang=b'uk', to=b'currency', currency=b'UAH'), b"одна тисяча двiстi тридцять чотири гривнi, п'ятдесят шiсть копiйок")
        self.assertEqual(numinwords(10121, lang=b'uk', to=b'currency', currency=b'UAH', separator=b' та'), b'сто одна гривня та двадцять одна копiйка')
        self.assertEqual(numinwords(10121, lang=b'uk', to=b'currency', currency=b'UAH', separator=b' та'), b'сто одна гривня та двадцять одна копiйка')
        self.assertEqual(numinwords(10122, lang=b'uk', to=b'currency', currency=b'UAH', separator=b' та'), b'сто одна гривня та двадцять двi копiйки')
        self.assertEqual(numinwords(-1251985, lang=b'uk', to=b'currency', currency=b'EUR', cents=False), b"мiнус дванадцять тисяч п'ятсот дев'ятнадцять євро, 85 центiв")
        self.assertEqual(numinwords(b'38.4', lang=b'uk', to=b'currency', separator=b' и', cents=False, currency=b'EUR'), b'тридцять вiсiм євро и 40 центiв')