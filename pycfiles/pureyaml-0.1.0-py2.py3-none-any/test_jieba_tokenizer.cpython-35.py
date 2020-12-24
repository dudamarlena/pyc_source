# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/tokenizer/test_jieba_tokenizer.py
# Compiled at: 2018-08-07 00:31:53
# Size of source mod 2**32: 938 bytes
__doc__ = 'jieba tokenizer testcases'
from unittest import TestCase
from unittest.mock import patch
from purewords.tokenizer import JiebaTokenizer

class TestJiebaTokenizerClass(TestCase):

    def setUp(self):
        self.tokenizer = JiebaTokenizer()

    def test_cut(self):
        sentence = '你好嗎？_我很好。'
        result = self.tokenizer.cut(sentence)
        self.assertTrue(len(result) > 0)
        self.assertNotIn('_', result)

    @patch('jieba.Tokenizer.add_word')
    def test_add_word(self, patch_add_word):
        new_word = '哈哈'
        self.tokenizer.add_word(new_word)
        patch_add_word.assert_called_once_with(new_word, None, None)

    @patch('jieba.Tokenizer.add_word')
    def test_add_words(self, patch_add_word):
        new_words = [str(i) for i in range(10)]
        self.tokenizer.add_words(new_words)
        self.assertEqual(patch_add_word.call_count, 10)