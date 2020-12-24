# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse33.py
# Compiled at: 2020-04-20 22:50:15
"""
spark grammar differences over Python 3.2 for Python 3.3.
"""
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse32 import Python32Parser

class Python33Parser(Python32Parser):
    __module__ = __name__

    def p_33on(self, args):
        """
        # Python 3.3+ adds yield from.
        expr          ::= yield_from
        yield_from    ::= expr expr YIELD_FROM
        """
        pass

    def customize_grammar_rules(self, tokens, customize):
        self.remove_rules('\n        # 3.3+ adds POP_BLOCKS\n        whileTruestmt ::= SETUP_LOOP l_stmts_opt JUMP_BACK NOP COME_FROM_LOOP\n        whileTruestmt ::= SETUP_LOOP l_stmts_opt JUMP_BACK POP_BLOCK NOP COME_FROM_LOOP\n        ')
        super(Python33Parser, self).customize_grammar_rules(tokens, customize)


class Python33ParserSingle(Python33Parser, PythonParserSingle):
    __module__ = __name__