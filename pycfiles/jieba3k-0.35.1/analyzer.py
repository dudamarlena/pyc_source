# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../jieba\analyse\analyzer.py
# Compiled at: 2014-11-12 21:17:09
from whoosh.analysis import RegexAnalyzer, LowercaseFilter, StopFilter, StemFilter
from whoosh.analysis import Tokenizer, Token
from whoosh.lang.porter import stem
import jieba, re
STOP_WORDS = frozenset(('a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'can', 'for',
                        'from', 'have', 'if', 'in', 'is', 'it', 'may', 'not', 'of',
                        'on', 'or', 'tbd', 'that', 'the', 'this', 'to', 'us', 'we',
                        'when', 'will', 'with', 'yet', 'you', 'your', '的', '了', '和'))
accepted_chars = re.compile('[一-龥]+')

class ChineseTokenizer(Tokenizer):

    def __call__(self, text, **kargs):
        words = jieba.tokenize(text, mode='search')
        token = Token()
        for w, start_pos, stop_pos in words:
            if not accepted_chars.match(w) and len(w) <= 1:
                continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token


def ChineseAnalyzer(stoplist=STOP_WORDS, minsize=1, stemfn=stem, cachesize=50000):
    return ChineseTokenizer() | LowercaseFilter() | StopFilter(stoplist=stoplist, minsize=minsize) | StemFilter(stemfn=stemfn, ignore=None, cachesize=cachesize)