# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/kvpairs.py
# Compiled at: 2019-05-28 16:54:24
# Size of source mod 2**32: 2032 bytes
"""
This module parses files that are simple lists of key values pairs. It supports
keys without values and skips blank lines and single line comments.

You can configure the k/v separator character and the comment start character.

It returns a dictionary. The last definition for a given key sets its value.
"""
import operator, string
from functools import reduce
from parsr import EOF, EOL, InSet, LineEnd, Many, Number, OneLineComment, Opt, PosMarker, skip_none, String, WS, WSChar
from parsr.query import Entry

def loads(s, sep_chars='=:', comment_chars='#;'):
    return KVPairs(sep_chars=sep_chars, comment_chars=comment_chars).loads(s)


def load(f, sep_chars='=:', comment_chars='#;'):
    return loads((f.read()), sep_chars=sep_chars, comment_chars=comment_chars)


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