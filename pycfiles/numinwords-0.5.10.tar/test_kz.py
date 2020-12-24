# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_kz.py
# Compiled at: 2020-04-17 01:13:31
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsKZTest(TestCase):

    def test_to_cardinal(self):
        self.maxDiff = None
        self.assertEqual(numinwords(7, lang=b'kz'), b'жеті')
        self.assertEqual(numinwords(23, lang=b'kz'), b'жиырма үш')
        self.assertEqual(numinwords(145, lang=b'kz'), b'жүз қырық бес')
        self.assertEqual(numinwords(2869, lang=b'kz'), b'екі мың сегіз жүз алпыс тоғыз')
        self.assertEqual(numinwords(-789000125, lang=b'kz'), b'минус жеті жүз сексен тоғыз миллион жүз жиырма бес')
        self.assertEqual(numinwords(84932, lang=b'kz'), b'сексен төрт мың тоғыз жүз отыз екі')
        return

    def test_to_cardinal_floats(self):
        self.assertEqual(numinwords(100.67, lang=b'kz'), b'жүз бүтін алпыс жеті')
        self.assertEqual(numinwords(0.7, lang=b'kz'), b'нөл бүтін жеті')
        self.assertEqual(numinwords(1.73, lang=b'kz'), b'бір бүтін жетпіс үш')

    def test_to_ordinal(self):
        with self.assertRaises(NotImplementedError):
            numinwords(1, lang=b'kz', to=b'ordinal')

    def test_to_currency(self):
        self.assertEqual(numinwords(25.24, lang=b'kz', to=b'currency', currency=b'KZT'), b'жиырма бес теңге, жиырма төрт тиын')
        self.assertEqual(numinwords(1996.4, lang=b'kz', to=b'currency', currency=b'KZT'), b'бір мың тоғыз жүз тоқсан алты теңге, қырық тиын')
        self.assertEqual(numinwords(632924.51, lang=b'kz', to=b'currency', currency=b'KZT'), b'алты жүз отыз екі мың тоғыз жүз жиырма төрт теңге, елу бір тиын')
        self.assertEqual(numinwords(632924.513, lang=b'kz', to=b'currency', currency=b'KZT'), b'алты жүз отыз екі мың тоғыз жүз жиырма төрт теңге, елу бір тиын')
        self.assertEqual(numinwords(987654321.123, lang=b'kz', to=b'currency', currency=b'KZT'), b'тоғыз жүз сексен жеті миллион алты жүз елу төрт мың үш жүз жиырма бір теңге, он екі тиын')