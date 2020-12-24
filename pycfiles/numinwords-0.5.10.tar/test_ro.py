# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_ro.py
# Compiled at: 2020-04-17 01:14:13
from unittest import TestCase
from numinwords import numinwords

class numinwordsROTest(TestCase):

    def test_ordinal(self):
        self.assertEqual(numinwords(1, lang='ro', to='ordinal'), 'primul')
        self.assertEqual(numinwords(22, lang='ro', to='ordinal'), 'al douăzeci și doilea')
        self.assertEqual(numinwords(21, lang='ro', to='ordinal'), 'al douăzeci și unulea')
        self.assertEqual(numinwords(12, lang='ro', to='ordinal'), 'al doisprezecelea')
        self.assertEqual(numinwords(130, lang='ro', to='ordinal'), 'al o sută treizecilea')
        self.assertEqual(numinwords(1003, lang='ro', to='ordinal'), 'al o mie treilea')

    def test_ordinal_num(self):
        self.assertEqual(numinwords(1, lang='ro', to='ordinal_num'), '1-ul')
        self.assertEqual(numinwords(10, lang='ro', to='ordinal_num'), 'al 10-lea')
        self.assertEqual(numinwords(21, lang='ro', to='ordinal_num'), 'al 21-lea')
        self.assertEqual(numinwords(102, lang='ro', to='ordinal_num'), 'al 102-lea')
        self.assertEqual(numinwords(73, lang='ro', to='ordinal_num'), 'al 73-lea')

    def test_cardinal_for_float_number(self):
        self.assertEqual(numinwords(12.5, lang='ro'), 'doisprezece virgulă cinci')
        self.assertEqual(numinwords(12.51, lang='ro'), 'doisprezece virgulă cinci unu')
        self.assertEqual(numinwords(12.53, lang='ro'), 'doisprezece virgulă cinci trei')
        self.assertEqual(numinwords(12.59, lang='ro'), 'doisprezece virgulă cinci nouă')

    def test_big_numbers(self):
        self.assertEqual(numinwords(1000000, lang='ro'), 'un milion')
        self.assertEqual(numinwords(1000000000, lang='ro'), 'un miliard')
        self.assertEqual(numinwords(33000000, lang='ro'), 'treizeci și trei milioane')
        self.assertEqual(numinwords(247000000000, lang='ro'), 'două sute patruzeci și șapte de miliarde')

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            numinwords('1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

    def test_to_currency(self):
        self.assertEqual(numinwords(1000, lang='ro', to='currency'), 'una mie de lei')
        self.assertEqual(numinwords(101, lang='ro', to='currency'), 'una sută unu lei')
        self.assertEqual(numinwords(100, lang='ro', to='currency'), 'una sută de lei')
        self.assertEqual(numinwords(38.4, lang='ro', to='currency'), 'treizeci și opt de lei și patruzeci de bani')
        self.assertEqual(numinwords(1.01, lang='ro', to='currency'), 'un leu și un ban')
        self.assertEqual(numinwords(4778.0, lang='ro', to='currency'), 'patru mii șapte sute șaptezeci și opt de lei')
        self.assertEqual(numinwords(4778.32, lang='ro', to='currency'), 'patru mii șapte sute șaptezeci și opt de lei și treizeci și doi de bani')
        self.assertEqual(numinwords(1207, lang='ro', to='currency'), 'una mie două sute șapte lei')
        self.assertEqual(numinwords(22000, lang='ro', to='currency'), 'douăzeci și două de mii de lei')
        self.assertEqual(numinwords(80000, lang='ro', to='currency'), 'optzeci de mii de lei')
        self.assertEqual(numinwords(123456789, lang='ro', to='currency'), 'una sută douăzeci și trei milioane patru sute cincizeci și șase de mii șapte sute optzeci și nouă de lei')

    def test_to_year(self):
        self.assertEqual(numinwords(1989, lang='ro', to='year'), 'o mie nouă sute optzeci și nouă')
        self.assertEqual(numinwords(1984, lang='ro', to='year'), 'o mie nouă sute optzeci și patru')
        self.assertEqual(numinwords(2018, lang='ro', to='year'), 'două mii optsprezece')
        self.assertEqual(numinwords(1066, lang='ro', to='year'), 'o mie șaizeci și șase')
        self.assertEqual(numinwords(5000, lang='ro', to='year'), 'cinci mii')
        self.assertEqual(numinwords(2001, lang='ro', to='year'), 'două mii unu')
        self.assertEqual(numinwords(905, lang='ro', to='year'), 'nouă sute cinci')
        self.assertEqual(numinwords(6600, lang='ro', to='year'), 'șase mii șase sute')
        self.assertEqual(numinwords(1600, lang='ro', to='year'), 'o mie șase sute')
        self.assertEqual(numinwords(700, lang='ro', to='year'), 'șapte sute')
        self.assertEqual(numinwords(50, lang='ro', to='year'), 'cincizeci')
        self.assertEqual(numinwords(0, lang='ro', to='year'), 'zero')
        self.assertEqual(numinwords(10, lang='ro', to='year'), 'zece')
        self.assertEqual(numinwords(-44, lang='ro', to='year'), 'patruzeci și patru î.Hr.')
        self.assertEqual(numinwords(-44, lang='ro', to='year', suffix='î.e.n.'), 'patruzeci și patru î.e.n.')
        self.assertEqual(numinwords(1, lang='ro', to='year', suffix='d.Hr.'), 'unu d.Hr.')
        self.assertEqual(numinwords(-66000000, lang='ro', to='year'), 'șaizeci și șase milioane î.Hr.')