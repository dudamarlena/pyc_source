# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_pattern_replace_filter.py
# Compiled at: 2018-08-07 00:31:17
# Size of source mod 2**32: 831 bytes
__doc__ = 'pattern replace filter testcases'
from unittest import TestCase
from unittest.mock import patch
from purewords.filters import PatternReplaceFilter

class TestPatternReplaceFilterClass(TestCase):

    def setUp(self):
        self.patterns = [
         'A']
        self.replacement = 'a'
        self.filter = PatternReplaceFilter(self.patterns, self.replacement)

    def test_add_pattern(self):
        pattern = '\\d+'
        self.filter.add_pattern(pattern)
        self.assertEqual(self.filter.patterns[(-1)], pattern)

    @patch('re.sub')
    def test_call(self, patch_sub):
        sentence = ''
        self.filter(sentence)
        patch_sub.assert_called_once_with(self.patterns[0], self.replacement, sentence)