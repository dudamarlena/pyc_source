# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/basic/nltk_tokenizers.py
# Compiled at: 2014-11-06 20:05:41
import nltk
from abstract_tokenizer import AbstractTokenizer

class NLTKEnglishTokenizer(AbstractTokenizer):

    def tokenize(self, sent):
        """
        :type sent: str
        :rtype: list of str
        """
        return nltk.word_tokenize(sent)

    @staticmethod
    def serve(param):
        """
        For serve web requests.
        """
        output = NLTKEnglishTokenizer().tokenize(param['input'])
        return {'output': output}