# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_node_factory.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 20546 bytes
from typing import Union
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.meta_model.ast_arithmetic_operator import ASTArithmeticOperator
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.meta_model.ast_variable import ASTVariable
from pynestml.meta_model.ast_assignment import ASTAssignment
from pynestml.meta_model.ast_bit_operator import ASTBitOperator
from pynestml.meta_model.ast_small_stmt import ASTSmallStmt
from pynestml.meta_model.ast_compound_stmt import ASTCompoundStmt
from pynestml.meta_model.ast_block import ASTBlock
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.meta_model.ast_block_with_variables import ASTBlockWithVariables
from pynestml.meta_model.ast_body import ASTBody
from pynestml.meta_model.ast_comparison_operator import ASTComparisonOperator
from pynestml.meta_model.ast_if_stmt import ASTIfStmt
from pynestml.meta_model.ast_while_stmt import ASTWhileStmt
from pynestml.meta_model.ast_for_stmt import ASTForStmt
from pynestml.meta_model.ast_unit_type import ASTUnitType
from pynestml.meta_model.ast_data_type import ASTDataType
from pynestml.meta_model.ast_elif_clause import ASTElifClause
from pynestml.meta_model.ast_else_clause import ASTElseClause
from pynestml.meta_model.ast_equations_block import ASTEquationsBlock
from pynestml.meta_model.ast_unary_operator import ASTUnaryOperator
from pynestml.meta_model.ast_logical_operator import ASTLogicalOperator
from pynestml.meta_model.ast_parameter import ASTParameter
from pynestml.meta_model.ast_function import ASTFunction
from pynestml.meta_model.ast_function_call import ASTFunctionCall
from pynestml.meta_model.ast_if_clause import ASTIfClause
from pynestml.meta_model.ast_input_block import ASTInputBlock
from pynestml.meta_model.ast_input_port import ASTInputPort
from pynestml.meta_model.ast_input_qualifier import ASTInputQualifier
from pynestml.meta_model.ast_signal_type import ASTSignalType
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.meta_model.ast_nestml_compilation_unit import ASTNestMLCompilationUnit
from pynestml.meta_model.ast_ode_equation import ASTOdeEquation
from pynestml.meta_model.ast_ode_function import ASTOdeFunction
from pynestml.meta_model.ast_ode_shape import ASTOdeShape
from pynestml.meta_model.ast_output_block import ASTOutputBlock
from pynestml.meta_model.ast_return_stmt import ASTReturnStmt
from pynestml.meta_model.ast_update_block import ASTUpdateBlock
from pynestml.meta_model.ast_stmt import ASTStmt

class ASTNodeFactory(object):
    __doc__ = '\n    An implementation of the factory pattern for an easier initialization of new AST nodes.\n    '

    @classmethod
    def create_ast_arithmetic_operator(cls, is_times_op=False, is_div_op=False, is_modulo_op=False, is_plus_op=False, is_minus_op=False, is_pow_op=False, source_position=None):
        return ASTArithmeticOperator(is_times_op, is_div_op, is_modulo_op, is_plus_op, is_minus_op, is_pow_op, source_position)

    @classmethod
    def create_ast_assignment(cls, lhs=None, is_direct_assignment=False, is_compound_sum=False, is_compound_minus=False, is_compound_product=False, is_compound_quotient=False, expression=None, source_position=None):
        return ASTAssignment(lhs, is_direct_assignment, is_compound_sum, is_compound_minus, is_compound_product, is_compound_quotient, expression, source_position)

    @classmethod
    def create_ast_bit_operator(cls, is_bit_and=False, is_bit_xor=False, is_bit_or=False, is_bit_shift_left=False, is_bit_shift_right=False, source_position=None):
        return ASTBitOperator(is_bit_and, is_bit_xor, is_bit_or, is_bit_shift_left, is_bit_shift_right, source_position)

    @classmethod
    def create_ast_block(cls, stmts, source_position):
        return ASTBlock(stmts, source_position)

    @classmethod
    def create_ast_block_with_variables(cls, is_state=False, is_parameters=False, is_internals=False, is_initial_values=False, declarations=list(), source_position=None):
        return ASTBlockWithVariables(is_state, is_parameters, is_internals, is_initial_values, declarations, source_position)

    @classmethod
    def create_ast_body(cls, body_elements, source_position):
        return ASTBody(body_elements, source_position)

    @classmethod
    def create_ast_comparison_operator(cls, is_lt=False, is_le=False, is_eq=False, is_ne=False, is_ne2=False, is_ge=False, is_gt=False, source_position=None):
        return ASTComparisonOperator(is_lt, is_le, is_eq, is_ne, is_ne2, is_ge, is_gt, source_position)

    @classmethod
    def create_ast_compound_stmt(cls, if_stmt, while_stmt, for_stmt, source_position):
        return ASTCompoundStmt(if_stmt, while_stmt, for_stmt, source_position)

    @classmethod
    def create_ast_data_type(cls, is_integer=False, is_real=False, is_string=False, is_boolean=False, is_void=False, is_unit_type=None, source_position=None):
        return ASTDataType(is_integer, is_real, is_string, is_boolean, is_void, is_unit_type, source_position)

    @classmethod
    def create_ast_declaration(cls, is_recordable=False, is_function=False, variables=list(), data_type=None, size_parameter=None, expression=None, invariant=None, source_position=None):
        return ASTDeclaration(is_recordable, is_function, variables, data_type, size_parameter, expression, invariant, source_position)

    @classmethod
    def create_ast_elif_clause(cls, condition, block, source_position=None):
        return ASTElifClause(condition, block, source_position)

    @classmethod
    def create_ast_else_clause(cls, block, source_position):
        return ASTElseClause(block, source_position)

    @classmethod
    def create_ast_equations_block(cls, declarations=None, source_position=None):
        return ASTEquationsBlock(declarations, source_position)

    @classmethod
    def create_ast_expression(cls, is_encapsulated=False, unary_operator=None, is_logical_not=False, expression=None, source_position=None):
        """
        The factory method used to create rhs which are either encapsulated in parentheses (e.g., (10mV))
        OR have a unary (e.g., ~bitVar), OR are negated (e.g., not logVar), or are simple rhs (e.g., 10mV).
        """
        return ASTExpression(is_encapsulated=is_encapsulated, unary_operator=unary_operator, is_logical_not=is_logical_not, expression=expression, source_position=source_position)

    @classmethod
    def create_ast_compound_expression(cls, lhs, binary_operator, rhs, source_position):
        """
        The factory method used to create compound expressions, e.g. 10mV + V_m.
        """
        assert binary_operator is not None and (isinstance(binary_operator, ASTBitOperator) or isinstance(binary_operator, ASTComparisonOperator) or isinstance(binary_operator, ASTLogicalOperator) or isinstance(binary_operator, ASTArithmeticOperator)), '(PyNestML.AST.Expression) No or wrong type of binary operator provided (%s)!' % type(binary_operator)
        return ASTExpression(lhs=lhs, binary_operator=binary_operator, rhs=rhs, source_position=source_position)

    @classmethod
    def create_ast_ternary_expression(cls, condition, if_true, if_not, source_position):
        """
        The factory method used to create a ternary operator rhs, e.g., 10mV<V_m?10mV:V_m
        """
        return ASTExpression(condition=condition, if_true=if_true, if_not=if_not, source_position=source_position)

    @classmethod
    def create_ast_for_stmt(cls, variable, start_from, end_at, step=0, block=None, source_position=None):
        return ASTForStmt(variable, start_from, end_at, step, block, source_position)

    @classmethod
    def create_ast_function(cls, name, parameters, return_type, block, source_position):
        return ASTFunction(name, parameters, return_type, block, source_position)

    @classmethod
    def create_ast_function_call(cls, callee_name, args, source_position):
        return ASTFunctionCall(callee_name, args, source_position)

    @classmethod
    def create_ast_if_clause(cls, condition, block, source_position):
        return ASTIfClause(condition, block, source_position)

    @classmethod
    def create_ast_if_stmt(cls, if_clause, elif_clauses, else_clause, source_position):
        return ASTIfStmt(if_clause, elif_clauses, else_clause, source_position)

    @classmethod
    def create_ast_input_block(cls, input_definitions, source_position):
        return ASTInputBlock(input_definitions, source_position)

    @classmethod
    def create_ast_input_port(cls, name, size_parameter, data_type, input_qualifiers, signal_type, source_position):
        return ASTInputPort(name=name, size_parameter=size_parameter, data_type=data_type, input_qualifiers=input_qualifiers, signal_type=signal_type, source_position=source_position)

    @classmethod
    def create_ast_input_qualifier(cls, is_inhibitory=False, is_excitatory=False, source_position=None):
        return ASTInputQualifier(is_inhibitory, is_excitatory, source_position)

    @classmethod
    def create_ast_logical_operator(cls, is_logical_and=False, is_logical_or=False, source_position=None):
        return ASTLogicalOperator(is_logical_and, is_logical_or, source_position)

    @classmethod
    def create_ast_nestml_compilation_unit(cls, list_of_neurons, source_position, artifact_name):
        instance = ASTNestMLCompilationUnit(source_position, artifact_name)
        for i in list_of_neurons:
            instance.add_neuron(i)

        return instance

    @classmethod
    def create_ast_neuron(cls, name, body, source_position, artifact_name):
        return ASTNeuron(name, body, source_position, artifact_name)

    @classmethod
    def create_ast_ode_equation(cls, lhs, rhs, source_position):
        return ASTOdeEquation(lhs, rhs, source_position)

    @classmethod
    def create_ast_ode_function(cls, variable_name, data_type, expression, source_position, is_recordable=False):
        return ASTOdeFunction(variable_name=variable_name, data_type=data_type, expression=expression, source_position=source_position, is_recordable=is_recordable)

    @classmethod
    def create_ast_ode_shape(cls, lhs=None, rhs=None, source_position=None):
        return ASTOdeShape(lhs, rhs, source_position)

    @classmethod
    def create_ast_output_block(cls, s_type, source_position):
        return ASTOutputBlock(s_type, source_position)

    @classmethod
    def create_ast_parameter(cls, name, data_type, source_position):
        return ASTParameter(name=name, data_type=data_type, source_position=source_position)

    @classmethod
    def create_ast_return_stmt(cls, expression=None, source_position=None):
        return ASTReturnStmt(expression, source_position)

    @classmethod
    def create_ast_simple_expression(cls, function_call=None, boolean_literal=None, numeric_literal=None, is_inf=False, variable=None, string=None, source_position=None):
        return ASTSimpleExpression(function_call, boolean_literal, numeric_literal, is_inf, variable, string, source_position)

    @classmethod
    def create_ast_small_stmt(cls, assignment=None, function_call=None, declaration=None, return_stmt=None, source_position=None):
        return ASTSmallStmt(assignment, function_call, declaration, return_stmt, source_position)

    @classmethod
    def create_ast_unary_operator(cls, is_unary_plus=False, is_unary_minus=False, is_unary_tilde=False, source_position=None):
        return ASTUnaryOperator(is_unary_plus, is_unary_minus, is_unary_tilde, source_position)

    @classmethod
    def create_ast_unit_type(cls, is_encapsulated=False, compound_unit=None, base=None, is_pow=False, exponent=None, lhs=None, rhs=None, is_div=False, is_times=False, unit=None, source_position=None):
        return ASTUnitType(is_encapsulated, compound_unit, base, is_pow, exponent, lhs, rhs, is_div, is_times, unit, source_position)

    @classmethod
    def create_ast_update_block(cls, block, source_position):
        return ASTUpdateBlock(block, source_position)

    @classmethod
    def create_ast_variable(cls, name, differential_order=0, source_position=None):
        return ASTVariable(name, differential_order, source_position)

    @classmethod
    def create_ast_while_stmt(cls, condition, block, source_position):
        return ASTWhileStmt(condition, block, source_position)

    @classmethod
    def create_ast_stmt(cls, small_stmt=None, compound_stmt=None, source_position=None):
        return ASTStmt(small_stmt, compound_stmt, source_position)