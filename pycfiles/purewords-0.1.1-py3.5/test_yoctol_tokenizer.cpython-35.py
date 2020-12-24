# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/tokenizer/test_yoctol_tokenizer.py
# Compiled at: 2018-08-07 00:31:58
# Size of source mod 2**32: 410 bytes
import unittest
from purewords.tokenizer import YoctolTokenizer

class TestYoctolJiebaClass(unittest.TestCase):

    def setUp(self):
        self.yoctol_jieba = YoctolTokenizer()

    def test_cut(self):
        sentence = '有顆頭是優拓資訊的好夥伴_'
        answer = ['有顆頭', '是', '優拓資訊', '的', '好', '夥伴']
        self.assertEqual(answer, self.yoctol_jieba.cut(sentence))