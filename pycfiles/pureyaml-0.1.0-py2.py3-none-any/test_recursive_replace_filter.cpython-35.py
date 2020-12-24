# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/filters/test_recursive_replace_filter.py
# Compiled at: 2018-08-07 00:31:21
# Size of source mod 2**32: 530 bytes
__doc__ = 'recursive replace filter testcase'
from unittest import TestCase
from purewords.filters import RecursiveReplaceFilter

class TestRecursiveReplaceFilterClass(TestCase):

    def setUp(self):
        self.pattern = 'AA'
        self.replacement = 'A'
        self.filter = RecursiveReplaceFilter(self.pattern, self.replacement)

    def test_call(self):
        sentence = 'AAAA'
        result = self.filter(sentence)
        self.assertEqual(result, 'A')