# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/parsers/parse10.py
# Compiled at: 2019-10-28 13:18:17
from spark_parser import DEFAULT_DEBUG as PARSER_DEFAULT_DEBUG
from uncompyle6.parser import PythonParserSingle
from uncompyle6.parsers.parse11 import Python11Parser

class Python10Parser(Python11Parser):
    __module__ = __name__

    def __init__(self, debug_parser=PARSER_DEFAULT_DEBUG):
        super(Python11Parser, self).__init__(debug_parser)
        self.customized = {}


class Python10ParserSingle(Python10Parser, PythonParserSingle):
    __module__ = __name__


if __name__ == '__main__':
    p = Python10Parser()
    p.check_grammar()
    p.dump_grammar()