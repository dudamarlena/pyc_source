# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/nginx_conf.py
# Compiled at: 2019-05-28 16:53:28
# Size of source mod 2**32: 1125 bytes
import string
from parsr import EOF, Forward, LeftCurly, Lift, LineEnd, RightCurly, Many, Number, OneLineComment, PosMarker, SemiColon, SingleQuotedString, skip_none, String, WS, WSChar
from parsr.query import Entry

def loads(data):
    return Top(data)[0]


def load(f):
    return loads(f.read())


def to_entry(name, attrs, body):
    if body == ';':
        return Entry(name=(name.value), attrs=attrs, lineno=(name.lineno))
    else:
        return Entry(name=(name.value), attrs=attrs, children=body, lineno=(name.lineno))


Stmt = Forward()
Num = Number & (WSChar | LineEnd)
Comment = OneLineComment('#').map(lambda x: None)
BeginBlock = WS >> LeftCurly << WS
EndBlock = WS >> RightCurly << WS
Bare = String(set(string.printable) - (set(string.whitespace) | set('#;{}\'"')))
Name = WS >> PosMarker(String(string.ascii_letters + '_')) << WS
Attr = WS >> (Num | Bare | SingleQuotedString) << WS
Attrs = Many(Attr)
Block = BeginBlock >> Many(Stmt).map(skip_none) << EndBlock
Stanza = Lift(to_entry) * Name * Attrs * (Block | SemiColon) | Comment
Stmt <= WS >> Stanza << WS
Doc = Many(Stmt).map(skip_none)
Top = Doc + EOF