# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/csams/git_repos/personal/parsr/lib/python3.6/site-packages/parsr/examples/json_parser.py
# Compiled at: 2019-10-05 08:12:29
# Size of source mod 2**32: 851 bytes
"""
json_parser handles primitive json parsing. It doesn't handle unicode or
numbers in scientific notation.
"""
from parsr import Colon, Comma, EOF, Forward, Literal, LeftBracket, LeftCurly, Number, RightBracket, RightCurly, QuotedString, WS

def loads(data):
    return Top(data)[0]


def load(f):
    return loads(f.read())


JsonArray = Forward()
JsonObject = Forward()
TRUE = Literal('true', value=True)
FALSE = Literal('false', value=False)
NULL = Literal('null', value=None)
SimpleValue = Number | QuotedString | JsonObject | JsonArray | TRUE | FALSE | NULL
JsonValue = WS >> SimpleValue << WS
Key = QuotedString << Colon
KVPairs = ((WS >> Key) + JsonValue).sep_by(Comma)
JsonArray <= LeftBracket >> JsonValue.sep_by(Comma) << RightBracket
JsonObject <= LeftCurly >> KVPairs.map(dict) << RightCurly
Top = JsonValue + EOF