# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bung/.virtualenvs/whatlangid/lib/python3.5/site-packages/cppjieba_py/analyse.py
# Compiled at: 2018-06-08 19:27:51
# Size of source mod 2**32: 695 bytes
from libcppjieba import get_default_keyword_extractor, get_default_textrank_extractor
from libcppjieba import KeywordExtractor, TextRankExtractor
TextRank = TextRankExtractor
TFIDF = KeywordExtractor

def _textrank(self, sentence, topK=20, withWeight=False):
    if not withWeight:
        return self.textrank_no_weight(sentence, topK)
    else:
        return self.textrank_with_weight(sentence, topK)


setattr(TextRank, 'textrank', _textrank)
keywordExtractor = get_default_keyword_extractor()
textrankExtractor = get_default_textrank_extractor()
extract_tags = keywordExtractor.extract_tags
textrank = textrankExtractor.textrank