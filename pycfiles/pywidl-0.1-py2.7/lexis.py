# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/lexis.py
# Compiled at: 2012-03-31 09:47:31
import ply.lex as lex, os, sys
literals = '{};:,=()[].<>?'
tokens = [
 'INTEGER',
 'FLOAT',
 'IDENTIFIER',
 'STRING',
 'ELLIPSIS']
keywords = ('Date', 'DOMString', 'any', 'attribute', 'boolean', 'byte', 'callback',
            'const', 'creator', 'deleter', 'dictionary', 'double', 'enum', 'exception',
            'false', 'float', 'getter', 'implements', 'inherit', 'interface', 'legacycaller',
            'long', 'null', 'object', 'octet', 'optional', 'or', 'partial', 'readonly',
            'sequence', 'setter', 'short', 'static', 'stringifier', 'true', 'typedef',
            'unsigned', 'void')
tokens.extend(keywords)
t_ignore = ' \t'
t_ignore_line_comment = '//.*'
t_INTEGER = '-?(0([0-7]*|[Xx][0-9A-Fa-f]+)|[1-9][0-9]*)'
t_FLOAT = '-?(([0-9]+\\.[0-9]*|[0-9]*\\.[0-9]+)([Ee][+-]?[0-9]+)?|[0-9]+[Ee][+-]?[0-9]+)'
t_ELLIPSIS = '\\.\\.\\.'

def t_IDENTIFIER(t):
    """[A-Z_a-z][0-9A-Z_a-z]*"""
    if t.value in keywords:
        t.type = t.value
    return t


def t_STRING(t):
    r"""\"[^\"]*\""""
    t.value = t.value[1:-1]
    return t


def t_ignore_block_comment(t):
    r"""\/\*[^*]*\*+([^/*][^*]*\*+)*\/"""
    t.lexer.lineno += t.value.count('\n')


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    print >> sys.stderr, "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


lexdir = os.path.dirname(__file__)
lex.lex(lextab='pywidl.lextab', outputdir=lexdir, optimize=0)