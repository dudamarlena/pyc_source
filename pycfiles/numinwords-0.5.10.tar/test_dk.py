# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_dk.py
# Compiled at: 2020-04-17 01:12:27
from __future__ import unicode_literals
from unittest import TestCase
from numinwords import numinwords

class numinwordsDKTest(TestCase):

    def test_ordinal(self):
        self.assertEqual(numinwords(1, to=b'ordinal', lang=b'dk'), b'første')
        self.assertEqual(numinwords(5, to=b'ordinal', lang=b'dk'), b'femte')

    def test_cardinal(self):
        self.assertEqual(numinwords(0, to=b'cardinal', lang=b'dk'), b'nul')
        self.assertEqual(numinwords(1, to=b'cardinal', lang=b'dk'), b'et')
        self.assertEqual(numinwords(2, to=b'cardinal', lang=b'dk'), b'to')
        self.assertEqual(numinwords(5, to=b'cardinal', lang=b'dk'), b'fem')
        self.assertEqual(numinwords(8, to=b'cardinal', lang=b'dk'), b'otte')
        self.assertEqual(numinwords(18, to=b'cardinal', lang=b'dk'), b'atten')
        self.assertEqual(numinwords(45, to=b'cardinal', lang=b'dk'), b'femogfyrre')