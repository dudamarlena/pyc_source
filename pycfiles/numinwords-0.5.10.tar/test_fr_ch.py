# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_fr_ch.py
# Compiled at: 2020-04-17 01:12:58
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords
TEST_CASES_CARDINAL = (
 (70, 'septante'),
 (79, 'septante-neuf'),
 (89, 'huitante-neuf'),
 (95, 'nonante-cinq'),
 (729, 'sept cents vingt-neuf'),
 (894, 'huit cents nonante-quatre'),
 (999, 'neuf cents nonante-neuf'),
 (7232, 'sept mille deux cents trente-deux'),
 (8569, 'huit mille cinq cents soixante-neuf'),
 (9539, 'neuf mille cinq cents trente-neuf'),
 (1000000, 'un millions'),
 (1000001, 'un millions un'),
 (4000000, 'quatre millions'),
 (10000000000000, 'dix billions'),
 (100000000000000, 'cent billions'),
 (1000000000000000000, 'un trillions'),
 (1000000000000000000000, 'un trilliards'),
 (10000000000000000000000000, 'dix quadrillions'))
TEST_CASES_ORDINAL = (
 (1, 'premier'),
 (8, 'huitième'),
 (12, 'douzième'),
 (14, 'quatorzième'),
 (28, 'vingt-huitième'),
 (100, 'centième'),
 (1000, 'millième'),
 (1000000, 'un millionsième'),
 (1000000000000000, 'un billiardsième'),
 (1000000000000000000, 'un trillionsième'))
TEST_CASES_TO_CURRENCY_EUR = (
 (1.0, 'un euro et zéro centimes'),
 (2.01, 'deux euros et un centime'),
 (8.1, 'huit euros et dix centimes'),
 (12.26, 'douze euros et vingt-six centimes'),
 (21.29, 'vingt et un euros et vingt-neuf centimes'),
 (81.25, 'huitante et un euros et vingt-cinq centimes'),
 (100.0, 'cent euros et zéro centimes'))
TEST_CASES_TO_CURRENCY_FRF = (
 (1.0, 'un franc et zéro centimes'),
 (2.01, 'deux francs et un centime'),
 (8.1, 'huit francs et dix centimes'),
 (12.27, 'douze francs et vingt-sept centimes'),
 (21.29, 'vingt et un francs et vingt-neuf centimes'),
 (81.25, 'huitante et un francs et vingt-cinq centimes'),
 (100.0, 'cent francs et zéro centimes'))

class numinwordsENTest(TestCase):

    def test_ordinal_special_joins(self):
        self.assertEqual(numinwords(5, ordinal=True, lang=b'fr_CH'), b'cinquième')
        self.assertEqual(numinwords(6, ordinal=True, lang=b'fr_CH'), b'sixième')
        self.assertEqual(numinwords(35, ordinal=True, lang=b'fr_CH'), b'trente-cinquième')
        self.assertEqual(numinwords(9, ordinal=True, lang=b'fr_CH'), b'neuvième')
        self.assertEqual(numinwords(49, ordinal=True, lang=b'fr_CH'), b'quarante-neuvième')
        self.assertEqual(numinwords(71, lang=b'fr_CH'), b'septante et un')
        self.assertEqual(numinwords(81, lang=b'fr_CH'), b'huitante et un')
        self.assertEqual(numinwords(80, lang=b'fr_CH'), b'huitante')
        self.assertEqual(numinwords(880, lang=b'fr_CH'), b'huit cents huitante')
        self.assertEqual(numinwords(91, ordinal=True, lang=b'fr_CH'), b'nonante et unième')
        self.assertEqual(numinwords(53, lang=b'fr_CH'), b'cinquante-trois')

    def test_number(self):
        for test in TEST_CASES_CARDINAL:
            self.assertEqual(numinwords(test[0], lang=b'fr_CH'), test[1])

    def test_ordinal(self):
        for test in TEST_CASES_ORDINAL:
            self.assertEqual(numinwords(test[0], lang=b'fr_CH', ordinal=True), test[1])

    def test_currency_eur(self):
        for test in TEST_CASES_TO_CURRENCY_EUR:
            self.assertEqual(numinwords(test[0], lang=b'fr_CH', to=b'currency'), test[1])

    def test_currency_frf(self):
        for test in TEST_CASES_TO_CURRENCY_FRF:
            self.assertEqual(numinwords(test[0], lang=b'fr_CH', to=b'currency', currency=b'FRF'), test[1])