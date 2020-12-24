# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_en_in.py
# Compiled at: 2020-04-17 01:12:29
from unittest import TestCase
from numinwords import numinwords

class numinwordsENINTest(TestCase):

    def test_cardinal(self):
        self.assertEqual(numinwords(100000.0, lang='en_IN'), 'one lakh')
        self.assertEqual(numinwords(1000000.0, lang='en_IN'), 'ten lakh')
        self.assertEqual(numinwords(10000000.0, lang='en_IN'), 'one crore')