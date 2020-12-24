# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/comment_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4108 bytes
import os, unittest
from antlr4 import *
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.generated.PyNestMLLexer import PyNestMLLexer
from pynestml.generated.PyNestMLParser import PyNestMLParser
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.visitors.ast_builder_visitor import ASTBuilderVisitor
PredefinedUnits.register_units()
PredefinedTypes.register_types()
PredefinedFunctions.register_functions()
PredefinedVariables.register_variables()
SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
Logger.init_logger(LoggingLevel.ERROR)

class CommentTest(unittest.TestCase):

    def test(self):
        input_file = FileStream(os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources')), 'CommentTest.nestml'))
        lexer = PyNestMLLexer(input_file)
        stream = CommonTokenStream(lexer)
        stream.fill()
        parser = PyNestMLParser(stream)
        compilation_unit = parser.nestMLCompilationUnit()
        ast_builder_visitor = ASTBuilderVisitor(stream.tokens)
        ast = ast_builder_visitor.visit(compilation_unit)
        neuron_body_elements = ast.get_neuron_list()[0].get_body().get_body_elements()
        assert neuron_body_elements[0].get_comment()[0] == 'init_values comment ok'
        comments = neuron_body_elements[0].get_declarations()[0].get_comment()
        assert comments[0] == 'pre comment 1 ok'
        assert comments[1] == 'pre comment 2 ok'
        assert comments[2] == 'inline comment ok'
        assert comments[3] == 'post comment 1 ok'
        assert comments[4] == 'post comment 2 ok'
        assert 'pre comment not ok' not in comments
        assert 'post comment not ok' not in comments
        self.assertEqual(neuron_body_elements[1].get_comment()[0], 'equations comment ok')
        self.assertEqual(neuron_body_elements[2].get_comment()[0], 'parameters comment ok')
        self.assertEqual(neuron_body_elements[3].get_comment()[0], 'internals comment ok')
        self.assertEqual(neuron_body_elements[4].get_comment()[0], 'input comment ok')
        self.assertEqual(neuron_body_elements[5].get_comment()[0], 'output comment ok')
        self.assertEqual(neuron_body_elements[6].get_comment()[0], 'update comment ok')


if __name__ == '__main__':
    unittest.main()