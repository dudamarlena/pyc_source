# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/examples/httpd_conf.py
# Compiled at: 2019-11-14 13:57:46
import string
from insights.parsr import Char, EOF, EOL, EndTagName, Forward, FS, GT, LT, Letters, Lift, LineEnd, Many, Number, OneLineComment, PosMarker, QuotedString, skip_none, StartTagName, String, WS, WSChar
from insights.parsr.query import Directive, Entry, Section

def loads(data):
    return Entry(children=Top(data)[0])


def load(f):
    return loads(f.read())


def simple_to_entry(name, attrs):
    return Directive(name=name.value, attrs=attrs, lineno=name.lineno)


def complex_to_entry(tag, children):
    name, attrs = tag
    return Section(name=name.value, attrs=attrs, children=children, lineno=name.lineno)


Complex = Forward()
Num = Number & (WSChar | LineEnd)
Cont = Char('\\') + EOL
StartName = WS >> PosMarker(StartTagName(Letters)) << WS
EndName = WS >> EndTagName(Letters) << WS
Comment = (WS >> OneLineComment('#')).map(lambda x: None)
AttrStart = Many(WSChar)
AttrEnd = Many(WSChar) + Cont | Many(WSChar)
BareAttr = String(set(string.printable) - (set(string.whitespace) | set(';{}<>\\\'"')))
Attr = AttrStart >> (Num | BareAttr | QuotedString) << AttrEnd
Attrs = Many(Attr)
StartTag = WS + LT >> StartName + Attrs << GT + WS
EndTag = WS + LT + FS >> EndName << GT + WS
Simple = WS >> Lift(simple_to_entry) * PosMarker(Letters) * Attrs << WS
Stanza = Simple | Complex | Comment
Complex <= Lift(complex_to_entry) * StartTag * Many(Stanza).map(skip_none) << EndTag
Doc = Many(Stanza).map(skip_none)
Top = Doc + EOF