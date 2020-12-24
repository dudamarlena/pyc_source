# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/canoe/config/lex.py
# Compiled at: 2013-03-20 10:50:18
import ply.lex as lex
reserved_words = {'route': 'ROUTE', 
   'watch': 'WATCH', 
   'filter': 'FILTER'}
tokens = [
 'COMMA',
 'EQUALS',
 'AT',
 'LCURLY',
 'RCURLY',
 'NUMBER',
 'STRING',
 'BOOL',
 'IMPORT_PATH',
 'IDENTIFIER'] + reserved_words.values()
t_AT = '@'
t_EQUALS = '='
t_COMMA = ','
t_LCURLY = '\\{'
t_RCURLY = '\\}'
t_ignore_COMMENT = '\\#.*'

def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_STRING(t):
    """"(\\\\[nrt"\\\\]|[^\\\\\\"])*\""""
    replacements = [
     ('\\n', '\n'),
     ('\\r', '\r'),
     ('\\t', '\t'),
     ('\\"', '"'),
     ('\\\\', '\\')]
    for s, r in replacements:
        t.value = t.value.replace(s, r)

    t.value = t.value[1:-1]
    return t


def t_IMPORT_PATH(t):
    """"[a-zA-Z_][a-zA-Z0-9_](\\.[a-zA-Z_][a-zA-Z0-9_])*\""""
    return t


def t_IDENTIFIER(t):
    """[a-zA-Z_][a-zA-Z0-9_]*"""
    if t.value.lower() == 'true':
        t.type = 'BOOL'
        t.value = True
    elif t.value.lower() == 'false':
        t.type = 'BOOL'
        t.value = False
    else:
        t.type = reserved_words.get(t.value, 'IDENTIFIER')
    return t


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'

def t_error(t):
    print "Illegal character '%s' on line %d, position %d." % (
     t.value[0], t.lexer.lineno, t.lexer.lexpos)
    raise SystemExit()


lexer = lex.lex()