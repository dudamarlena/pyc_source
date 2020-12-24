# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/tokenizer/test_whitespace_tokenizer.py
# Compiled at: 2018-08-07 00:31:55
# Size of source mod 2**32: 489 bytes
import unittest
from purewords.tokenizer import WhitespaceTokenizer

class TestWhiteSpaceTokenizer(unittest.TestCase):

    def setUp(self):
        self.whitespace_tokenizer = WhitespaceTokenizer()

    def test_cut(self):
        sentence = 'Hello, my name is cph_cph. cph is _ wonderful.'
        answer = [
         'Hello,', 'my', 'name', 'is', 'cph_cph.',
         'cph', 'is', 'wonderful.']
        self.assertEqual(answer, self.whitespace_tokenizer.cut(sentence))