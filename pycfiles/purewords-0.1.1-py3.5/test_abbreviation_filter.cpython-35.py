# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_abbreviation_filter.py
# Compiled at: 2018-08-07 00:31:06
# Size of source mod 2**32: 662 bytes
"""abbreviation filter testcases"""
from unittest import TestCase
from purewords.filters import abbreviation_filter

class TestAbbreviationFilter(TestCase):

    def setUp(self):
        self.filter = abbreviation_filter

    def test_abbreviation_filter(self):
        sentence = "I'm Mr. Qoo. She's Mrs. M. " + "You're great. I'd and I'll " + 'like to show you something'
        answer = 'I am Mr. Qoo. She Mrs. M. ' + 'you are great. I would and ' + 'I will like to show you something'
        self.assertEqual(answer, self.filter(sentence))