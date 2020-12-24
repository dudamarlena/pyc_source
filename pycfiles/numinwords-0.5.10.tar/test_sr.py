# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_sr.py
# Compiled at: 2020-04-17 01:14:31
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsSRTest(TestCase):

    def test_cardinal(self):
        self.assertEqual(b'sto', numinwords(100, lang=b'sr'))
        self.assertEqual(b'sto jedan', numinwords(101, lang=b'sr'))
        self.assertEqual(b'sto deset', numinwords(110, lang=b'sr'))
        self.assertEqual(b'sto petnaest', numinwords(115, lang=b'sr'))
        self.assertEqual(b'sto dvadeset tri', numinwords(123, lang=b'sr'))
        self.assertEqual(b'jedna hiljada', numinwords(1000, lang=b'sr'))
        self.assertEqual(b'jedna hiljada jedan', numinwords(1001, lang=b'sr'))
        self.assertEqual(b'dve hiljade dvanaest', numinwords(2012, lang=b'sr'))
        self.assertEqual(b'dvanaest hiljada petsto devetnaest zapeta osamdeset pet', numinwords(12519.85, lang=b'sr'))
        self.assertEqual(b'jedan bilion dvesta trideset četiri miliona petsto šezdeset sedam hiljada osamsto devedeset', numinwords(1234567890, lang=b'sr'))
        self.assertEqual(b'dvesta petnaest noniliona četristo šezdeset jedan oktilion četristo sedam septiliona osamsto devedeset dva sekstiliona trideset devet kvintiliona dva kvadriliona sto pedeset sedam triliona sto osamdeset devet biliona osamsto osamdeset tri miliona devetsto jedna hiljada šesto sedamdeset šest', numinwords(215461407892039002157189883901676, lang=b'sr'))
        self.assertEqual(b'sedamsto devetnaest noniliona devedeset četiri oktiliona dvesta trideset četiri septiliona šesto devedeset tri sekstiliona šesto šezdeset tri kvintiliona trideset četiri kvadriliona osamsto dvadeset dva triliona osamsto dvadeset četiri biliona trista osamdeset četiri miliona dvesta dvadeset hiljada dvesta devedeset jedan', numinwords(719094234693663034822824384220291, lang=b'sr'))
        self.assertEqual(b'pet', numinwords(5, lang=b'sr'))
        self.assertEqual(b'petnaest', numinwords(15, lang=b'sr'))
        self.assertEqual(b'sto pedeset četiri', numinwords(154, lang=b'sr'))
        self.assertEqual(b'jedna hiljada sto trideset pet', numinwords(1135, lang=b'sr'))
        self.assertEqual(b'četristo osamnaest hiljada petsto trideset jedan', numinwords(418531, lang=b'sr'))
        self.assertEqual(b'jedan milion sto trideset devet', numinwords(1000139, lang=b'sr'))

    def test_floating_point(self):
        self.assertEqual(b'pet zapeta dva', numinwords(5.2, lang=b'sr'))
        self.assertEqual(b'petsto šezdeset jedan zapeta četrdeset dva', numinwords(561.42, lang=b'sr'))

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'sr', to=b'ordinal')

    def test_to_currency(self):
        self.assertEqual(b'jedan evro, nula centi', numinwords(1.0, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'dva evra, nula centi', numinwords(2.0, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'pet evra, nula centi', numinwords(5.0, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'dva evra, jedan cent', numinwords(2.01, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'dva evra, dva centa', numinwords(2.02, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'dva evra, pet centi', numinwords(2.05, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'dve rublje, nula kopejki', numinwords(2.0, lang=b'sr', to=b'currency', currency=b'RUB'))
        self.assertEqual(b'dve rublje, jedna kopejka', numinwords(2.01, lang=b'sr', to=b'currency', currency=b'RUB'))
        self.assertEqual(b'dve rublje, dve kopejke', numinwords(2.02, lang=b'sr', to=b'currency', currency=b'RUB'))
        self.assertEqual(b'dve rublje, pet kopejki', numinwords(2.05, lang=b'sr', to=b'currency', currency=b'RUB'))
        self.assertEqual(b'jedan dinar, nula para', numinwords(1.0, lang=b'sr', to=b'currency', currency=b'RSD'))
        self.assertEqual(b'dva dinara, dve pare', numinwords(2.02, lang=b'sr', to=b'currency', currency=b'RSD'))
        self.assertEqual(b'pet dinara, pet para', numinwords(5.05, lang=b'sr', to=b'currency', currency=b'RSD'))
        self.assertEqual(b'jedanaest dinara, jedanaest para', numinwords(11.11, lang=b'sr', to=b'currency', currency=b'RSD'))
        self.assertEqual(b'dvadeset jedan dinar, dvadeset jedna para', numinwords(21.21, lang=b'sr', to=b'currency', currency=b'RSD'))
        self.assertEqual(b'dvadeset jedan evro, dvadeset jedan cent', numinwords(21.21, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'dvadeset jedna rublja, dvadeset jedna kopejka', numinwords(21.21, lang=b'sr', to=b'currency', currency=b'RUB'))
        self.assertEqual(b'jedna hiljada dvesta trideset četiri evra, pedeset šest centi', numinwords(1234.56, lang=b'sr', to=b'currency', currency=b'EUR'))
        self.assertEqual(b'jedna hiljada dvesta trideset četiri rublje, pedeset šest kopejki', numinwords(1234.56, lang=b'sr', to=b'currency', currency=b'RUB'))
        self.assertEqual(b'sto jedan evro i jedanaest centi', numinwords(10111, lang=b'sr', to=b'currency', currency=b'EUR', separator=b' i'))
        self.assertEqual(b'sto jedna rublja i dvadeset jedna kopejka', numinwords(10121, lang=b'sr', to=b'currency', currency=b'RUB', separator=b' i'))
        self.assertEqual(b'sto jedna rublja i dvadeset dve kopejke', numinwords(10122, lang=b'sr', to=b'currency', currency=b'RUB', separator=b' i'))
        self.assertEqual(b'sto jedan evro i dvadeset jedan cent', numinwords(10121, lang=b'sr', to=b'currency', currency=b'EUR', separator=b' i'))
        self.assertEqual(b'minus dvanaest hiljada petsto devetnaest evra, 85 centi', numinwords(-1251985, lang=b'sr', to=b'currency', currency=b'EUR', cents=False))
        self.assertEqual(b'trideset osam evra i 40 centi', numinwords(b'38.4', lang=b'sr', to=b'currency', separator=b' i', cents=False, currency=b'EUR'))