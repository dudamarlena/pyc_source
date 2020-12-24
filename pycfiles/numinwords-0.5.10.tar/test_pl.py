# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_pl.py
# Compiled at: 2020-04-17 01:13:47
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsPLTest(TestCase):

    def test_cardinal(self):
        self.assertEqual(numinwords(100, lang=b'pl'), b'sto')
        self.assertEqual(numinwords(101, lang=b'pl'), b'sto jeden')
        self.assertEqual(numinwords(110, lang=b'pl'), b'sto dziesięć')
        self.assertEqual(numinwords(115, lang=b'pl'), b'sto piętnaście')
        self.assertEqual(numinwords(123, lang=b'pl'), b'sto dwadzieścia trzy')
        self.assertEqual(numinwords(1000, lang=b'pl'), b'tysiąc')
        self.assertEqual(numinwords(1001, lang=b'pl'), b'tysiąc jeden')
        self.assertEqual(numinwords(2012, lang=b'pl'), b'dwa tysiące dwanaście')
        self.assertEqual(numinwords(12519.85, lang=b'pl'), b'dwanaście tysięcy pięćset dziewiętnaście przecinek osiemdziesiąt pięć')
        self.assertEqual(numinwords(123.5, lang=b'pl'), b'sto dwadzieścia trzy przecinek pięć')
        self.assertEqual(numinwords(1234567890, lang=b'pl'), b'miliard dwieście trzydzieści cztery miliony pięćset sześćdziesiąt siedem tysięcy osiemset dziewięćdzisiąt')
        self.assertEqual(numinwords(10000000001000000100000, lang=b'pl'), b'dziesięć tryliardów bilion sto tysięcy')
        self.assertEqual(numinwords(215461407892039002157189883901676, lang=b'pl'), b'dwieście piętnaście kwintylionów czterysta sześćdziesiąt jeden kwadryliardów czterysta siedem kwadrylionów osiemset dziewięćdzisiąt dwa tryliardy trzydzieści dziewięć trylionów dwa biliardy sto pięćdziesiąt siedem bilionów sto osiemdziesiąt dziewięć miliardów osiemset osiemdziesiąt trzy miliony dziewięćset jeden tysięcy sześćset siedemdziesiąt sześć')
        self.assertEqual(numinwords(719094234693663034822824384220291, lang=b'pl'), b'siedemset dziewiętnaście kwintylionów dziewięćdzisiąt cztery kwadryliardy dwieście trzydzieści cztery kwadryliony sześćset dziewięćdzisiąt trzy tryliardy sześćset sześćdziesiąt trzy tryliony trzydzieści cztery biliardy osiemset dwadzieścia dwa biliony osiemset dwadzieścia cztery miliardy trzysta osiemdziesiąt cztery miliony dwieście dwadzieścia tysięcy dwieście dziewięćdzisiąt jeden')
        self.assertEqual(numinwords(963301000001918264129471001047146102 * 1000000000000000000000000000000 + 1007, lang=b'pl'), b'dziewięćset sześćdziesiąt trzy decyliardy trzysta jeden decylionów nonylion dziewięćset osiemnaście oktyliardów dwieście sześćdziesiąt cztery oktyliony sto dwadzieścia dziewięć septyliardów czterysta siedemdziesiąt jeden septylionów sekstyliard czterdzieści siedem sekstylionów sto czterdzieści sześć kwintyliardów sto dwa kwintyliony tysiąc siedem')

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'pl', to=b'ordinal')

    def test_currency(self):
        self.assertEqual(numinwords(1.0, lang=b'pl', to=b'currency', currency=b'EUR'), b'jeden euro, zero centów')
        self.assertEqual(numinwords(1.0, lang=b'pl', to=b'currency', currency=b'PLN'), b'jeden złoty, zero groszy')
        self.assertEqual(numinwords(1234.56, lang=b'pl', to=b'currency', currency=b'EUR'), b'tysiąc dwieście trzydzieści cztery euro, pięćdziesiąt sześć centów')
        self.assertEqual(numinwords(1234.56, lang=b'pl', to=b'currency', currency=b'PLN'), b'tysiąc dwieście trzydzieści cztery złote, pięćdziesiąt sześć groszy')
        self.assertEqual(numinwords(10111, lang=b'pl', to=b'currency', currency=b'EUR', separator=b' i'), b'sto jeden euro i jedenaście centów')
        self.assertEqual(numinwords(10121, lang=b'pl', to=b'currency', currency=b'PLN', separator=b' i'), b'sto jeden złotych i dwadzieścia jeden groszy')
        self.assertEqual(numinwords(-1251985, lang=b'pl', to=b'currency', cents=False), b'minus dwanaście tysięcy pięćset dziewiętnaście euro, 85 centów')
        self.assertEqual(numinwords(123.5, lang=b'pl', to=b'currency', currency=b'PLN', separator=b' i'), b'sto dwadzieścia trzy złote i pięćdziesiąt groszy')
        self.assertEqual(numinwords(1950, lang=b'pl', to=b'currency', cents=False), b'dziewiętnaście euro, 50 centów')