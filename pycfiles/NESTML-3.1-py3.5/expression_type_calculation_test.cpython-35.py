# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/expression_type_calculation_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4104 bytes
import os, unittest
from pynestml.codegeneration.unit_converter import UnitConverter
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import MessageCode
from pynestml.utils.model_parser import ModelParser
from pynestml.visitors.ast_visitor import ASTVisitor
SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
PredefinedUnits.register_units()
PredefinedTypes.register_types()
PredefinedVariables.register_variables()
PredefinedFunctions.register_functions()

class ExpressionTestVisitor(ASTVisitor):

    def endvisit_assignment(self, node):
        scope = node.get_scope()
        var_name = node.get_variable().get_name()
        _expr = node.get_expression()
        var_symbol = scope.resolve_to_symbol(var_name, SymbolKind.VARIABLE)
        _equals = var_symbol.get_type_symbol().equals(_expr.type) or var_symbol.get_type_symbol().differs_only_in_magnitude(_expr.type)
        message = 'line ' + str(_expr.get_source_position()) + ' : LHS = ' + var_symbol.get_type_symbol().get_symbol_name() + ' RHS = ' + _expr.type.get_symbol_name() + ' Equal ? ' + str(_equals)
        if isinstance(_expr.type, UnitTypeSymbol):
            message += ' Neuroscience Factor: ' + str(UnitConverter().get_factor(_expr.type.astropy_unit))
        Logger.log_message(error_position=node.get_source_position(), code=MessageCode.TYPE_MISMATCH, message=message, log_level=LoggingLevel.INFO)
        if _equals is False:
            Logger.log_message(message='Type mismatch in test!', code=MessageCode.TYPE_MISMATCH, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)


class ExpressionTypeCalculationTest(unittest.TestCase):
    __doc__ = '\n    A simple test that prints all top-level expression types in a file.\n    '

    def test(self):
        Logger.init_logger(LoggingLevel.INFO)
        model = ModelParser.parse_model(os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources', 'ExpressionTypeTest.nestml'))))
        Logger.set_current_neuron(model.get_neuron_list()[0])
        model.accept(ExpressionTestVisitor())
        Logger.set_current_neuron(None)
        self.assertEqual(len(Logger.get_all_messages_of_level_and_or_neuron(model.get_neuron_list()[0], LoggingLevel.ERROR)), 2)


if __name__ == '__main__':
    unittest.main()