# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse22.py
# Compiled at: 2018-03-25 15:08:08
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse23 import Python23Parser

class Python22Parser(Python23Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python23Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_misc22(self, args):
        """
        for_iter  ::= LOAD_CONST FOR_LOOP
        list_iter ::= list_if JUMP_FORWARD
                      COME_FROM POP_TOP COME_FROM
        list_for  ::= expr for_iter store list_iter CONTINUE JUMP_FORWARD
                      COME_FROM POP_TOP COME_FROM

        # Some versions of Python 2.2 have been found to generate
        # PRINT_ITEM_CONT for PRINT_ITEM
        print_items_stmt ::= expr PRINT_ITEM_CONT print_items_opt
        """
        pass

    def customize_grammar_rules(self, tokens, customize):
        super(Python22Parser, self).customize_grammar_rules(tokens, customize)
        self.remove_rules('\n        kvlist ::= kvlist kv2\n        ')


class Python22ParserSingle(Python23Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python22Parser()
    p.check_grammar()
    p.dump_grammar()