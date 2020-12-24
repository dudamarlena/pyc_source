# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_lv.py
# Compiled at: 2020-04-17 01:13:38
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsLVTest(TestCase):

    def test_to_cardinal(self):
        self.assertEqual(numinwords(100, lang=b'lv'), b'simts')
        self.assertEqual(numinwords(101, lang=b'lv'), b'simtu viens')
        self.assertEqual(numinwords(110, lang=b'lv'), b'simts desmit')
        self.assertEqual(numinwords(115, lang=b'lv'), b'simts piecpadsmit')
        self.assertEqual(numinwords(123, lang=b'lv'), b'simts divdesmit trīs')
        self.assertEqual(numinwords(1000, lang=b'lv'), b'tūkstotis')
        self.assertEqual(numinwords(1001, lang=b'lv'), b'tūkstotis viens')
        self.assertEqual(numinwords(2012, lang=b'lv'), b'divi tūkstoši divpadsmit')
        self.assertEqual(numinwords(1234567890, lang=b'lv'), b'miljards divi simti trīsdesmit četri miljoni pieci simti sešdesmit septiņi tūkstoši astoņi simti deviņdesmit')
        self.assertEqual(numinwords(215461407892039002157189883901676, lang=b'lv'), b'divi simti piecpadsmit nontiljoni četri simti sešdesmit viens oktiljons četri simti septiņi septiljoni astoņi simti deviņdesmit divi sikstiljoni trīsdesmit deviņi kvintiljoni divi kvadriljoni simts piecdesmit septiņi triljoni simts astoņdesmit deviņi miljardi astoņi simti astoņdesmit trīs miljoni deviņi simti viens tūkstotis seši simti septiņdesmit seši')
        self.assertEqual(numinwords(719094234693663034822824384220291, lang=b'lv'), b'septiņi simti deviņpadsmit nontiljoni deviņdesmit četri oktiljoni divi simti trīsdesmit četri septiljoni seši simti deviņdesmit trīs sikstiljoni seši simti sešdesmit trīs kvintiljoni trīsdesmit četri kvadriljoni astoņi simti divdesmit divi triljoni astoņi simti divdesmit četri miljardi trīs simti astoņdesmit četri miljoni divi simti divdesmit tūkstoši divi simti deviņdesmit viens')
        self.assertEqual(numinwords(-5000, lang=b'lv'), b'mīnus pieci tūkstoši')
        self.assertEqual(numinwords(-5000.22, lang=b'lv'), b'mīnus pieci tūkstoši komats divdesmit divi')
        self.assertEqual(numinwords(0, lang=b'lv'), b'nulle')
        self.assertEqual(numinwords(5, lang=b'lv'), b'pieci')
        self.assertEqual(numinwords(15, lang=b'lv'), b'piecpadsmit')
        self.assertEqual(numinwords(154, lang=b'lv'), b'simts piecdesmit četri')
        self.assertEqual(numinwords(101, lang=b'lv'), b'simtu viens')
        self.assertEqual(numinwords(1135, lang=b'lv'), b'tūkstotis simts trīsdesmit pieci')
        self.assertEqual(numinwords(418531, lang=b'lv'), b'četri simti astoņpadsmit tūkstoši pieci simti trīsdesmit viens')
        self.assertEqual(numinwords(1000139, lang=b'lv'), b'miljons simts trīsdesmit deviņi')

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'lv', to=b'ordinal')

    def test_to_currency(self):
        self.assertEqual(numinwords(1.0, lang=b'lv', to=b'currency', currency=b'EUR'), b'viens eiro, nulle centu')
        self.assertEqual(numinwords(1.0, lang=b'lv', to=b'currency', currency=b'LVL'), b'viens lats, nulle santīmu')
        self.assertEqual(numinwords(1234.56, lang=b'lv', to=b'currency', currency=b'EUR'), b'tūkstotis divi simti trīsdesmit četri eiro, piecdesmit seši centi')
        self.assertEqual(numinwords(1234.56, lang=b'lv', to=b'currency', currency=b'LVL'), b'tūkstotis divi simti trīsdesmit četri lati, piecdesmit seši santīmi')
        self.assertEqual(numinwords(10111, lang=b'lv', to=b'currency', separator=b' un', currency=b'EUR'), b'simtu viens eiro un vienpadsmit centi')
        self.assertEqual(numinwords(10121, lang=b'lv', to=b'currency', separator=b' un', currency=b'LVL'), b'simtu viens lats un divdesmit viens santīms')
        self.assertEqual(numinwords(-1251985, lang=b'lv', to=b'currency', cents=False, currency=b'EUR'), b'mīnus divpadsmit tūkstoši pieci simti deviņpadsmit eiro, 85 centi')
        self.assertEqual(numinwords(b'38.4', lang=b'lv', to=b'currency', separator=b' un', cents=False, currency=b'EUR'), b'trīsdesmit astoņi eiro un 40 centi')
        self.assertEqual(numinwords(b'38.4', lang=b'lv', to=b'currency', separator=b' un', cents=False, currency=b'EUR_LEGAL'), b'trīsdesmit astoņi euro un 40 centi')
        self.assertEqual(numinwords(b'38.4', lang=b'lv', to=b'currency', separator=b' un', cents=False, currency=b'USD', adjective=False), b'trīsdesmit astoņi dolāri un 40 centi')
        self.assertEqual(numinwords(b'38.4', lang=b'lv', to=b'currency', separator=b' un', cents=False, currency=b'USD', adjective=True), b'trīsdesmit astoņi ASV dolāri un 40 centi')

    def test_fractions(self):
        self.assertEqual(numinwords(5.2, lang=b'lv'), b'pieci komats divi')
        self.assertEqual(numinwords(561.42, lang=b'lv'), b'pieci simti sešdesmit viens komats četrdesmit divi')