# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_lt.py
# Compiled at: 2020-04-17 01:13:34
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsLTTest(TestCase):

    def test_to_cardinal(self):
        self.assertEqual(numinwords(100, lang=b'lt'), b'vienas šimtas')
        self.assertEqual(numinwords(101, lang=b'lt'), b'vienas šimtas vienas')
        self.assertEqual(numinwords(110, lang=b'lt'), b'vienas šimtas dešimt')
        self.assertEqual(numinwords(115, lang=b'lt'), b'vienas šimtas penkiolika')
        self.assertEqual(numinwords(123, lang=b'lt'), b'vienas šimtas dvidešimt trys')
        self.assertEqual(numinwords(1000, lang=b'lt'), b'vienas tūkstantis')
        self.assertEqual(numinwords(1001, lang=b'lt'), b'vienas tūkstantis vienas')
        self.assertEqual(numinwords(2012, lang=b'lt'), b'du tūkstančiai dvylika')
        self.assertEqual(numinwords(1234567890, lang=b'lt'), b'vienas milijardas du šimtai trisdešimt keturi milijonai penki šimtai šešiasdešimt septyni tūkstančiai aštuoni šimtai devyniasdešimt')
        self.assertEqual(numinwords(215461407892039002157189883901676, lang=b'lt'), b'du šimtai penkiolika naintilijonų keturi šimtai šešiasdešimt vienas oktilijonas keturi šimtai septyni septilijonai aštuoni šimtai devyniasdešimt du sikstilijonai trisdešimt devyni kvintilijonai du kvadrilijonai vienas šimtas penkiasdešimt septyni trilijonai vienas šimtas aštuoniasdešimt devyni milijardai aštuoni šimtai aštuoniasdešimt trys milijonai devyni šimtai vienas tūkstantis šeši šimtai septyniasdešimt šeši')
        self.assertEqual(numinwords(719094234693663034822824384220291, lang=b'lt'), b'septyni šimtai devyniolika naintilijonų devyniasdešimt keturi oktilijonai du šimtai trisdešimt keturi septilijonai šeši šimtai devyniasdešimt trys sikstilijonai šeši šimtai šešiasdešimt trys kvintilijonai trisdešimt keturi kvadrilijonai aštuoni šimtai dvidešimt du trilijonai aštuoni šimtai dvidešimt keturi milijardai trys šimtai aštuoniasdešimt keturi milijonai du šimtai dvidešimt tūkstančių du šimtai devyniasdešimt vienas')
        self.assertEqual(numinwords(-5000, lang=b'lt'), b'minus penki tūkstančiai')
        self.assertEqual(numinwords(-5000.22, lang=b'lt'), b'minus penki tūkstančiai kablelis dvidešimt du')

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'lt', to=b'ordinal')

    def test_to_currency(self):
        self.assertEqual(numinwords(1.0, lang=b'lt', to=b'currency', currency=b'LTL'), b'vienas litas, nulis centų')
        self.assertEqual(numinwords(10.01, lang=b'lt', to=b'currency', currency=b'LTL'), b'dešimt litų, vienas centas')
        self.assertEqual(numinwords(1234.56, lang=b'lt', to=b'currency', currency=b'LTL'), b'vienas tūkstantis du šimtai trisdešimt keturi litai, penkiasdešimt šeši centai')
        self.assertEqual(numinwords(-1251981, lang=b'lt', to=b'currency', currency=b'EUR', cents=False), b'minus dvylika tūkstančių penki šimtai devyniolika eurų, 81 centas')
        self.assertEqual(numinwords(1.0, lang=b'lt', to=b'currency', currency=b'EUR'), b'vienas euras, nulis centų')
        self.assertEqual(numinwords(1234.56, lang=b'lt', to=b'currency', currency=b'EUR'), b'vienas tūkstantis du šimtai trisdešimt keturi eurai, penkiasdešimt šeši centai')
        self.assertEqual(numinwords(1122.22, lang=b'lt', to=b'currency', currency=b'EUR'), b'vienas tūkstantis vienas šimtas dvidešimt du eurai, dvidešimt du centai')
        self.assertEqual(numinwords(-1281, lang=b'lt', to=b'currency', currency=b'USD', cents=False), b'minus dvylika dolerių, 81 centas')
        self.assertEqual(numinwords(1.0, lang=b'lt', to=b'currency', currency=b'USD'), b'vienas doleris, nulis centų')
        self.assertEqual(numinwords(5.06, lang=b'lt', to=b'currency', currency=b'USD'), b'penki doleriai, šeši centai')
        self.assertEqual(numinwords(-1281, lang=b'lt', to=b'currency', currency=b'GBP', cents=False), b'minus dvylika svarų sterlingų, 81 pensas')
        self.assertEqual(numinwords(1.0, lang=b'lt', to=b'currency', currency=b'GBP'), b'vienas svaras sterlingų, nulis pensų')
        self.assertEqual(numinwords(5.06, lang=b'lt', to=b'currency', currency=b'GBP'), b'penki svarai sterlingų, šeši pensai')
        self.assertEqual(numinwords(-1281, lang=b'lt', to=b'currency', currency=b'PLN', cents=False), b'minus dvylika zlotų, 81 grašis')
        self.assertEqual(numinwords(1.0, lang=b'lt', to=b'currency', currency=b'PLN'), b'vienas zlotas, nulis grašių')
        self.assertEqual(numinwords(5.06, lang=b'lt', to=b'currency', currency=b'PLN'), b'penki zlotai, šeši grašiai')
        self.assertEqual(numinwords(-1281, lang=b'lt', to=b'currency', currency=b'RUB', cents=False), b'minus dvylika rublių, 81 kapeika')
        self.assertEqual(numinwords(1.0, lang=b'lt', to=b'currency', currency=b'RUB'), b'vienas rublis, nulis kapeikų')
        self.assertEqual(numinwords(5.06, lang=b'lt', to=b'currency', currency=b'RUB'), b'penki rubliai, šešios kapeikos')
        self.assertEqual(numinwords(-12.01, lang=b'lt', to=b'currency', currency=b'RUB'), b'minus dvylika rublių, viena kapeika')
        self.assertEqual(numinwords(1122.22, lang=b'lt', to=b'currency', currency=b'RUB'), b'vienas tūkstantis vienas šimtas dvidešimt du rubliai, dvidešimt dvi kapeikos')