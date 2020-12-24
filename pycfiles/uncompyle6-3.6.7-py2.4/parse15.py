# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse15.py
# Compiled at: 2018-06-10 16:49:24
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parser import PythonParserSingle, nop_func
from uncompyle6.parsers.parse21 import Python21Parser

class Python15Parser(Python21Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python15Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_import15(self, args):
        """
        import      ::= filler IMPORT_NAME STORE_FAST
        import      ::= filler IMPORT_NAME STORE_NAME

        import_from ::= filler IMPORT_NAME importlist
        import_from ::= filler filler IMPORT_NAME importlist POP_TOP

        importlist  ::= importlist IMPORT_FROM
        importlist  ::= IMPORT_FROM
        """
        pass

    def customize_grammar_rules(self, tokens, customize):
        super(Python15Parser, self).customize_grammar_rules(tokens, customize)
        for (i, token) in enumerate(tokens):
            opname = token.kind
            opname_base = opname[:opname.rfind('_')]
            if opname_base == 'UNPACK_LIST':
                self.addRule('store ::= unpack_list', nop_func)


class Python15ParserSingle(Python15Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python15Parser()
    p.check_grammar()
    p.dump_grammar()