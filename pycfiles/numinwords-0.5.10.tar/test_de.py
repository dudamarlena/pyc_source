# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_de.py
# Compiled at: 2020-04-17 01:12:24
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords
TEST_CASES_TO_CURRENCY_EUR = (
 (1.0, 'ein Euro und null Cent'),
 (2.01, 'zwei Euro und ein Cent'),
 (8.1, 'acht Euro und zehn Cent'),
 (12.26, 'zwölf Euro und sechsundzwanzig Cent'),
 (21.29, 'einundzwanzig Euro und neunundzwanzig Cent'),
 (81.25, 'einundachtzig Euro und fünfundzwanzig Cent'),
 (100.0, 'einhundert Euro und null Cent'))
TEST_CASES_TO_CURRENCY_USD = (
 (1.0, 'ein Dollar und null Cent'),
 (2.01, 'zwei Dollar und ein Cent'),
 (8.1, 'acht Dollar und zehn Cent'),
 (12.26, 'zwölf Dollar und sechsundzwanzig Cent'),
 (21.29, 'einundzwanzig Dollar und neunundzwanzig Cent'),
 (81.25, 'einundachtzig Dollar und fünfundzwanzig Cent'),
 (100.0, 'einhundert Dollar und null Cent'))
TEST_CASES_TO_CURRENCY_GBP = (
 (1.0, 'ein Pfund und null Pence'),
 (2.01, 'zwei Pfund und ein Penny'),
 (8.1, 'acht Pfund und zehn Pence'),
 (12.26, 'zwölf Pfund und sechsundzwanzig Pence'),
 (21.29, 'einundzwanzig Pfund und neunundzwanzig Pence'),
 (81.25, 'einundachtzig Pfund und fünfundzwanzig Pence'),
 (100.0, 'einhundert Pfund und null Pence'))
TEST_CASES_TO_CURRENCY_DEM = (
 (1.0, 'ein Mark und null Pfennig'),
 (2.01, 'zwei Mark und ein Pfennig'),
 (8.1, 'acht Mark und zehn Pfennig'),
 (12.26, 'zwölf Mark und sechsundzwanzig Pfennig'),
 (21.29, 'einundzwanzig Mark und neunundzwanzig Pfennig'),
 (81.25, 'einundachtzig Mark und fünfundzwanzig Pfennig'),
 (100.0, 'einhundert Mark und null Pfennig'))

class numinwordsDETest(TestCase):

    def test_ordinal_less_than_twenty(self):
        self.assertEqual(numinwords(0, ordinal=True, lang=b'de'), b'nullte')
        self.assertEqual(numinwords(1, ordinal=True, lang=b'de'), b'erste')
        self.assertEqual(numinwords(7, ordinal=True, lang=b'de'), b'siebte')
        self.assertEqual(numinwords(8, ordinal=True, lang=b'de'), b'achte')
        self.assertEqual(numinwords(12, ordinal=True, lang=b'de'), b'zwölfte')
        self.assertEqual(numinwords(17, ordinal=True, lang=b'de'), b'siebzehnte')

    def test_ordinal_more_than_twenty(self):
        self.assertEqual(numinwords(81, ordinal=True, lang=b'de'), b'einundachtzigste')

    def test_ordinal_at_crucial_number(self):
        self.assertEqual(numinwords(100, ordinal=True, lang=b'de'), b'hundertste')
        self.assertEqual(numinwords(1000, ordinal=True, lang=b'de'), b'tausendste')
        self.assertEqual(numinwords(4000, ordinal=True, lang=b'de'), b'viertausendste')
        self.assertEqual(numinwords(1000000, ordinal=True, lang=b'de'), b'millionste')
        self.assertEqual(numinwords(2000000, ordinal=True, lang=b'de'), b'zweimillionste')
        self.assertEqual(numinwords(1000000000, ordinal=True, lang=b'de'), b'milliardste')
        self.assertEqual(numinwords(5000000000, ordinal=True, lang=b'de'), b'fünfmilliardste')

    def test_cardinal_at_some_numbers(self):
        self.assertEqual(numinwords(100, lang=b'de'), b'einhundert')
        self.assertEqual(numinwords(1000, lang=b'de'), b'eintausend')
        self.assertEqual(numinwords(5000, lang=b'de'), b'fünftausend')
        self.assertEqual(numinwords(10000, lang=b'de'), b'zehntausend')
        self.assertEqual(numinwords(1000000, lang=b'de'), b'eine Million')
        self.assertEqual(numinwords(2000000, lang=b'de'), b'zwei Millionen')
        self.assertEqual(numinwords(4000000000, lang=b'de'), b'vier Milliarden')
        self.assertEqual(numinwords(1000000000, lang=b'de'), b'eine Milliarde')

    def test_cardinal_for_decimal_number(self):
        self.assertEqual(numinwords(3.486, lang=b'de'), b'drei Komma vier acht sechs')

    def test_giant_cardinal_for_merge(self):
        self.assertEqual(numinwords(4500072900000111, lang=b'de'), b'vier Billiarden fünfhundert Billionen ' + b'zweiundsiebzig Milliarden neunhundert Millionen einhundertelf')

    def test_ordinal_num(self):
        self.assertEqual(numinwords(7, to=b'ordinal_num', lang=b'de'), b'7.')
        self.assertEqual(numinwords(81, to=b'ordinal_num', lang=b'de'), b'81.')

    def test_ordinal_for_negative_numbers(self):
        self.assertRaises(TypeError, numinwords, -12, ordinal=True, lang=b'de')

    def test_ordinal_for_floating_numbers(self):
        self.assertRaises(TypeError, numinwords, 2.453, ordinal=True, lang=b'de')

    def test_currency_eur(self):
        for test in TEST_CASES_TO_CURRENCY_EUR:
            self.assertEqual(numinwords(test[0], lang=b'de', to=b'currency', currency=b'EUR'), test[1])

    def test_currency_usd(self):
        for test in TEST_CASES_TO_CURRENCY_USD:
            self.assertEqual(numinwords(test[0], lang=b'de', to=b'currency', currency=b'USD'), test[1])

    def test_currency_dem(self):
        for test in TEST_CASES_TO_CURRENCY_DEM:
            self.assertEqual(numinwords(test[0], lang=b'de', to=b'currency', currency=b'DEM'), test[1])

    def test_currency_gbp(self):
        for test in TEST_CASES_TO_CURRENCY_GBP:
            self.assertEqual(numinwords(test[0], lang=b'de', to=b'currency', currency=b'GBP'), test[1])

    def test_year(self):
        self.assertEqual(numinwords(2002, to=b'year', lang=b'de'), b'zweitausendzwei')

    def test_year_before_2000(self):
        self.assertEqual(numinwords(1780, to=b'year', lang=b'de'), b'siebzehnhundertachtzig')