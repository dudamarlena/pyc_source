# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/examples/corosync_conf.py
# Compiled at: 2019-11-14 13:57:46
"""
corosync_conf parses corosync configuration files into nested dictionaries.
"""
import string
from insights.parsr import EOF, Forward, InSet, LeftCurly, Lift, LineEnd, Literal, RightCurly, Many, Number, OneLineComment, PosMarker, skip_none, String, QuotedString, WS, WSChar
from insights.parsr.query import Directive, Entry, Section

def loads(data):
    return Entry(children=Top(data))


def load(f):
    return loads(f.read())


def to_entry(name, rest):
    if isinstance(rest, list):
        return Section(name=name.value, children=rest, lineno=name.lineno)
    return Directive(name=name.value, attrs=[rest], lineno=name.lineno)


Sep = InSet(':=')
Stmt = Forward()
Num = Number & (WSChar | LineEnd)
NULL = Literal('none', value=None)
Comment = WS >> OneLineComment('#').map(lambda x: None)
BeginBlock = WS >> LeftCurly << WS
EndBlock = WS >> RightCurly << WS
Bare = String(set(string.printable) - (set(string.whitespace) | set('#{}\'"')))
Name = WS >> PosMarker(String(string.ascii_letters + '_' + string.digits)) << WS
Value = WS >> (Num | NULL | QuotedString | Bare) << WS
Block = BeginBlock >> Many(Stmt).map(skip_none) << EndBlock
Stanza = Lift(to_entry) * Name * (Block | Sep >> Value) | Comment
Stmt <= WS >> Stanza << WS
Doc = Many(Stmt).map(skip_none)
Top = Doc << EOF