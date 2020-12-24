# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/nestml_printer_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 9257 bytes
import unittest
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.utils.ast_nestml_printer import ASTNestMLPrinter
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.model_parser import ModelParser
PredefinedUnits.register_units()
PredefinedTypes.register_types()
PredefinedFunctions.register_functions()
PredefinedVariables.register_variables()
SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
Logger.init_logger(LoggingLevel.INFO)

class NestMLPrinterTest(unittest.TestCase):
    __doc__ = '\n    Tests if the NestML printer works as intended.\n    '

    def test_block_with_variables_with_comments(self):
        block = '\n/* pre1\n* pre2\n*/\nstate: # in\nend\n/* post1\n* post2\n*/\n\n'
        model = ModelParser.parse_block_with_variables(block)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(block, model_printer.print_node(model))

    def test_block_with_variables_without_comments(self):
        block = 'state:\nend'
        model = ModelParser.parse_block_with_variables(block)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(block, model_printer.print_node(model))

    def test_assignment_with_comments(self):
        assignment = '\n/* pre */\na = b # in\n/* post */\n\n'
        model = ModelParser.parse_assignment(assignment)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(assignment, model_printer.print_node(model))

    def test_assignment_without_comments(self):
        assignment = 'a = b\n'
        model = ModelParser.parse_assignment(assignment)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(assignment, model_printer.print_node(model))

    def test_function_with_comments(self):
        t_function = '\n/*pre func*/\nfunction test(Tau_1 ms) real: # in func\n\n  /* decl pre */\n  exact_integration_adjustment real = ((1 / Tau_2) - (1 / Tau_1)) * ms # decl in\n  /* decl post */\n\n  return normalisation_factor\nend\n/*post func*/\n\n'
        model = ModelParser.parse_function(t_function)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(t_function, model_printer.print_node(model))

    def test_function_without_comments(self):
        t_function = 'function test(Tau_1 ms) real:\n  exact_integration_adjustment real = ((1 / Tau_2) - (1 / Tau_1)) * ms\n  return normalisation_factor\nend\n'
        model = ModelParser.parse_function(t_function)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(t_function, model_printer.print_node(model))

    def test_function_call_with_comments(self):
        function_call = '\n/* pre */\nmin(1,2) # in\n/* post */\n\n'
        model = ModelParser.parse_stmt(function_call)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(function_call, model_printer.print_node(model))

    def test_function_call_without_comments(self):
        function_call = 'min(1,2)\n'
        model = ModelParser.parse_stmt(function_call)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(function_call, model_printer.print_node(model))

    def test_neuron_with_comments(self):
        neuron = '\n/*pre*/\nneuron test: # in\nend\n/*post*/\n\n'
        model = ModelParser.parse_neuron(neuron)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(neuron, model_printer.print_node(model))

    def test_neuron_without_comments(self):
        neuron = 'neuron test:\nend\n'
        model = ModelParser.parse_neuron(neuron)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(neuron, model_printer.print_node(model))

    def test_declaration_with_comments(self):
        declaration = '\n/*pre*/\ntest mV = 10mV # in\n/*post*/\n\n'
        model = ModelParser.parse_declaration(declaration)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(declaration, model_printer.print_node(model))

    def test_declaration_without_comments(self):
        declaration = 'test mV = 10mV\n'
        model = ModelParser.parse_declaration(declaration)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(declaration, model_printer.print_node(model))

    def test_equations_block_with_comments(self):
        block = '\n/*pre*/\nequations: # in\nend\n/*post*/\n\n'
        model = ModelParser.parse_equations_block(block)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(block, model_printer.print_node(model))

    def test_equations_block_without_comments(self):
        block = 'equations:\nend\n'
        model = ModelParser.parse_equations_block(block)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(block, model_printer.print_node(model))

    def test_for_stmt_with_comments(self):
        stmt = '\n/*pre*/\nfor i in 10 - 3.14...10 + 3.14 step -1: # in\nend\n/*post*/\n\n'
        model = ModelParser.parse_for_stmt(stmt)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(stmt, model_printer.print_node(model))

    def test_for_stmt_without_comments(self):
        stmt = 'for i in 10 - 3.14...10 + 3.14 step -1: # in\nend\n'
        model = ModelParser.parse_for_stmt(stmt)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(stmt, model_printer.print_node(model))

    def test_while_stmt_with_comments(self):
        stmt = '\n/*pre*/\nwhile true: # in \nend\n/*post*/\n\n'
        model = ModelParser.parse_while_stmt(stmt)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(stmt, model_printer.print_node(model))

    def test_while_stmt_without_comments(self):
        stmt = 'while true:\nend\n'
        model = ModelParser.parse_while_stmt(stmt)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(stmt, model_printer.print_node(model))

    def test_update_block_with_comments(self):
        block = '\n/*pre*/\nupdate: # in\nend\n/*post*/\n\n'
        model = ModelParser.parse_update_block(block)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(block, model_printer.print_node(model))

    def test_update_block_without_comments(self):
        block = 'update:\nend\n'
        model = ModelParser.parse_update_block(block)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(block, model_printer.print_node(model))

    def test_variable(self):
        var = 'V_m'
        model = ModelParser.parse_variable(var)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(var, model_printer.print_node(model))

    def test_unit_type(self):
        unit = '1/(mV*kg**2)'
        model = ModelParser.parse_unit_type(unit)
        model_printer = ASTNestMLPrinter()
        self.assertEqual(unit, model_printer.print_node(model))

    def test_unary_operator(self):
        ops = {
         '-', '+', '~'}
        for op in ops:
            model = ModelParser.parse_unary_operator(op)
            model_printer = ASTNestMLPrinter()
            self.assertEqual(op, model_printer.print_node(model))