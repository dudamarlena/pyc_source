# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xpath/lexrules.py
# Compiled at: 2016-02-19 17:15:24
"""XPath lexing rules.

To understand how this module works, it is valuable to have a strong
understanding of the `ply <http://www.dabeaz.com/ply/>` module.
"""
from __future__ import unicode_literals
operator_names = {b'or': b'OR_OP', 
   b'and': b'AND_OP', 
   b'div': b'DIV_OP', 
   b'mod': b'MOD_OP'}
tokens = [
 b'PATH_SEP',
 b'ABBREV_PATH_SEP',
 b'ABBREV_STEP_SELF',
 b'ABBREV_STEP_PARENT',
 b'AXIS_SEP',
 b'ABBREV_AXIS_AT',
 b'OPEN_PAREN',
 b'CLOSE_PAREN',
 b'OPEN_BRACKET',
 b'CLOSE_BRACKET',
 b'UNION_OP',
 b'EQUAL_OP',
 b'REL_OP',
 b'PLUS_OP',
 b'MINUS_OP',
 b'MULT_OP',
 b'STAR_OP',
 b'COMMA',
 b'LITERAL',
 b'FLOAT',
 b'INTEGER',
 b'NCNAME',
 b'NODETYPE',
 b'FUNCNAME',
 b'AXISNAME',
 b'COLON',
 b'DOLLAR'] + list(operator_names.values())
t_PATH_SEP = b'/'
t_ABBREV_PATH_SEP = b'//'
t_ABBREV_STEP_SELF = b'\\.'
t_ABBREV_STEP_PARENT = b'\\.\\.'
t_AXIS_SEP = b'::'
t_ABBREV_AXIS_AT = b'@'
t_OPEN_PAREN = b'\\('
t_CLOSE_PAREN = b'\\)'
t_OPEN_BRACKET = b'\\['
t_CLOSE_BRACKET = b'\\]'
t_UNION_OP = b'\\|'
t_EQUAL_OP = b'!?='
t_REL_OP = b'[<>]=?'
t_PLUS_OP = b'\\+'
t_MINUS_OP = b'-'
t_COMMA = b','
t_COLON = b':'
t_DOLLAR = b'\\$'
t_STAR_OP = b'\\*'
t_ignore = b' \t\r\n'
NameStartChar = b'[A-Z]|_|[a-z]|\\xc0-\\xd6]|[\\xd8-\\xf6]|[\\xf8-˿]|' + b'[Ͱ-ͽ]|[Ϳ-\u1fff]|[\u200c-\u200d]|[⁰-\u218f]|' + b'[Ⰰ-\u2fef]|[、-\ud7ff]|[豈-\ufdcf]|[ﷰ-�]'
Full_NameStartChar = b'(' + NameStartChar + b'|[𐀀-\U000effff]' + b')'
NameChar_extras = b'[-.0-9\\xb7̀-ͯ‿-⁀]'
try:
    import re
    re.compile(b'[𐀀-𐀁]')
    NameStartChar = Full_NameStartChar
except:
    pass

NCNAME_REGEX = b'(' + NameStartChar + b')(' + NameStartChar + b'|' + NameChar_extras + b')*'
NODE_TYPES = set([b'comment', b'text', b'processing-instruction', b'node'])
t_NCNAME = NCNAME_REGEX

def t_LITERAL(t):
    """"[^"]*"|'[^']*'"""
    t.value = t.value[1:-1]
    return t


def t_FLOAT(t):
    r"""\d+\.\d*|\.\d+"""
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_error(t):
    raise TypeError(b"Unknown text '%s'" % (t.value,))