# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/basic_lex.py
# Compiled at: 2019-04-20 06:35:29
# Size of source mod 2**32: 1900 bytes
import ply.lex as lex
from .utils import BasicError
reserved_tuple = ('LET', 'DIM', 'IF', 'THEN', 'ELSE', 'ELSEIF', 'END', 'WHILE', 'DO',
                  'WEND', 'LOOP', 'UNTIL', 'FOR', 'TO', 'STEP', 'NEXT', 'EXIT', 'CONTINUE',
                  'DEFUN', 'SUB', 'FUNCTION', 'RETURN', 'AND', 'OR', 'NOT', 'MOD',
                  'AS', 'USE')
reserved_words = {x:x for x in reserved_tuple}
tokens = ('ID', 'INTEGER', 'DECIMAL', 'STRING', 'EQUALS', 'PLUS', 'MINUS', 'TIMES',
          'DIVIDE', 'EXACTDIV', 'EXP', 'GREATER_THAN', 'LESS_THAN', 'EQUAL_GREATER_THAN',
          'EQUAL_LESS_THAN', 'NOT_EQUAL', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
          'COMMA')
tokens += reserved_tuple
t_ignore = ' \t'
t_EQUALS = '='
t_PLUS = '\\+'
t_MINUS = '-'
t_TIMES = '\\*'
t_DIVIDE = '/'
t_EXACTDIV = '\\\\'
t_EXP = '\\^'
t_GREATER_THAN = '\\>'
t_LESS_THAN = '\\<'
t_EQUAL_GREATER_THAN = '\\>\\='
t_EQUAL_LESS_THAN = '\\<\\='
t_NOT_EQUAL = '\\<\\>'
t_LPAREN = '\\('
t_RPAREN = '\\)'
t_LBRACE = '\\{'
t_RBRACE = '\\}'
t_COMMA = '\\,'

def t_DECIMAL(t):
    r"""[1-9]*[0-9]\.[0-9]*"""
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_STRING(t):
    r"""\"(.*?)\""""
    t.value = t.value[1:-1]
    return t


def t_ID(t):
    r"""[a-zA-Z_\$][a-zA-Z_\$0-9]*"""
    t.value = t.value.upper()
    t.type = reserved_words.get(t.value.upper(), 'ID')
    return t


def t_COMMENT(t):
    r"""\'.*"""
    pass


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise BasicError('Illegal character: "%s"' % t.value[0])


lexer = lex.lex()