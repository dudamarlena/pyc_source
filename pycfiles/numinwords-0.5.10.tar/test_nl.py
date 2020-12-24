# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_nl.py
# Compiled at: 2020-04-17 01:13:41
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords
from numinwords.lang_NL import Num2Word_NL

class numinwordsNLTest(TestCase):

    def test_ordinal_less_than_twenty(self):
        self.assertEqual(numinwords(7, ordinal=True, lang=b'nl'), b'zevende')
        self.assertEqual(numinwords(8, ordinal=True, lang=b'nl'), b'achtste')
        self.assertEqual(numinwords(12, ordinal=True, lang=b'nl'), b'twaalfde')
        self.assertEqual(numinwords(17, ordinal=True, lang=b'nl'), b'zeventiende')

    def test_ordinal_more_than_twenty(self):
        self.assertEqual(numinwords(81, ordinal=True, lang=b'nl'), b'eenentachtigste')

    def test_ordinal_at_crucial_number(self):
        self.assertEqual(numinwords(100, ordinal=True, lang=b'nl'), b'honderdste')
        self.assertEqual(numinwords(1000, ordinal=True, lang=b'nl'), b'duizendste')
        self.assertEqual(numinwords(4000, ordinal=True, lang=b'nl'), b'vierduizendste')
        self.assertEqual(numinwords(2000000, ordinal=True, lang=b'nl'), b'twee miljoenste')
        self.assertEqual(numinwords(5000000000, ordinal=True, lang=b'nl'), b'vijf miljardste')

    def test_cardinal_at_some_numbers(self):
        self.assertEqual(numinwords(82, lang=b'nl'), b'tweeëntachtig')
        self.assertEqual(numinwords(1013, lang=b'nl'), b'duizenddertien')
        self.assertEqual(numinwords(2000000, lang=b'nl'), b'twee miljoen')
        self.assertEqual(numinwords(4000000000, lang=b'nl'), b'vier miljard')

    def test_cardinal_for_decimal_number(self):
        self.assertEqual(numinwords(3.486, lang=b'nl'), b'drie komma vier acht zes')

    def test_ordinal_for_negative_numbers(self):
        self.assertRaises(TypeError, numinwords, -12, ordinal=True, lang=b'nl')

    def test_ordinal_for_floating_numbers(self):
        self.assertRaises(TypeError, numinwords, 2.453, ordinal=True, lang=b'nl')

    def test_to_currency_eur(self):
        self.assertEqual(numinwords(b'38.4', lang=b'nl', to=b'currency', separator=b' en', cents=False, currency=b'EUR'), b'achtendertig euro en 40 cent')
        self.assertEqual(numinwords(b'0', lang=b'nl', to=b'currency', separator=b' en', cents=False, currency=b'EUR'), b'nul euro en 00 cent')
        self.assertEqual(numinwords(b'1.01', lang=b'nl', to=b'currency', separator=b' en', cents=True, currency=b'EUR'), b'één euro en één cent')
        self.assertEqual(numinwords(b'4778.00', lang=b'nl', to=b'currency', separator=b' en', cents=True, currency=b'EUR'), b'vierduizendzevenhonderdachtenzeventig euro en nul cent')

    def test_to_currency_usd(self):
        self.assertEqual(numinwords(b'38.4', lang=b'nl', to=b'currency', separator=b' en', cents=False, currency=b'USD'), b'achtendertig dollar en 40 cent')
        self.assertEqual(numinwords(b'0', lang=b'nl', to=b'currency', separator=b' en', cents=False, currency=b'USD'), b'nul dollar en 00 cent')
        self.assertEqual(numinwords(b'1.01', lang=b'nl', to=b'currency', separator=b' en', cents=True, currency=b'USD'), b'één dollar en één cent')
        self.assertEqual(numinwords(b'4778.00', lang=b'nl', to=b'currency', separator=b' en', cents=True, currency=b'USD'), b'vierduizendzevenhonderdachtenzeventig dollar en nul cent')

    def test_pluralize(self):
        n = Num2Word_NL()
        cr1, cr2 = n.CURRENCY_FORMS[b'EUR']
        self.assertEqual(n.pluralize(1, cr1), b'euro')
        self.assertEqual(n.pluralize(2, cr1), b'euro')
        self.assertEqual(n.pluralize(1, cr2), b'cent')
        self.assertEqual(n.pluralize(2, cr2), b'cent')

    def test_to_year(self):
        self.assertEqual(numinwords(2018, lang=b'nl', to=b'year'), b'tweeduizendachttien')
        self.assertEqual(numinwords(2100, lang=b'nl', to=b'year'), b'eenentwintig honderd')