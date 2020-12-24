# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/symbol_table_resolution_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3010 bytes
import os, unittest
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.symbol_table.scope import ScopeType
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.model_parser import ModelParser
Logger.init_logger(LoggingLevel.INFO)
SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
PredefinedUnits.register_units()
PredefinedTypes.register_types()
PredefinedVariables.register_variables()
PredefinedFunctions.register_functions()

class SymbolTableResolutionTest(unittest.TestCase):
    __doc__ = '\n    This test is used to check if the resolution of symbols works as expected.\n    '

    def test(self):
        model = ModelParser.parse_model(os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources', 'ResolutionTest.nestml'))))
        scope = model.get_neuron_list()[0].get_scope()
        res1 = scope.resolve_to_all_scopes('test1', SymbolKind.VARIABLE)
        self.assertTrue(res1 is not None)
        res2 = scope.resolve_to_all_scopes('testNot', SymbolKind.VARIABLE)
        self.assertTrue(res2 is None)
        res3 = scope.resolve_to_all_scopes('test2', SymbolKind.VARIABLE)
        self.assertTrue(res3 is None)
        res4 = scope.resolve_to_all_scopes('arg1', SymbolKind.VARIABLE)
        self.assertTrue(res4 is None)
        res5 = scope.resolve_to_all_scopes('test3', SymbolKind.VARIABLE)
        self.assertTrue(res5 is None)
        res6 = scope.resolve_to_all_scopes('test1', SymbolKind.FUNCTION)
        self.assertTrue(res6 is not None and res6.get_scope_type() == ScopeType.GLOBAL)
        res7 = scope.resolve_to_all_scopes('test6', SymbolKind.VARIABLE)
        self.assertTrue(res7 is not None and res7.get_scope_type() == ScopeType.UPDATE)


if __name__ == '__main__':
    unittest.main()