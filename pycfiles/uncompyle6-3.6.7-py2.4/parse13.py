# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse13.py
# Compiled at: 2018-06-14 22:45:01
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse14 import Python14Parser

class Python13Parser(Python14Parser):
    __module__ = __name__

    def p_misc13(self, args):
        """
        # Nothing here yet, but will need to add LOAD_GLOBALS
        """
        pass

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python13Parser, self).__init__(debug_parser)
        self.customized = {}


class Python13ParserSingle(Python13Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python13Parser()
    p.check_grammar()
    p.dump_grammar()