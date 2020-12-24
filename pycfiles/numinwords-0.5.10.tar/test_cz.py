# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_cz.py
# Compiled at: 2020-04-17 01:12:20
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsCZTest(TestCase):

    def test_cardinal(self):
        self.assertEqual(numinwords(100, lang=b'cz'), b'sto')
        self.assertEqual(numinwords(101, lang=b'cz'), b'sto jedna')
        self.assertEqual(numinwords(110, lang=b'cz'), b'sto deset')
        self.assertEqual(numinwords(115, lang=b'cz'), b'sto patnáct')
        self.assertEqual(numinwords(123, lang=b'cz'), b'sto dvacet tři')
        self.assertEqual(numinwords(1000, lang=b'cz'), b'tisíc')
        self.assertEqual(numinwords(1001, lang=b'cz'), b'tisíc jedna')
        self.assertEqual(numinwords(2012, lang=b'cz'), b'dva tisíce dvanáct')
        self.assertEqual(numinwords(12519.85, lang=b'cz'), b'dvanáct tisíc pětset devatenáct celá osmdesát pět')
        self.assertEqual(numinwords(123.5, lang=b'cz'), b'sto dvacet tři celá pět')
        self.assertEqual(numinwords(1234567890, lang=b'cz'), b'miliarda dvěstě třicet čtyři miliony pětset šedesát sedm tisíc osmset devadesát')
        self.assertEqual(numinwords(215461407892039002157189883901676, lang=b'cz'), b'dvěstě patnáct quintillionů čtyřista šedesát jedna kvadriliard čtyřista sedm kvadrilionů osmset devadesát dva triliardy třicet devět trilionů dva biliardy sto padesát sedm bilionů sto osmdesát devět miliard osmset osmdesát tři miliony devětset jedna tisíc šestset sedmdesát šest')
        self.assertEqual(numinwords(719094234693663034822824384220291, lang=b'cz'), b'sedmset devatenáct quintillionů devadesát čtyři kvadriliardy dvěstě třicet čtyři kvadriliony šestset devadesát tři triliardy šestset šedesát tři triliony třicet čtyři biliardy osmset dvacet dva biliony osmset dvacet čtyři miliardy třista osmdesát čtyři miliony dvěstě dvacet tisíc dvěstě devadesát jedna')

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'cz', to=b'ordinal')

    def test_currency(self):
        self.assertEqual(numinwords(10.0, lang=b'cz', to=b'currency', currency=b'EUR'), b'deset euro, nula centů')
        self.assertEqual(numinwords(1.0, lang=b'cz', to=b'currency', currency=b'CZK'), b'jedna koruna, nula haléřů')
        self.assertEqual(numinwords(1234.56, lang=b'cz', to=b'currency', currency=b'EUR'), b'tisíc dvěstě třicet čtyři euro, padesát šest centů')
        self.assertEqual(numinwords(1234.56, lang=b'cz', to=b'currency', currency=b'CZK'), b'tisíc dvěstě třicet čtyři koruny, padesát šest haléřů')
        self.assertEqual(numinwords(101.11, lang=b'cz', to=b'currency', currency=b'EUR', separator=b' a'), b'sto jedna euro a jedenáct centů')
        self.assertEqual(numinwords(101.21, lang=b'cz', to=b'currency', currency=b'CZK', separator=b' a'), b'sto jedna korun a dvacet jedna haléřů')
        self.assertEqual(numinwords(-12519.85, lang=b'cz', to=b'currency', cents=False), b'mínus dvanáct tisíc pětset devatenáct euro, 85 centů')
        self.assertEqual(numinwords(123.5, lang=b'cz', to=b'currency', currency=b'CZK', separator=b' a'), b'sto dvacet tři koruny a padesát haléřů')
        self.assertEqual(numinwords(19.5, lang=b'cz', to=b'currency', cents=False), b'devatenáct euro, 50 centů')