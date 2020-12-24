# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/lexer.py
# Compiled at: 2012-03-17 10:31:19
import ply.lex as lex, os
tokens = ('integer', 'float', 'identifier', 'string', 'whitespace', 'other')
t_integer = '-?(0([0-7]*|[Xx][0-9A-Fa-f]+)|[1-9][0-9]*)'
t_identifier = '[A-Z_a-z][0-9A-Z_a-z]*'
t_string = '\\"[^\\"]*\\"'
t_whitespace = '[\\t\\n\\r ]+|[\\t\\n\\r ]*((//.*|/\\*.*?\\*/)[\\t\\n\\r ]*)+'

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


lexdir = os.path.dirname(__file__)
lex.lex(lextab='pywidl.lextab', outputdir=lexdir, optimize=1)