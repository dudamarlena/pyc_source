# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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