# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gan/project/source/testgit/yaha/yaha/analyse/analyzer.py
# Compiled at: 2013-08-21 03:57:22
from whoosh.analysis import RegexAnalyzer, LowercaseFilter, StopFilter, StemFilter
from whoosh.analysis import Tokenizer, Token
from whoosh.lang.porter import stem
from yaha import Cuttor, SurnameCutting, SuffixCutting, get_dict, DICTS
import re
STOP_WORDS = None

def __init_stop_words():
    global STOP_WORDS
    stop_words = []
    for (t, v) in get_dict(DICTS.EXT_STOPWORD).iteritems():
        stop_words.append(t)

    for (t, v) in get_dict(DICTS.STOPWORD).iteritems():
        stop_words.append(t)

    for (t, v) in get_dict(DICTS.STOP_SENTENCE).iteritems():
        stop_words.append(t)

    STOP_WORDS = frozenset(stop_words)


__init_stop_words()
accepted_chars = re.compile('[一-龥]+')
_cuttor = Cuttor()
_cuttor.set_stage1_regex(re.compile('(\\d+)|([a-zA-Z]+)', re.I | re.U))
_cuttor.add_stage(SurnameCutting())
_cuttor.add_stage(SuffixCutting())

class ChineseTokenizer(Tokenizer):

    def __call__(self, text, **kargs):
        words = _cuttor.tokenize(text, search=True)
        token = Token()
        for (w, start_pos, stop_pos) in words:
            if not accepted_chars.match(w):
                if len(w) > 1:
                    pass
                else:
                    continue
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = stop_pos
            yield token


def ChineseAnalyzer(stoplist=STOP_WORDS, minsize=1, stemfn=stem, cachesize=50000):
    return ChineseTokenizer() | LowercaseFilter() | StopFilter(stoplist=stoplist, minsize=minsize) | StemFilter(stemfn=stemfn, ignore=None, cachesize=cachesize)