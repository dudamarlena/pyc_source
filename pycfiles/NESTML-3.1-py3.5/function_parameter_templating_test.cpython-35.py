# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/function_parameter_templating_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2560 bytes
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

class FunctionParameterTemplatingTest(unittest.TestCase):
    __doc__ = '\n    This test is used to test the correct derivation of types when functions use templated type parameters.\n    '

    def test(self):
        Logger.init_logger(LoggingLevel.INFO)
        model = ModelParser.parse_model(os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources', 'FunctionParameterTemplatingTest.nestml'))))
        self.assertEqual(len(Logger.get_all_messages_of_level_and_or_neuron(model.get_neuron_list()[0], LoggingLevel.ERROR)), 7)


if __name__ == '__main__':
    unittest.main()