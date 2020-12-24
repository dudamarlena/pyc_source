# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/common/test_titlecase.py
# Compiled at: 2015-11-08 18:30:19
import re, titlecase as tc
from tvrenamer.tests import base
tc.ALL_CAPS = re.compile('^[A-Z\\s%s]+$' % tc.PUNCT)

class TitlecaseTest(base.BaseTest):

    def test_from_all_lower(self):
        self.assertEqual(tc.titlecase('a very simple title'), 'A Very Simple Title')
        self.assertEqual(tc.titlecase("o'shea is not a good band"), "O'Shea Is Not a Good Band")
        self.assertEqual(tc.titlecase("o'do not wanton with those eyes"), "O'Do Not Wanton With Those Eyes")

    def test_from_all_upper(self):
        self.assertEqual(tc.titlecase('A VERY SIMPLE TITLE'), 'A Very Simple Title')
        self.assertEqual(tc.titlecase('W.KI.N.YR.'), 'W.KI.N.YR.')

    def test_from_notation(self):
        self.assertEqual(tc.titlecase('funtime.example.com'), 'funtime.example.com')
        self.assertEqual(tc.titlecase('Funtime.Example.Com'), 'Funtime.Example.Com')

    def test_from_location(self):
        self.assertEqual(tc.titlecase('S09E01 - sample episode'), 'S09E01 - Sample Episode')
        self.assertEqual(tc.titlecase('sample series/season 9/S09E01 - sample episode'), 'Sample Series/Season 9/S09E01 - Sample Episode')

    def test_from_mac(self):
        self.assertEqual(tc.titlecase('macyhg'), 'Macyhg')

    def test_from_asis(self):
        self.assertEqual(tc.titlecase('A Very Simple Title'), 'A Very Simple Title')