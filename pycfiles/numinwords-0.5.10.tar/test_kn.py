# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_kn.py
# Compiled at: 2020-04-17 01:13:25
from unittest import TestCase
from numinwords import numinwords

class numinwordsKNTest(TestCase):

    def test_numbers(self):
        self.assertEqual(numinwords(42, lang='kn'), 'ನಲವತ್ತ್ ಎರಡು')
        self.assertEqual(numinwords(893, lang='kn'), 'ಎಂಟು ನೂರ ತೊಂಬತ್ತ ಮೂರು')
        self.assertEqual(numinwords(1729, lang='kn'), 'ಒಂದು ಸಾವಿರ ಏಳು ನೂರ ಇಪ್ಪತ್ತ್ಒಂಬತ್ತು')
        self.assertEqual(numinwords(123, lang='kn'), 'ಒಂದು ನೂರ ಇಪ್ಪತ್ತ್ ಮೂರು')
        self.assertEqual(numinwords(32211, lang='kn'), 'ಮೂವತ್ತ್ಎರಡು ಸಾವಿರ ಎರಡು ನೂರ ಹನ್ನೊಂದು')

    def test_cardinal_for_float_number(self):
        self.assertEqual(numinwords(3.14, lang='kn'), 'ಮೂರು ಬಿಂದು ಒಂದು ನಾಲ್ಕು')
        self.assertEqual(numinwords(1.61803, lang='kn'), 'ಒಂದು ಬಿಂದು ಆರು ಒಂದು ಎಂಟು ಸೊನ್ನೆ ಮೂರು')

    def test_ordinal(self):
        self.assertEqual(numinwords(1, lang='kn', to='ordinal'), 'ಒಂದನೇ')
        self.assertEqual(numinwords(22, lang='kn', to='ordinal'), 'ಇಪ್ಪತ್ತ್ ಎರಡನೇ')
        self.assertEqual(numinwords(12, lang='kn', to='ordinal'), 'ಹನ್ನೆರಡನೇ')
        self.assertEqual(numinwords(130, lang='kn', to='ordinal'), 'ಒಂದು ನೂರ ಮೂವತ್ತನೇ')
        self.assertEqual(numinwords(1003, lang='kn', to='ordinal'), 'ಒಂದು ಸಾವಿರದ ಮೂರನೇ')
        self.assertEqual(numinwords(2, lang='kn', ordinal=True), 'ಎರಡನೇ')
        self.assertEqual(numinwords(5, lang='kn', ordinal=True), 'ಐದನೇ')
        self.assertEqual(numinwords(16, lang='kn', ordinal=True), 'ಹದಿನಾರನೇ')
        self.assertEqual(numinwords(113, lang='kn', ordinal=True), 'ಒಂದು ನೂರ ಹದಿಮೂರನೇ')

    def test_ordinal_num(self):
        self.assertEqual(numinwords(2, lang='kn', to='ordinal_num'), '2ಎರಡನೇ')
        self.assertEqual(numinwords(5, lang='kn', to='ordinal_num'), '5ಐದನೇ')
        self.assertEqual(numinwords(16, lang='kn', to='ordinal_num'), '16ಹದಿನಾರನೇ')
        self.assertEqual(numinwords(113, lang='kn', to='ordinal_num'), '113ಒಂದು ನೂರ ಹದಿಮೂರನೇ')