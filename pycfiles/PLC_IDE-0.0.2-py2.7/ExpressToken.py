# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib\ExpressToken.py
# Compiled at: 2018-09-23 10:29:34
reserved = {}
tokens = [
 'ID',
 'VAL_INTEGER', 'VAL_FLOAT', 'VAL_STRING', 'VAL_CHARACTER',
 'EQUALS',
 'COMMENT',
 'LPAREN', 'RPAREN',
 'LBRACKET', 'RBRACKET',
 'LBRACE', 'RBRACE',
 'COMMA', 'PERIOD', 'SEMI', 'COLON',
 'ELLIPSIS',
 'DOTDOT',
 'ADDRESS']
t_EQUALS = ':='
t_LPAREN = '\\('
t_RPAREN = '\\)'
t_LBRACKET = '\\['
t_RBRACKET = '\\]'
t_LBRACE = '\\{'
t_RBRACE = '\\}'
t_COMMA = ','
t_PERIOD = '\\.'
t_SEMI = ';'
t_COLON = ':'
t_ELLIPSIS = '\\.\\.\\.'
t_VAL_INTEGER = '\\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
t_VAL_FLOAT = '((\\d+)(\\.\\d+)(e(\\+|-)?(\\d+))? | (\\d+)e(\\+|-)?(\\d+))([lL]|[fF])?'
t_VAL_STRING = '\\"([^\\\\\\n]|(\\\\.))*?\\"'
t_VAL_CHARACTER = "(L)?\\'([^\\\\\\n]|(\\\\.))*?\\'"
t_DOTDOT = '\\.\\.'
t_ADDRESS = '%'

def t_ID(t):
    """[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r"""\(\*(.|\n)*?\*\)"""
    t.lexer.lineno += t.value.count('\n')
    return t


def t_CPPCOMMENT(t):
    r"""//.*\n"""
    t.lexer.lineno += 1
    return t


t_ignore = ' \t'

def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


import ply.lex as lex
lexer = lex.lex(debug=False)