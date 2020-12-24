# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/lexer_parser_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1807 bytes
import os, unittest
from antlr4 import *
from pynestml.generated.PyNestMLLexer import PyNestMLLexer
from pynestml.generated.PyNestMLParser import PyNestMLParser

class LexerParserTest(unittest.TestCase):
    __doc__ = '\n    This test is used to test the parser and lexer for correct functionality.\n    '

    def test(self):
        for filename in os.listdir(os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.join('..', 'models')))):
            if filename.endswith('.nestml'):
                input_file = FileStream(os.path.join(os.path.dirname(__file__), os.path.join(os.path.join('..', 'models'), filename)))
                lexer = PyNestMLLexer(input_file)
                stream = CommonTokenStream(lexer)
                tree = PyNestMLParser(stream)
                self.assertTrue(tree is not None)


if __name__ == '__main__':
    unittest.main()