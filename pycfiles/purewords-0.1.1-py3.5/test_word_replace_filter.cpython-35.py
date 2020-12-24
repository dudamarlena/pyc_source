# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_word_replace_filter.py
# Compiled at: 2018-08-07 00:31:33
# Size of source mod 2**32: 911 bytes
"""Word replace filter testcases"""
from unittest import TestCase
from unittest.mock import patch
from purewords.filters import WordReplaceFilter

class TestWordReplaceFilterClass(TestCase):

    def setUp(self):
        self.replace_dictionary = {'A': 'a', 
         'B': 'b'}
        self.filter = WordReplaceFilter(self.replace_dictionary)

    def test_add_replacement(self):
        self.filter.add_replacement('C', 'c')
        self.assertEqual(self.filter.replace_dictionary['C'], 'c')
        self.assertEqual(len(self.filter.replace_dictionary), 3)

    @patch('re.sub')
    def test_call(self, patch_sub):
        sentence = 'ABC'
        self.filter(sentence)
        self.assertEqual(patch_sub.call_count, len(self.replace_dictionary))