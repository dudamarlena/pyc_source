# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/model_parser.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 19606 bytes
import copy
from antlr4 import *
from antlr4.error.ErrorStrategy import BailErrorStrategy, DefaultErrorStrategy
from antlr4.error.ErrorListener import ConsoleErrorListener
from pynestml.generated.PyNestMLLexer import PyNestMLLexer
from pynestml.generated.PyNestMLParser import PyNestMLParser
from pynestml.meta_model.ast_arithmetic_operator import ASTArithmeticOperator
from pynestml.meta_model.ast_assignment import ASTAssignment
from pynestml.meta_model.ast_block import ASTBlock
from pynestml.meta_model.ast_block_with_variables import ASTBlockWithVariables
from pynestml.meta_model.ast_body import ASTBody
from pynestml.meta_model.ast_comparison_operator import ASTComparisonOperator
from pynestml.meta_model.ast_compound_stmt import ASTCompoundStmt
from pynestml.meta_model.ast_data_type import ASTDataType
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.meta_model.ast_elif_clause import ASTElifClause
from pynestml.meta_model.ast_else_clause import ASTElseClause
from pynestml.meta_model.ast_equations_block import ASTEquationsBlock
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_for_stmt import ASTForStmt
from pynestml.meta_model.ast_function import ASTFunction
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_if_clause import ASTIfClause
from pynestml.meta_model.ast_if_stmt import ASTIfStmt
from pynestml.meta_model.ast_input_block import ASTInputBlock
from pynestml.meta_model.ast_input_port import ASTInputPort
from pynestml.meta_model.ast_input_qualifier import ASTInputQualifier
from pynestml.meta_model.ast_logical_operator import ASTLogicalOperator
from pynestml.meta_model.ast_nestml_compilation_unit import ASTNestMLCompilationUnit
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.meta_model.ast_ode_equation import ASTOdeEquation
from pynestml.meta_model.ast_ode_function import ASTOdeFunction
from pynestml.meta_model.ast_ode_shape import ASTOdeShape
from pynestml.meta_model.ast_output_block import ASTOutputBlock
from pynestml.meta_model.ast_parameter import ASTParameter
from pynestml.meta_model.ast_return_stmt import ASTReturnStmt
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.meta_model.ast_small_stmt import ASTSmallStmt
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.meta_model.ast_stmt import ASTStmt
from pynestml.meta_model.ast_unary_operator import ASTUnaryOperator
from pynestml.meta_model.ast_unit_type import ASTUnitType
from pynestml.meta_model.ast_update_block import ASTUpdateBlock
from pynestml.meta_model.ast_variable import ASTVariable
from pynestml.meta_model.ast_while_stmt import ASTWhileStmt
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.utils.ast_utils import ASTUtils
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_builder_visitor import ASTBuilderVisitor
from pynestml.visitors.ast_higher_order_visitor import ASTHigherOrderVisitor
from pynestml.visitors.ast_symbol_table_visitor import ASTSymbolTableVisitor
from pynestml.utils.error_listener import NestMLErrorListener

class ModelParser(object):

    @classmethod
    def parse_model(cls, file_path=None):
        """
        Parses a handed over model and returns the meta_model representation of it.
        :param file_path: the path to the file which shall be parsed.
        :type file_path: str
        :return: a new ASTNESTMLCompilationUnit object.
        :rtype: ASTNestMLCompilationUnit
        """
        try:
            input_file = FileStream(file_path)
        except IOError:
            code, message = Messages.get_input_path_not_found(path=file_path)
            Logger.log_message(neuron=None, code=None, message=message, error_position=None, log_level=LoggingLevel.ERROR)
            return

        code, message = Messages.get_start_processing_file(file_path)
        Logger.log_message(neuron=None, code=code, message=message, error_position=None, log_level=LoggingLevel.INFO)
        lexer = PyNestMLLexer()
        lexer.removeErrorListeners()
        lexer.addErrorListener(ConsoleErrorListener())
        lexerErrorListener = NestMLErrorListener()
        lexer.addErrorListener(lexerErrorListener)
        lexer.inputStream = input_file
        stream = CommonTokenStream(lexer)
        stream.fill()
        if lexerErrorListener._error_occurred:
            code, message = Messages.get_lexer_error()
            Logger.log_message(neuron=None, code=None, message=message, error_position=None, log_level=LoggingLevel.ERROR)
            return
        parser = PyNestMLParser(None)
        parser.removeErrorListeners()
        parser.addErrorListener(ConsoleErrorListener())
        parserErrorListener = NestMLErrorListener()
        parser.addErrorListener(parserErrorListener)
        parser.setTokenStream(stream)
        compilation_unit = parser.nestMLCompilationUnit()
        if parserErrorListener._error_occurred:
            code, message = Messages.get_parser_error()
            Logger.log_message(neuron=None, code=None, message=message, error_position=None, log_level=LoggingLevel.ERROR)
            return
        ast_builder_visitor = ASTBuilderVisitor(stream.tokens)
        ast = ast_builder_visitor.visit(compilation_unit)
        SymbolTable.initialize_symbol_table(ast.get_source_position())
        log_to_restore = copy.deepcopy(Logger.get_log())
        counter = Logger.curr_message
        restore_differential_order = []
        for ode in ASTUtils.get_all(ast, ASTOdeEquation):
            lhs_variable = ode.get_lhs()
            if lhs_variable.get_differential_order() > 0:
                lhs_variable.differential_order = lhs_variable.get_differential_order() - 1
                restore_differential_order.append(lhs_variable)

        for shape in ASTUtils.get_all(ast, ASTOdeShape):
            lhs_variable = shape.get_variable()
            if lhs_variable.get_differential_order() > 0:
                lhs_variable.differential_order = lhs_variable.get_differential_order() - 1
                restore_differential_order.append(lhs_variable)

        for variable in ASTUtils.get_all(ast, ASTVariable):
            if variable.get_differential_order() > 0:
                variable.set_name(variable.get_name() + '__' + 'd' * variable.get_differential_order())
                variable.differential_order = 0

        for ode_variable in restore_differential_order:
            ode_variable.differential_order = 1

        Logger.set_log(log_to_restore, counter)
        for neuron in ast.get_neuron_list():
            neuron.accept(ASTSymbolTableVisitor())
            SymbolTable.add_neuron_scope(neuron.get_name(), neuron.get_scope())

        return ast

    @classmethod
    def parse_expression(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.expression())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_declaration(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.declaration())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.stmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_assignment(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.assignment())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_bit_operator(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.bitOperator())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_block(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.block())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_block_with_variables(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.blockWithVariables())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_body(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.body())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_comparison_operator(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.comparisonOperator())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_compound_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.compoundStmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_data_type(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.dataType())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_elif_clause(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.elifClause())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_else_clause(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.elseClause())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_equations_block(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.equationsBlock())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_for_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.forStmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_function(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.function())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_function_call(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.functionCall())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_if_clause(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.ifClause())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_if_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.ifStmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_input_block(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.inputBlock())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_input_port(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.inputPort())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_input_qualifier(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.inputQualifier())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_logic_operator(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.logicalOperator())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_nestml_compilation_unit(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.nestMLCompilationUnit())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_neuron(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.neuron())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_ode_equation(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.odeEquation())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_ode_function(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.odeFunction())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_ode_shape(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.odeShape())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_output_block(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.outputBlock())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_parameter(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.parameter())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_return_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.returnStmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_simple_expression(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.simpleExpression())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_small_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.smallStmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_unary_operator(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.unaryOperator())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_unit_type(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.unitType())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_update_block(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.updateBlock())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_variable(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.variable())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret

    @classmethod
    def parse_while_stmt(cls, string):
        builder, parser = tokenize(string)
        ret = builder.visit(parser.whileStmt())
        ret.accept(ASTHigherOrderVisitor(log_set_added_source_position))
        return ret


def tokenize(string):
    lexer = PyNestMLLexer(InputStream(string))
    stream = CommonTokenStream(lexer)
    stream.fill()
    parser = PyNestMLParser(stream)
    builder = ASTBuilderVisitor(stream.tokens)
    return (builder, parser)


def log_set_added_source_position(node):
    node.set_source_position(ASTSourceLocation.get_added_source_position())