# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/random_number_generators_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2115 bytes
from __future__ import print_function
import os, unittest
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.model_parser import ModelParser

class RandomNumberGeneratorsTest(unittest.TestCase):

    def setUp(self):
        Logger.init_logger(LoggingLevel.INFO)
        SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
        PredefinedUnits.register_units()
        PredefinedTypes.register_types()
        PredefinedVariables.register_variables()
        PredefinedFunctions.register_functions()

    def test_invalid_element_defined_after_usage(self):
        model = ModelParser.parse_model(os.path.join(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources')), 'random_number_generators_test.nestml'))
        self.assertEqual(len(Logger.get_all_messages_of_level_and_or_neuron(model.get_neuron_list()[0], LoggingLevel.ERROR)), 0)