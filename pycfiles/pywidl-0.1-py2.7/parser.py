# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/parser.py
# Compiled at: 2012-03-17 10:29:16
from lexer import tokens
import ply.yacc as yacc, os

def p_Definitions(p):
    """Definitions : identifier whitespace integer whitespace"""
    p[0] = [
     p[1]] + [p[3]]


parsedir = os.path.dirname(__file__)
parser = yacc.yacc(tabmodule='pywidl.parsetab', outputdir=parsedir, debug=1)

def parse(source):
    return parser.parse(source)