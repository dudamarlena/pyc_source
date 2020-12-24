# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_it.py
# Compiled at: 2020-04-17 01:13:14
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsITTest(TestCase):
    maxDiff = None

    def test_negative(self):
        number = 648972145
        pos_crd = numinwords(+number, lang=b'it')
        neg_crd = numinwords(-number, lang=b'it')
        pos_ord = numinwords(+number, lang=b'it', ordinal=True)
        neg_ord = numinwords(-number, lang=b'it', ordinal=True)
        self.assertEqual(b'meno ' + pos_crd, neg_crd)
        self.assertEqual(b'meno ' + pos_ord, neg_ord)

    def test_float_to_cardinal(self):
        self.assertEqual(numinwords(3.1415, lang=b'it'), b'tre virgola uno quattro uno cinque')
        self.assertEqual(numinwords(-5.15, lang=b'it'), b'meno cinque virgola uno cinque')
        self.assertEqual(numinwords(-0.15, lang=b'it'), b'meno zero virgola uno cinque')

    def test_float_to_ordinal(self):
        self.assertEqual(numinwords(3.1415, lang=b'it', ordinal=True), b'terzo virgola uno quattro uno cinque')
        self.assertEqual(numinwords(-5.15, lang=b'it', ordinal=True), b'meno quinto virgola uno cinque')
        self.assertEqual(numinwords(-0.15, lang=b'it', ordinal=True), b'meno zero virgola uno cinque')

    def test_0(self):
        self.assertEqual(numinwords(0, lang=b'it'), b'zero')
        self.assertEqual(numinwords(0, lang=b'it', ordinal=True), b'zero')

    def test_1_to_10(self):
        self.assertEqual(numinwords(1, lang=b'it'), b'uno')
        self.assertEqual(numinwords(2, lang=b'it'), b'due')
        self.assertEqual(numinwords(7, lang=b'it'), b'sette')
        self.assertEqual(numinwords(10, lang=b'it'), b'dieci')

    def test_11_to_19(self):
        self.assertEqual(numinwords(11, lang=b'it'), b'undici')
        self.assertEqual(numinwords(13, lang=b'it'), b'tredici')
        self.assertEqual(numinwords(15, lang=b'it'), b'quindici')
        self.assertEqual(numinwords(16, lang=b'it'), b'sedici')
        self.assertEqual(numinwords(19, lang=b'it'), b'diciannove')

    def test_20_to_99(self):
        self.assertEqual(numinwords(20, lang=b'it'), b'venti')
        self.assertEqual(numinwords(21, lang=b'it'), b'ventuno')
        self.assertEqual(numinwords(23, lang=b'it'), b'ventitré')
        self.assertEqual(numinwords(28, lang=b'it'), b'ventotto')
        self.assertEqual(numinwords(31, lang=b'it'), b'trentuno')
        self.assertEqual(numinwords(40, lang=b'it'), b'quaranta')
        self.assertEqual(numinwords(66, lang=b'it'), b'sessantasei')
        self.assertEqual(numinwords(92, lang=b'it'), b'novantadue')

    def test_100_to_999(self):
        self.assertEqual(numinwords(100, lang=b'it'), b'cento')
        self.assertEqual(numinwords(111, lang=b'it'), b'centoundici')
        self.assertEqual(numinwords(150, lang=b'it'), b'centocinquanta')
        self.assertEqual(numinwords(196, lang=b'it'), b'centonovantasei')
        self.assertEqual(numinwords(200, lang=b'it'), b'duecento')
        self.assertEqual(numinwords(210, lang=b'it'), b'duecentodieci')
        self.assertEqual(numinwords(701, lang=b'it'), b'settecentouno')

    def test_1000_to_9999(self):
        self.assertEqual(numinwords(1000, lang=b'it'), b'mille')
        self.assertEqual(numinwords(1001, lang=b'it'), b'milleuno')
        self.assertEqual(numinwords(1500, lang=b'it'), b'millecinquecento')
        self.assertEqual(numinwords(7378, lang=b'it'), b'settemilatrecentosettantotto')
        self.assertEqual(numinwords(2000, lang=b'it'), b'duemila')
        self.assertEqual(numinwords(2100, lang=b'it'), b'duemilacento')
        self.assertEqual(numinwords(6870, lang=b'it'), b'seimilaottocentosettanta')
        self.assertEqual(numinwords(10000, lang=b'it'), b'diecimila')
        self.assertEqual(numinwords(98765, lang=b'it'), b'novantottomilasettecentosessantacinque')
        self.assertEqual(numinwords(100000, lang=b'it'), b'centomila')
        self.assertEqual(numinwords(523456, lang=b'it'), b'cinquecentoventitremilaquattrocentocinquantasei')

    def test_big(self):
        self.assertEqual(numinwords(1000000, lang=b'it'), b'un milione')
        self.assertEqual(numinwords(1000007, lang=b'it'), b'un milione e sette')
        self.assertEqual(numinwords(1200000, lang=b'it'), b'un milione e duecentomila')
        self.assertEqual(numinwords(3000000, lang=b'it'), b'tre milioni')
        self.assertEqual(numinwords(3000005, lang=b'it'), b'tre milioni e cinque')
        self.assertEqual(numinwords(3800000, lang=b'it'), b'tre milioni e ottocentomila')
        self.assertEqual(numinwords(1000000000, lang=b'it'), b'un miliardo')
        self.assertEqual(numinwords(1000000017, lang=b'it'), b'un miliardo e diciassette')
        self.assertEqual(numinwords(2000000000, lang=b'it'), b'due miliardi')
        self.assertEqual(numinwords(2000001000, lang=b'it'), b'due miliardi e mille')
        self.assertEqual(numinwords(1234567890, lang=b'it'), b'un miliardo, duecentotrentaquattro milioni e cinquecentosessantasettemilaottocentonovanta')
        self.assertEqual(numinwords(1000000000000, lang=b'it'), b'un bilione')
        self.assertEqual(numinwords(123456789012345678901234567890, lang=b'it'), b'centoventitré quadriliardi, quattrocentocinquantasei quadrilioni, settecentottantanove triliardi, dodici trilioni, trecentoquarantacinque biliardi, seicentosettantotto bilioni, novecentouno miliardi, duecentotrentaquattro milioni e cinquecentosessantasettemilaottocentonovanta')

    def test_nth_1_to_99(self):
        self.assertEqual(numinwords(1, lang=b'it', ordinal=True), b'primo')
        self.assertEqual(numinwords(8, lang=b'it', ordinal=True), b'ottavo')
        self.assertEqual(numinwords(21, lang=b'it', ordinal=True), b'ventunesimo')
        self.assertEqual(numinwords(23, lang=b'it', ordinal=True), b'ventitreesimo')
        self.assertEqual(numinwords(47, lang=b'it', ordinal=True), b'quarantasettesimo')
        self.assertEqual(numinwords(99, lang=b'it', ordinal=True), b'novantanovesimo')

    def test_nth_100_to_999(self):
        self.assertEqual(numinwords(100, lang=b'it', ordinal=True), b'centesimo')
        self.assertEqual(numinwords(112, lang=b'it', ordinal=True), b'centododicesimo')
        self.assertEqual(numinwords(120, lang=b'it', ordinal=True), b'centoventesimo')
        self.assertEqual(numinwords(121, lang=b'it', ordinal=True), b'centoventunesimo')
        self.assertEqual(numinwords(316, lang=b'it', ordinal=True), b'trecentosedicesimo')
        self.assertEqual(numinwords(700, lang=b'it', ordinal=True), b'settecentesimo')
        self.assertEqual(numinwords(803, lang=b'it', ordinal=True), b'ottocentotreesimo')
        self.assertEqual(numinwords(923, lang=b'it', ordinal=True), b'novecentoventitreesimo')

    def test_nth_1000_to_999999(self):
        self.assertEqual(numinwords(1000, lang=b'it', ordinal=True), b'millesimo')
        self.assertEqual(numinwords(1001, lang=b'it', ordinal=True), b'milleunesimo')
        self.assertEqual(numinwords(1003, lang=b'it', ordinal=True), b'milletreesimo')
        self.assertEqual(numinwords(1200, lang=b'it', ordinal=True), b'milleduecentesimo')
        self.assertEqual(numinwords(8640, lang=b'it', ordinal=True), b'ottomilaseicentoquarantesimo')
        self.assertEqual(numinwords(14000, lang=b'it', ordinal=True), b'quattordicimillesimo')
        self.assertEqual(numinwords(123456, lang=b'it', ordinal=True), b'centoventitremilaquattrocentocinquantaseiesimo')
        self.assertEqual(numinwords(987654, lang=b'it', ordinal=True), b'novecentottantasettemilaseicentocinquantaquattresimo')

    def test_nth_big(self):
        self.assertEqual(numinwords(1000000001, lang=b'it', ordinal=True), b'un miliardo e unesimo')
        self.assertEqual(numinwords(123456789012345678901234567890, lang=b'it', ordinal=True), b'centoventitré quadriliardi, quattrocentocinquantasei quadrilioni, settecentottantanove triliardi, dodici trilioni, trecentoquarantacinque biliardi, seicentosettantotto bilioni, novecentouno miliardi, duecentotrentaquattro milioni e cinquecentosessantasettemilaottocentonovantesimo')

    def test_with_decimals(self):
        self.assertAlmostEqual(numinwords(1.0, lang=b'it'), b'uno virgola zero')
        self.assertAlmostEqual(numinwords(1.1, lang=b'it'), b'uno virgola uno')