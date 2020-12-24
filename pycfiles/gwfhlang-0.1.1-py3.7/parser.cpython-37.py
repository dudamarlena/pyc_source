# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gwfhlang/parser.py
# Compiled at: 2019-03-25 13:59:09
# Size of source mod 2**32: 581 bytes
from pathlib import Path
from lark import Lark
from lark.indenter import Indenter

class GWFHIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4


def get_parser():
    return Lark.open('grammar.lark', parser='lalr', rel_to=__file__, postlex=(GWFHIndenter()), start='main')


if __name__ == '__main__':
    parser = get_parser()
    code = '\n    name = "batuhan"\n    born = 2003\n    '
    tree = parser.parse(code)