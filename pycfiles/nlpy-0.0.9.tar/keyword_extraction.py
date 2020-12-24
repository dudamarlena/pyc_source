# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/tasks/keyword_extraction.py
# Compiled at: 2014-11-26 02:20:18
from nlpy.ex.keyword import DefaultKeywordExtractor
from nlpy.basic import DefaultLemmatizer
from nlpy.basic import DefaultRecaser
from nlpy.basic import DefaultTokenizer

class KeywordExtractor(object):

    def __init__(self):
        self._kwex = DefaultKeywordExtractor()
        self._lem = DefaultLemmatizer()
        self._recaser = DefaultRecaser()
        self._tokenizer = DefaultTokenizer()

    def extract(self, sent):
        keywords = self._kwex.extract(map(self._recaser.recase, map(self._lem.lemmatize, map(str.lower, self._tokenizer.tokenize(sent)))))
        return keywords

    def extract_weighted(self, sent):
        keywords = self._kwex.extract_weighted(map(self._recaser.recase, map(self._lem.lemmatize, map(str.lower, self._tokenizer.tokenize(sent)))))
        return keywords

    @staticmethod
    def serve(params):
        global keyword_extractor
        if 'keyword_extractor' not in globals():
            keyword_extractor = KeywordExtractor()
        return {'output': keyword_extractor.extract(params['input'])}