# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_purewords.py
# Compiled at: 2018-08-07 00:31:46
# Size of source mod 2**32: 1138 bytes
import unittest, purewords
from purewords.__main__ import sentences_generator

class TestPurewordsClass(unittest.TestCase):

    def test_clean_sentence(self):
        sentence = '薄餡=柏憲=cph=cph_is_god\n讚讚讚！聯絡方式：cph@cph.tw, 0912345678'
        answer = '薄餡 柏憲 cph cph is god 讚 讚 讚 聯絡 方式 _url_ _phone_'
        self.assertEqual(answer, purewords.clean_sentence(sentence))

    def test_clean_document(self):
        sentence = '薄餡=柏憲=cph=cph_is_god\n讚讚讚！聯絡方式：cph@cph.tw, 0912345678'
        answer = ['薄餡 柏憲 cph cph is god', '讚 讚 讚', '聯絡 方式 _url_ _phone_']
        self.assertEqual(answer, purewords.clean_document(sentence))

    def test_sentence_generator(self):
        test_corpus_path = 'test/test_corpus.txt'
        answer = [
         '大腸花們快來看看,有沒有覺得很相似的畫面.原來這樣的行為在別國看來較暴民.',
         '美国推销的民主太他妈坑人了']
        sentences = sentences_generator(test_corpus_path, 2).__next__()
        self.assertEqual(answer, sentences)