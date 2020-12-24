# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lpabon/git/golang/porx/src/github.com/libopenstorage/openstorage-sdk-clients/sdk/python/build/lib/python3.6/site-packages/pycparser/_build_tables.py
# Compiled at: 2018-07-25 08:51:15
# Size of source mod 2**32: 859 bytes
from _ast_gen import ASTCodeGenerator
ast_gen = ASTCodeGenerator('_c_ast.cfg')
ast_gen.generate(open('c_ast.py', 'w'))
import sys
sys.path[0:0] = [
 '.', '..']
from pycparser import c_parser
c_parser.CParser(lex_optimize=True,
  yacc_debug=False,
  yacc_optimize=True)
import lextab, yacctab, c_ast