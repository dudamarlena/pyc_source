# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/multipath_conf.py
# Compiled at: 2019-05-28 16:55:47
# Size of source mod 2**32: 1233 bytes
"""
multipath_conf parses multipath.conf configuration files into nested
dictionaries.
"""
import string
from parsr import EOF, Forward, LeftCurly, Lift, Literal, LineEnd, RightCurly, Many, Number, OneLineComment, PosMarker, skip_none, String, QuotedString, WS, WSChar
from parsr.query import Entry

def loads(data):
    return Entry(children=(Top(data)[0]))


def load(f):
    return loads(f.read())


def to_entry(name, rest):
    if isinstance(rest, list):
        return Entry(name=(name.value), children=rest, lineno=(name.lineno))
    else:
        return Entry(name=(name.value), attrs=[rest], lineno=(name.lineno))


Stmt = Forward()
Num = Number & (WSChar | LineEnd)
NULL = Literal('none', value=None)
Comment = WS >> OneLineComment('#').map(lambda x: None)
BeginBlock = WS >> LeftCurly << WS
EndBlock = WS >> RightCurly << WS
Bare = String(set(string.printable) - (set(string.whitespace) | set('#{}\'"')))
Name = WS >> PosMarker(String(string.ascii_letters + '_')) << WS
Value = WS >> (Num | NULL | QuotedString | Bare) << WS
Block = BeginBlock >> Many(Stmt).map(skip_none) << EndBlock
Stanza = Lift(to_entry) * Name * (Block | Value) | Comment
Stmt <= WS >> Stanza << WS
Doc = Many(Stmt).map(skip_none)
Top = Doc + EOF