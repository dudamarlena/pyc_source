# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_fr_dz.py
# Compiled at: 2020-04-17 01:13:00
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords
from . import test_fr
TEST_CASES_TO_CURRENCY = (
 (1, 'un dinard'),
 (2, 'deux dinards'),
 (8, 'huit dinards'),
 (12, 'douze dinards'),
 (21, 'vingt et un dinards'),
 (81.25, 'quatre-vingt-un dinards et vingt-cinq centimes'),
 (100, 'cent dinards'))

class numinwordsPLTest(TestCase):

    def test_currency(self):
        self.assertEqual(numinwords(1234.12, lang=b'fr_DZ', to=b'currency'), b'mille deux cent trente-quatre dinards et douze centimes')
        self.assertEqual(numinwords(45689.89, lang=b'fr_DZ', to=b'currency'), b'quarante-cinq mille six cent quatre-vingt-neuf dinards et quatre-vingt-neuf centimes')

    def test_number(self):
        for test in test_fr.TEST_CASES_CARDINAL:
            self.assertEqual(numinwords(test[0], lang=b'fr_DZ'), test[1])

    def test_ordinal(self):
        for test in test_fr.TEST_CASES_ORDINAL:
            self.assertEqual(numinwords(test[0], lang=b'fr_DZ', ordinal=True), test[1])

    def test_ordinal_num(self):
        for test in test_fr.TEST_CASES_ORDINAL_NUM:
            self.assertEqual(numinwords(test[0], lang=b'fr_DZ', to=b'ordinal_num'), test[1])