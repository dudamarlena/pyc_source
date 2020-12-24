# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/tests/test_pos_marker.py
# Compiled at: 2019-01-29 13:57:17
# Size of source mod 2**32: 1742 bytes
import operator, string
from functools import reduce
from parsr import EOF, EOL, InSet, LineEnd, Many, Number, OneLineComment, Opt, PosMarker, skip_none, String, WS, WSChar
from parsr.query import Entry
DATA = '\n# this is a config file\na = 15\nb = a string\nvalueless\nd = 1.14\n\n# another section\n+valueless  # no value\ne = hello   # a value\n#\n'

def to_entry(ms):
    children = []
    for mark, value in ms:
        children.append(Entry(name=(mark.value), attrs=[value], lineno=(mark.lineno)))

    return Entry(children=children)


class KVPairs:

    def __init__(self, sep_chars='=:', comment_chars='#;'):
        eol_chars = set('\n\r')
        sep_chars = set(sep_chars)
        comment_chars = set(comment_chars)
        key_chars = set(string.printable) - (sep_chars | eol_chars | comment_chars)
        value_chars = set(string.printable) - (eol_chars | comment_chars)
        OLC = reduce(operator.__or__, [OneLineComment(c) for c in comment_chars])
        Comment = (WS >> OLC).map(lambda x: None)
        Num = Number & (WSChar | LineEnd)
        Key = WS >> PosMarker(String(key_chars).map(lambda x: x.strip())) << WS
        Sep = InSet(sep_chars)
        Value = WS >> (Num | String(value_chars).map(lambda x: x.strip()))
        KVPair = (Key + Opt((Sep + Value), default=[None, None])).map(lambda a: (a[0], a[1][1]))
        Line = Comment | KVPair | EOL.map(lambda x: None)
        Doc = Many(Line).map(skip_none).map(to_entry)
        self.Top = Doc + EOF

    def loads(self, s):
        return self.Top(s)[0]

    def load(self, f):
        return self.loads(f.read())


def test_marker():
    kvp = KVPairs()
    res = kvp.loads(DATA)
    if not res:
        raise AssertionError
    elif not res['+valueless'][0].lineno == 9:
        raise AssertionError