# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_fr_be.py
# Compiled at: 2020-04-17 01:12:55
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords
TEST_CASES_CARDINAL = (
 (70, 'septante'),
 (79, 'septante-neuf'),
 (89, 'quatre-vingt-neuf'),
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
 (81.25, 'quatre-vingt et un euros et vingt-cinq centimes'),
 (100.0, 'cent euros et zéro centimes'))
TEST_CASES_TO_CURRENCY_FRF = (
 (1.0, 'un franc et zéro centimes'),
 (2.01, 'deux francs et un centime'),
 (8.1, 'huit francs et dix centimes'),
 (12.27, 'douze francs et vingt-sept centimes'),
 (21.29, 'vingt et un francs et vingt-neuf centimes'),
 (81.25, 'quatre-vingt et un francs et vingt-cinq centimes'),
 (100.0, 'cent francs et zéro centimes'))
LANG = b'fr_BE'

class numinwordsENTest(TestCase):

    def test_ordinal_special_joins(self):
        self.assertEqual(numinwords(5, ordinal=True, lang=LANG), b'cinquième')
        self.assertEqual(numinwords(6, ordinal=True, lang=LANG), b'sixième')
        self.assertEqual(numinwords(35, ordinal=True, lang=LANG), b'trente-cinquième')
        self.assertEqual(numinwords(9, ordinal=True, lang=LANG), b'neuvième')
        self.assertEqual(numinwords(49, ordinal=True, lang=LANG), b'quarante-neuvième')
        self.assertEqual(numinwords(71, lang=LANG), b'septante et un')
        self.assertEqual(numinwords(81, lang=LANG), b'quatre-vingt et un')
        self.assertEqual(numinwords(80, lang=LANG), b'quatre-vingt')
        self.assertEqual(numinwords(880, lang=LANG), b'huit cents quatre-vingt')
        self.assertEqual(numinwords(91, ordinal=True, lang=LANG), b'nonante et unième')
        self.assertEqual(numinwords(53, lang=LANG), b'cinquante-trois')

    def test_number(self):
        for test in TEST_CASES_CARDINAL:
            self.assertEqual(numinwords(test[0], lang=LANG), test[1])

    def test_ordinal(self):
        for test in TEST_CASES_ORDINAL:
            self.assertEqual(numinwords(test[0], lang=LANG, ordinal=True), test[1])

    def test_currency_eur(self):
        for test in TEST_CASES_TO_CURRENCY_EUR:
            self.assertEqual(numinwords(test[0], lang=LANG, to=b'currency'), test[1])

    def test_currency_frf(self):
        for test in TEST_CASES_TO_CURRENCY_FRF:
            self.assertEqual(numinwords(test[0], lang=LANG, to=b'currency', currency=b'FRF'), test[1])