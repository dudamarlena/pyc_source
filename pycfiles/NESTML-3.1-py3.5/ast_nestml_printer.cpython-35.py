# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/ast_nestml_printer.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 28261 bytes
from pynestml.meta_model.ast_arithmetic_operator import ASTArithmeticOperator
from pynestml.meta_model.ast_assignment import ASTAssignment
from pynestml.meta_model.ast_bit_operator import ASTBitOperator
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
from pynestml.meta_model.ast_stmt import ASTStmt
from pynestml.meta_model.ast_unary_operator import ASTUnaryOperator
from pynestml.meta_model.ast_unit_type import ASTUnitType
from pynestml.meta_model.ast_update_block import ASTUpdateBlock
from pynestml.meta_model.ast_variable import ASTVariable
from pynestml.meta_model.ast_while_stmt import ASTWhileStmt

class ASTNestMLPrinter(object):
    __doc__ = '\n    This class can be used to print any ast node to a human readable and NestML conform syntax. The entry point is\n    the print_node() operation.\n    '
    tab_size = 2

    def __init__(self):
        self.indent = 0

    def print_node(self, node):
        ret = ''
        if isinstance(node, ASTArithmeticOperator):
            ret = self.print_arithmetic_operator(node)
        if isinstance(node, ASTAssignment):
            ret = self.print_assignment(node)
        if isinstance(node, ASTBitOperator):
            ret = self.print_bit_operator(node)
        if isinstance(node, ASTBlock):
            ret = self.print_block(node)
        if isinstance(node, ASTBlockWithVariables):
            ret = self.print_block_with_variables(node)
        if isinstance(node, ASTBody):
            ret = self.print_body(node)
        if isinstance(node, ASTComparisonOperator):
            ret = self.print_comparison_operator(node)
        if isinstance(node, ASTCompoundStmt):
            ret = self.print_compound_stmt(node)
        if isinstance(node, ASTDataType):
            ret = self.print_data_type(node)
        if isinstance(node, ASTDeclaration):
            ret = self.print_declaration(node)
        if isinstance(node, ASTElifClause):
            ret = self.print_elif_clause(node)
        if isinstance(node, ASTElseClause):
            ret = self.print_else_clause(node)
        if isinstance(node, ASTEquationsBlock):
            ret = self.print_equations_block(node)
        if isinstance(node, ASTExpression):
            ret = self.print_expression(node)
        if isinstance(node, ASTForStmt):
            ret = self.print_for_stmt(node)
        if isinstance(node, ASTFunction):
            ret = self.print_function(node)
        if isinstance(node, ASTFunctionCall):
            ret = self.print_function_call(node)
        if isinstance(node, ASTIfClause):
            ret = self.print_if_clause(node)
        if isinstance(node, ASTIfStmt):
            ret = self.print_if_stmt(node)
        if isinstance(node, ASTInputBlock):
            ret = self.print_input_block(node)
        if isinstance(node, ASTInputPort):
            ret = self.print_input_port(node)
        if isinstance(node, ASTInputQualifier):
            ret = self.print_input_qualifier(node)
        if isinstance(node, ASTLogicalOperator):
            ret = self.print_logical_operator(node)
        if isinstance(node, ASTNestMLCompilationUnit):
            ret = self.print_compilation_unit(node)
        if isinstance(node, ASTNeuron):
            ret = self.print_neuron(node)
        if isinstance(node, ASTOdeEquation):
            ret = self.print_ode_equation(node)
        if isinstance(node, ASTOdeFunction):
            ret = self.print_ode_function(node)
        if isinstance(node, ASTOdeShape):
            ret = self.print_ode_shape(node)
        if isinstance(node, ASTOutputBlock):
            ret = self.print_output_block(node)
        if isinstance(node, ASTParameter):
            ret = self.print_parameter(node)
        if isinstance(node, ASTReturnStmt):
            ret = self.print_return_stmt(node)
        if isinstance(node, ASTSimpleExpression):
            ret = self.print_simple_expression(node)
        if isinstance(node, ASTSmallStmt):
            ret = self.print_small_stmt(node)
        if isinstance(node, ASTUnaryOperator):
            ret = self.print_unary_operator(node)
        if isinstance(node, ASTUnitType):
            ret = self.print_unit_type(node)
        if isinstance(node, ASTUpdateBlock):
            ret = self.print_update_block(node)
        if isinstance(node, ASTVariable):
            ret = self.print_variable(node)
        if isinstance(node, ASTWhileStmt):
            ret = self.print_while_stmt(node)
        if isinstance(node, ASTStmt):
            ret = self.print_stmt(node)
        ret = filter_subsequent_whitespaces(ret)
        return ret

    def print_neuron(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        self.inc_indent()
        ret += 'neuron ' + node.get_name() + ':' + print_sl_comment(node.in_comment)
        ret += '\n' + self.print_node(node.get_body()) + 'end' + '\n'
        self.dec_indent()
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    @classmethod
    def print_arithmetic_operator(cls, node):
        if node.is_times_op:
            return ' * '
        if node.is_div_op:
            return ' / '
        if node.is_modulo_op:
            return ' % '
        if node.is_plus_op:
            return ' + '
        if node.is_minus_op:
            return ' - '
        if node.is_pow_op:
            return ' ** '
        raise RuntimeError('(PyNestML.ArithmeticOperator.Print) Arithmetic operator not specified.')

    def print_assignment(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent) + self.print_node(node.lhs) + ' '
        if node.is_compound_quotient:
            ret += '/='
        else:
            if node.is_compound_product:
                ret += '*='
            else:
                if node.is_compound_minus:
                    ret += '-='
                else:
                    if node.is_compound_sum:
                        ret += '+='
                    else:
                        ret += '='
        ret += ' ' + self.print_node(node.rhs) + print_sl_comment(node.in_comment) + '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    @classmethod
    def print_bit_operator(cls, node):
        if node.is_bit_and:
            return ' & '
        if node.is_bit_or:
            return ' ^ '
        if node.is_bit_or:
            return ' | '
        if node.is_bit_shift_left:
            return ' << '
        if node.is_bit_shift_right:
            return ' >> '
        raise RuntimeError('(PyNestML.BitOperator.Print) Type of bit operator not specified!')

    def print_block(self, node):
        ret = ''
        self.inc_indent()
        for stmt in node.stmts:
            ret += self.print_node(stmt)

        self.dec_indent()
        return ret

    def print_block_with_variables(self, node):
        temp_indent = self.indent
        self.inc_indent()
        ret = print_ml_comments(node.pre_comments, temp_indent, False)
        ret += print_n_spaces(temp_indent)
        if node.is_state:
            ret += 'state'
        else:
            if node.is_parameters:
                ret += 'parameters'
            else:
                if node.is_internals:
                    ret += 'internals'
                else:
                    ret += 'initial_values'
        ret += ':' + print_sl_comment(node.in_comment) + '\n'
        if node.get_declarations() is not None:
            for decl in node.get_declarations():
                ret += self.print_node(decl)

        ret += print_n_spaces(temp_indent) + 'end' + ('\n' if len(node.post_comments) else '')
        ret += print_ml_comments(node.post_comments, temp_indent, True)
        self.dec_indent()
        return ret

    def print_body(self, node):
        ret = ''
        for elem in node.bodyElements:
            ret += self.print_node(elem)
            ret += '\n'

        return ret

    @classmethod
    def print_comparison_operator(cls, node):
        if node.is_lt:
            return ' < '
        if node.is_le:
            return ' <= '
        if node.is_eq:
            return ' == '
        if node.is_ne:
            return ' != '
        if node.is_ne2:
            return ' <> '
        if node.is_ge:
            return ' >= '
        if node.is_gt:
            return ' > '
        raise RuntimeError('(PyNestML.ComparisonOperator.Print) Type of comparison operator not specified!')

    def print_compound_stmt(self, node):
        if node.is_if_stmt():
            return self.print_node(node.get_if_stmt())
        if node.is_for_stmt():
            return self.print_node(node.get_for_stmt())
        if node.is_while_stmt():
            return self.print_node(node.get_while_stmt())
        raise RuntimeError('(PyNestML.CompoundStmt.Print) Type of compound statement not specified!')

    def print_data_type(self, node):
        if node.is_void:
            return 'void'
        if node.is_string:
            return 'string'
        if node.is_boolean:
            return 'boolean'
        if node.is_integer:
            return 'integer'
        if node.is_real:
            return 'real'
        if node.is_unit_type():
            return self.print_node(node.get_unit_type())
        raise RuntimeError('Type of datatype not specified!')

    def print_declaration(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent)
        if node.is_recordable:
            ret += 'recordable '
        if node.is_function:
            ret += 'function '
        for var in node.get_variables():
            ret += self.print_node(var)
            if node.get_variables().index(var) < len(node.get_variables()) - 1:
                ret += ','

        ret += ' ' + self.print_node(node.get_data_type()) + ' '
        if node.has_size_parameter():
            ret += '[' + node.get_size_parameter() + '] '
        if node.has_expression():
            ret += '= ' + self.print_node(node.get_expression())
        if node.has_invariant():
            ret += ' [[' + self.print_node(node.get_invariant()) + ']]'
        ret += print_sl_comment(node.in_comment) + '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_elif_clause(self, node):
        return print_n_spaces(self.indent) + 'elif ' + self.print_node(node.get_condition()) + ':\n' + self.print_node(node.get_block())

    def print_else_clause(self, node):
        return print_n_spaces(self.indent) + 'else:\n' + self.print_node(node.get_block())

    def print_equations_block(self, node):
        temp_indent = self.indent
        self.inc_indent()
        ret = print_ml_comments(node.pre_comments, temp_indent, False)
        ret += print_n_spaces(temp_indent)
        ret += 'equations:' + print_sl_comment(node.in_comment) + '\n'
        for decl in node.get_declarations():
            ret += self.print_node(decl)

        self.dec_indent()
        ret += print_n_spaces(temp_indent) + 'end' + '\n'
        ret += print_ml_comments(node.post_comments, temp_indent, True)
        return ret

    def print_expression(self, node):
        ret = ''
        if node.is_expression():
            if node.is_encapsulated:
                ret += '('
            if node.is_logical_not:
                ret += 'not '
            if node.is_unary_operator():
                ret += self.print_node(node.get_unary_operator())
            ret += self.print_node(node.get_expression())
            if node.is_encapsulated:
                ret += ')'
        else:
            if node.is_compound_expression():
                ret += self.print_node(node.get_lhs())
                ret += self.print_node(node.get_binary_operator())
                ret += self.print_node(node.get_rhs())
            elif node.is_ternary_operator():
                ret += self.print_node(node.get_condition()) + '?' + self.print_node(node.get_if_true()) + ':' + self.print_node(node.get_if_not())
        return ret

    def print_for_stmt(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += 'for ' + node.get_variable() + ' in ' + self.print_node(node.get_start_from()) + '...' + self.print_node(node.get_end_at()) + ' step ' + str(node.get_step()) + ':' + print_sl_comment(node.in_comment) + '\n'
        ret += self.print_node(node.get_block()) + 'end\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_function(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent)
        ret += 'function ' + node.get_name() + '('
        if node.has_parameters():
            for par in node.get_parameters():
                ret += self.print_node(par)

        ret += ')'
        if node.has_return_type():
            ret += ' ' + self.print_node(node.get_return_type())
        ret += ':' + print_sl_comment(node.in_comment) + '\n'
        ret += self.print_node(node.get_block()) + '\nend\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_function_call(self, node):
        ret = str(node.get_name()) + '('
        for i in range(0, len(node.get_args())):
            ret += self.print_node(node.get_args()[i])
            if i < len(node.get_args()) - 1:
                ret += ','

        ret += ')'
        return ret

    def print_if_clause(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent)
        ret += print_n_spaces(self.indent) + 'if ' + self.print_node(node.get_condition()) + ':'
        ret += print_sl_comment(node.in_comment) + '\n'
        ret += self.print_node(node.get_block())
        ret += print_ml_comments(node.post_comments, self.indent)
        return ret

    def print_if_stmt(self, node):
        ret = self.print_node(node.get_if_clause())
        if node.get_elif_clauses() is not None:
            for clause in node.get_elif_clauses():
                ret += self.print_node(clause)

        if node.get_else_clause() is not None:
            ret += self.print_node(node.get_else_clause())
        ret += print_n_spaces(self.indent) + 'end\n'
        return ret

    def print_input_block(self, node):
        temp_indent = self.indent
        self.inc_indent()
        ret = print_ml_comments(node.pre_comments, temp_indent, False)
        ret += print_n_spaces(temp_indent) + 'input:\n'
        if node.get_input_ports() is not None:
            for inputDef in node.get_input_ports():
                ret += self.print_node(inputDef)

        ret += print_n_spaces(temp_indent) + 'end\n'
        ret += print_ml_comments(node.post_comments, temp_indent, True)
        self.dec_indent()
        return ret

    def print_input_port(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent) + node.get_name()
        if node.has_datatype():
            ret += ' ' + self.print_node(node.get_datatype()) + ' '
        if node.has_index_parameter():
            ret += '[' + node.get_index_parameter() + ']'
        ret += '<-'
        if node.has_input_qualifiers():
            for qual in node.get_input_qualifiers():
                ret += self.print_node(qual) + ' '

        if node.is_spike():
            ret += 'spike'
        else:
            ret += 'current'
        ret += print_sl_comment(node.in_comment) + '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    @classmethod
    def print_input_qualifier(cls, node):
        if node.is_inhibitory:
            return 'inhibitory'
        else:
            return 'excitatory'

    @classmethod
    def print_logical_operator(cls, node):
        if node.is_logical_and:
            return ' and '
        else:
            return ' or '

    def print_compilation_unit(self, node):
        ret = ''
        if node.get_neuron_list() is not None:
            for neuron in node.get_neuron_list():
                ret += self.print_node(neuron) + '\n'

        return ret

    def print_ode_equation(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent) + self.print_node(node.get_lhs()) + '=' + self.print_node(node.get_rhs()) + print_sl_comment(node.in_comment) + '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_ode_function(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        if node.is_recordable:
            ret += 'recordable'
        ret += print_n_spaces(self.indent) + 'function ' + str(node.get_variable_name()) + ' ' + self.print_node(node.get_data_type()) + ' = ' + self.print_node(node.get_expression()) + print_sl_comment(node.in_comment) + '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_ode_shape(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent)
        ret += 'shape ' + self.print_node(node.get_variable()) + ' = ' + self.print_node(node.get_expression())
        ret += print_sl_comment(node.in_comment) + '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_output_block(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent) + 'output: ' + ('spike' if node.is_spike() else 'current')
        ret += print_sl_comment(node.in_comment)
        ret += '\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    def print_parameter(self, node):
        return node.get_name() + ' ' + self.print_node(node.get_data_type())

    def print_return_stmt(self, node):
        ret = print_n_spaces(self.indent)
        ret += 'return ' + (self.print_node(node.get_expression()) if node.has_expression() else '')
        return ret

    def print_simple_expression(self, node):
        if node.is_function_call():
            return self.print_node(node.function_call)
        if node.is_boolean_true:
            return 'true'
        if node.is_boolean_false:
            return 'false'
        if node.is_inf_literal:
            return 'inf'
        if node.is_numeric_literal():
            if node.variable is not None:
                return str(node.numeric_literal) + self.print_node(node.variable)
            else:
                return str(node.numeric_literal)
        else:
            if node.is_variable():
                return self.print_node(node.variable)
            if node.is_string():
                return node.get_string()
            raise RuntimeError('Simple rhs at %s not specified!' % str(node.get_source_position()))

    def print_small_stmt(self, node):
        if node.is_assignment():
            ret = self.print_node(node.get_assignment())
        else:
            if node.is_function_call():
                ret = print_ml_comments(node.pre_comments, self.indent, False)
                ret += print_n_spaces(self.indent) + self.print_node(node.get_function_call())
                ret += print_sl_comment(node.in_comment) + '\n'
                ret += print_ml_comments(node.post_comments, self.indent, True)
            else:
                if node.is_declaration():
                    ret = self.print_node(node.get_declaration())
                else:
                    ret = self.print_node(node.get_return_stmt())
        return ret

    def print_stmt(self, node):
        if node.is_small_stmt():
            return self.print_node(node.small_stmt)
        else:
            return self.print_node(node.compound_stmt)

    @classmethod
    def print_unary_operator(cls, node):
        if node.is_unary_plus:
            return '+'
        if node.is_unary_minus:
            return '-'
        if node.is_unary_tilde:
            return '~'
        raise RuntimeError('Type of unary operator not specified!')

    def print_unit_type(self, node):
        if node.is_encapsulated:
            return '(' + self.print_node(node.compound_unit) + ')'
        if node.is_pow:
            return self.print_node(node.base) + '**' + str(node.exponent)
        if node.is_arithmetic_expression():
            t_lhs = self.print_node(node.get_lhs()) if isinstance(node.get_lhs(), ASTUnitType) else str(node.get_lhs())
            if node.is_times:
                return t_lhs + '*' + self.print_node(node.get_rhs())
            else:
                return t_lhs + '/' + self.print_node(node.get_rhs())
        else:
            return node.unit

    def print_update_block(self, node):
        ret = print_ml_comments(node.pre_comments, self.indent, False)
        ret += print_n_spaces(self.indent) + 'update:' + print_sl_comment(node.in_comment) + '\n'
        ret += self.print_node(node.get_block()) + print_n_spaces(self.indent) + 'end\n'
        ret += print_ml_comments(node.post_comments, self.indent, True)
        return ret

    @classmethod
    def print_variable(cls, node):
        ret = node.name
        for i in range(1, node.differential_order + 1):
            ret += "'"

        return ret

    def print_while_stmt(self, node):
        temp_indent = self.indent
        self.inc_indent()
        ret = print_ml_comments(node.pre_comments, temp_indent, False)
        ret += print_n_spaces(temp_indent) + 'while ' + self.print_node(node.get_condition()) + ':' + print_sl_comment(node.in_comment) + '\n'
        ret += self.print_node(node.get_block()) + print_n_spaces(temp_indent) + 'end\n'
        self.dec_indent()
        ret += print_ml_comments(node.post_comments, temp_indent, True)
        return ret

    def inc_indent(self):
        self.indent += self.tab_size

    def dec_indent(self):
        self.indent -= self.tab_size


def print_n_spaces(n):
    return ' ' * n


def print_ml_comments(comments, indent=0, is_post=False):
    if comments is None or len(list(comments)) == 0:
        return ''
    ret = ''
    if len(comments) > 0 and not is_post:
        ret += '\n'
    for comment in comments:
        ret += print_n_spaces(indent) + '/*'
        for c_line in comment.splitlines(True):
            if c_line == '\n':
                ret += print_n_spaces(indent) + '*' + '\n'
                continue
            elif c_line.lstrip() == '':
                continue
            if comment.splitlines(True).index(c_line) != 0:
                ret += print_n_spaces(indent)
                ret += '*  ' if c_line[(len(c_line) - len(c_line.lstrip()))] != '*' and len(comment.splitlines(True)) > 1 else ''
            ret += c_line

        if len(comment.splitlines(True)) > 1:
            ret += print_n_spaces(indent)
        ret += '*/\n'

    if len(comments) > 0 and is_post:
        ret += '\n'
    return ret


def print_sl_comment(comment):
    if comment is not None:
        return ' # ' + comment.lstrip()
    else:
        return ''


def filter_subsequent_whitespaces(string):
    """
    This filter reduces more then one newlines to exactly one, e.g.:
        l1
        

        

        

        l2
    is filtered to
        l1
        

        l2
    """
    s_lines = string.splitlines(True)
    for index, item in enumerate(s_lines, start=0):
        if index < len(s_lines) - 1 and item == '\n' and s_lines[(index + 1)] == '\n':
            del s_lines[index + 1]

    ret = ''.join(s_lines)
    return ret