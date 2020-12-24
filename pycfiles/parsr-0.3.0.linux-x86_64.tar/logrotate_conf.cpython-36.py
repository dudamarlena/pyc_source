# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/logrotate_conf.py
# Compiled at: 2019-05-28 16:53:44
# Size of source mod 2**32: 1808 bytes
import string
from parsr import AnyChar, Choice, EOF, EOL, Forward, LeftCurly, LineEnd, Literal, Many, Number, OneLineComment, Opt, PosMarker, QuotedString, RightCurly, skip_none, String, WS, WSChar
from parsr.query import Directive, Entry, Section

def loads(data):
    return Entry(children=(Top(data)[0]))


def load(f):
    return loads(f.read())


def to_entries(x):
    ret = []
    for i in x:
        name, attrs, body = i
        if body:
            for n in [name.value] + attrs:
                ret.append(Section(name=n, children=body, lineno=(name.lineno)))

        else:
            attrs = [attrs] if not isinstance(attrs, list) else attrs
            ret.append(Directive(name=(name.value), attrs=attrs, lineno=(name.lineno)))

    return ret


scripts = set('postrotate prerotate firstaction lastaction preremove'.split())
Stanza = Forward()
Spaces = Many(WSChar)
Bare = String(set(string.printable) - (set(string.whitespace) | set('#{}\'"')))
Num = Number & (WSChar | LineEnd)
Comment = OneLineComment('#').map(lambda x: None)
ScriptStart = WS >> PosMarker(Choice([Literal(s) for s in scripts])) << WS
ScriptEnd = Literal('endscript')
Line = (WS >> AnyChar.until(EOL) << WS).map(lambda x: ''.join(x))
Lines = Line.until(ScriptEnd).map(lambda x: '\n'.join(x))
Script = ScriptStart + Lines << ScriptEnd
Script = Script.map(lambda x: [x[0], x[1], None])
BeginBlock = WS >> LeftCurly << WS
EndBlock = WS >> RightCurly
First = PosMarker(Bare | QuotedString) << Spaces
Attr = Spaces >> (Num | Bare | QuotedString) << Spaces
Rest = Many(Attr)
Block = BeginBlock >> Many(Stanza).map(skip_none).map(to_entries) << EndBlock
Stmt = WS >> (Script | First + Rest + Opt(Block)) << WS
Stanza <= WS >> (Stmt | Comment) << WS
Doc = Many(Stanza).map(skip_none).map(to_entries)
Top = Doc + EOF