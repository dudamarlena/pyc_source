# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/magnitude_compatibility_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2570 bytes
import os, unittest
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.model_parser import ModelParser
from pynestml.visitors.ast_visitor import ASTVisitor
SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
PredefinedUnits.register_units()
PredefinedTypes.register_types()
PredefinedVariables.register_variables()
PredefinedFunctions.register_functions()

class ExpressionTestVisitor(ASTVisitor):

    def end_visit_assignment(self, node):
        pass

    def end_visit_expression(self, node):
        pass


class MagnitudeCompatibilityTest(unittest.TestCase):
    __doc__ = '\n    A simple test that prints all top-level expression types in a file.\n    '

    def test(self):
        Logger.init_logger(LoggingLevel.INFO)
        model = ModelParser.parse_model(os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources', 'MagnitudeCompatibilityTest.nestml'))))
        ExpressionTestVisitor().handle(model)


if __name__ == '__main__':
    unittest.main()