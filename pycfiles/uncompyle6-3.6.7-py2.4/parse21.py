# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse21.py
# Compiled at: 2020-02-08 15:24:06
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse22 import Python22Parser

class Python21Parser(Python22Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python22Parser, self).__init__(debug_parser)
        self.customized = {}

    def p_forstmt21(self, args):
        """
        for         ::= SETUP_LOOP expr for_iter store
                        returns
                        POP_BLOCK COME_FROM
        for         ::= SETUP_LOOP expr for_iter store
                        l_stmts_opt _jump_back
                        POP_BLOCK COME_FROM
        """
        pass

    def p_import21(self, args):
        """
        alias ::= IMPORT_NAME_CONT store
        """
        pass


class Python21ParserSingle(Python22Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python21Parser()
    p.check_grammar()
    p.dump_grammar()