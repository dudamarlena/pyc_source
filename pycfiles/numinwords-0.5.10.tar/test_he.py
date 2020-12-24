# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_he.py
# Compiled at: 2020-04-17 01:13:07
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsHETest(TestCase):
    maxDiff = None

    def test_0(self):
        self.assertEqual(numinwords(0, lang=b'he'), b'אפס')

    def test_1_to_10(self):
        self.assertEqual(numinwords(1, lang=b'he'), b'אחת')
        self.assertEqual(numinwords(2, lang=b'he'), b'שתים')
        self.assertEqual(numinwords(7, lang=b'he'), b'שבע')
        self.assertEqual(numinwords(10, lang=b'he'), b'עשר')

    def test_11_to_19(self):
        self.assertEqual(numinwords(11, lang=b'he'), b'אחת עשרה')
        self.assertEqual(numinwords(13, lang=b'he'), b'שלש עשרה')
        self.assertEqual(numinwords(15, lang=b'he'), b'חמש עשרה')
        self.assertEqual(numinwords(16, lang=b'he'), b'שש עשרה')
        self.assertEqual(numinwords(19, lang=b'he'), b'תשע עשרה')

    def test_20_to_99(self):
        self.assertEqual(numinwords(20, lang=b'he'), b'עשרים')
        self.assertEqual(numinwords(23, lang=b'he'), b'עשרים ושלש')
        self.assertEqual(numinwords(28, lang=b'he'), b'עשרים ושמונה')
        self.assertEqual(numinwords(31, lang=b'he'), b'שלשים ואחת')
        self.assertEqual(numinwords(40, lang=b'he'), b'ארבעים')
        self.assertEqual(numinwords(66, lang=b'he'), b'ששים ושש')
        self.assertEqual(numinwords(92, lang=b'he'), b'תשעים ושתים')

    def test_100_to_999(self):
        self.assertEqual(numinwords(100, lang=b'he'), b'מאה')
        self.assertEqual(numinwords(111, lang=b'he'), b'מאה ואחת עשרה')
        self.assertEqual(numinwords(150, lang=b'he'), b'מאה וחמישים')
        self.assertEqual(numinwords(196, lang=b'he'), b'מאה תשעים ושש')
        self.assertEqual(numinwords(200, lang=b'he'), b'מאתיים')
        self.assertEqual(numinwords(210, lang=b'he'), b'מאתיים ועשר')
        self.assertEqual(numinwords(701, lang=b'he'), b'שבע מאות ואחת')

    def test_1000_to_9999(self):
        self.assertEqual(numinwords(1000, lang=b'he'), b'אלף')
        self.assertEqual(numinwords(1001, lang=b'he'), b'אלף ואחת')
        self.assertEqual(numinwords(1500, lang=b'he'), b'אלף וחמש מאות')
        self.assertEqual(numinwords(7378, lang=b'he'), b'שבעת אלפים שלש מאות שבעים ושמונה')
        self.assertEqual(numinwords(2000, lang=b'he'), b'אלפיים')
        self.assertEqual(numinwords(2100, lang=b'he'), b'אלפיים ומאה')
        self.assertEqual(numinwords(6870, lang=b'he'), b'ששת אלפים שמונה מאות ושבעים')