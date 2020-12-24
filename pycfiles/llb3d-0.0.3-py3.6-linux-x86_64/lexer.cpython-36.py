# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/lexer.py
# Compiled at: 2018-08-24 05:28:10
# Size of source mod 2**32: 2774 bytes
"""Lexer for Blitz3D language."""
from ply import lex

class LexerGlobals:
    __doc__ = 'Global variables to save with lexer.'

    def __init__(self, code):
        """Initialize self.  See help(type(self)) for accurate signature."""
        self.error_list = []
        self.code = code


literals = '#$%(),.\\=\n+-~^*/<>'
keywords = ('AFTER', 'AND', 'BEFORE', 'CASE', 'CONST', 'DATA', 'DEFAULT', 'DELETE',
            'DIM', 'EACH', 'ELSE', 'ELSEIF', 'END', 'ENDIF', 'EXIT', 'FALSE', 'FIELD',
            'FIRST', 'FLOAT', 'FOR', 'FOREVER', 'FUNCTION', 'GLOBAL', 'GOSUB', 'GOTO',
            'IF', 'INSERT', 'INT', 'LAST', 'LOCAL', 'MOD', 'NEW', 'NEXT', 'NOT',
            'NULL', 'OR', 'PI', 'READ', 'REPEAT', 'RESTORE', 'RETURN', 'SAR', 'SELECT',
            'SHL', 'SHR', 'STEP', 'STR', 'THEN', 'TO', 'TRUE', 'TYPE', 'UNTIL', 'WEND',
            'WHILE', 'XOR', 'INCLUDE')
tokens = ('FLOATLIT', 'INTLIT', 'STRLIT', 'ID') + keywords

def find_column(lexer, lexpos):
    """Find column number for errors."""
    last_cr = lexer.globals.code.rfind('\n', 0, lexpos)
    if last_cr == -1:
        return lexpos + 1
    else:
        return lexpos - last_cr


def position(t):
    """Return symbol position."""
    return '{line}:{col}'.format(line=(t.lineno), col=(find_column(t.lexer, t.lexpos)))


t_ignore = ' \t\r\x0c\x0b'
t_ignore_COMMENT = ';.*'

def t_FLOATLIT(t):
    r"""(?:\d+\.\d*)|(?:\.\d+)"""
    t.value = float(t.value)
    return t


def t_INTLIT(t):
    r"""\d+"""
    t.value = int(t.value, 0)
    return t


def t_STRLIT(t):
    """".*?\""""
    length = len(t.value) - 2
    t.value = t.lexer.globals.code[t.lexpos + 1:t.lexpos + 1 + length]
    return t


def t_ID(t):
    r"""\w+"""
    if t.value.upper() in keywords:
        t.type = t.value.upper()
    return t


def t_newline(t):
    r"""\n"""
    t.lexer.lineno += 1
    t.type = '\n'
    return t


def t_error(t):
    """Error handlings."""
    t.lexer.globals.error_list.append("Illegal character '{char}' at {position}".format(char=(t.value[0]),
      position=(position(t))))
    t.lexer.skip(1)


def init_lexer(code):
    """Init lexer."""
    lexer = lex.lex()
    lexer.lineno = 1
    lexer.globals = LexerGlobals(code)
    lexer.input(code)
    return lexer


def get_lexer(code):
    """Check lex errors and get lexer."""
    lexer = init_lexer(code)
    for _token in lexer:
        pass

    if lexer.globals.error_list != []:
        raise SyntaxError('\n'.join(lexer.globals.error_list))
    lexer = init_lexer(code)
    return lexer