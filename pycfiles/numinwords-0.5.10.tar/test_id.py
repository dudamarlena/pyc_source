# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_id.py
# Compiled at: 2020-04-17 01:13:11
from unittest import TestCase
from numinwords import numinwords

class numinwordsIDTest(TestCase):

    def test_cardinal_for_natural_number(self):
        self.assertEqual(numinwords(10, lang='id'), 'sepuluh')
        self.assertEqual(numinwords(11, lang='id'), 'sebelas')
        self.assertEqual(numinwords(108, lang='id'), 'seratus delapan')
        self.assertEqual(numinwords(1075, lang='id'), 'seribu tujuh puluh lima')
        self.assertEqual(numinwords(1087231, lang='id'), 'satu juta delapan puluh tujuh ribu dua ratus tiga puluh satu')
        self.assertEqual(numinwords(1000000408, lang='id'), 'satu miliar empat ratus delapan')

    def test_cardinal_for_decimal_number(self):
        self.assertEqual(numinwords(12.234, lang='id'), 'dua belas koma dua tiga empat')
        self.assertEqual(numinwords(9.076, lang='id'), 'sembilan koma nol tujuh enam')

    def test_cardinal_for_negative_number(self):
        self.assertEqual(numinwords(-923, lang='id'), 'min sembilan ratus dua puluh tiga')
        self.assertEqual(numinwords(-0.234, lang='id'), 'min nol koma dua tiga empat')

    def test_ordinal_for_natural_number(self):
        self.assertEqual(numinwords(1, ordinal=True, lang='id'), 'pertama')
        self.assertEqual(numinwords(10, ordinal=True, lang='id'), 'kesepuluh')

    def test_ordinal_for_negative_number(self):
        self.assertRaises(TypeError, numinwords, -12, ordinal=True, lang='id')

    def test_ordinal_for_floating_number(self):
        self.assertRaises(TypeError, numinwords, 3.243, ordinal=True, lang='id')