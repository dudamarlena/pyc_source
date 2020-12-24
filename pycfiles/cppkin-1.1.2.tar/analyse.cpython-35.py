# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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