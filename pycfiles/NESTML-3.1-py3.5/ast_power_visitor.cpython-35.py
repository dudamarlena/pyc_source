# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_power_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3569 bytes
"""
rhs : <assoc=right> left=rhs powOp='**' right=rhs
"""
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.either import Either
from pynestml.utils.error_strings import ErrorStrings
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTPowerVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single power rhs and updates its types accordingly.\n    '

    def visit_expression(self, node):
        """
        Visits a single power expression and updates the types.
        :param node: a single expression.
        :type node: ASTExpression
        """
        base_type = node.get_lhs().type
        exponent_type = node.get_rhs().type
        base_type.referenced_object = node.get_lhs()
        exponent_type.referenced_object = node.get_rhs()
        if base_type.is_instance_of(UnitTypeSymbol):
            node.type = self.try_to_calculate_resulting_unit(node)
            return
        else:
            node.type = base_type ** exponent_type
            return

    def try_to_calculate_resulting_unit(self, expr):
        base_type = expr.get_lhs().type
        exponent_numeric_value_either = self.calculate_numeric_value(expr.get_rhs())
        if exponent_numeric_value_either.is_value():
            return base_type ** exponent_numeric_value_either.get_value()
        else:
            return base_type ** None

    def calculate_numeric_value(self, expr):
        """
        Calculates the numeric value of a exponent.
        :param expr: a single expression
        :type expr: ASTSimpleExpression or ASTExpression
        :return: an Either object
        :rtype: Either
        """
        if isinstance(expr, ASTExpression) and expr.is_encapsulated:
            return self.calculate_numeric_value(expr.get_expression())
        if isinstance(expr, ASTSimpleExpression) and expr.get_numeric_literal() is not None:
            if isinstance(expr.get_numeric_literal(), int) or isinstance(expr.get_numeric_literal(), float):
                literal = expr.get_numeric_literal()
                return Either.value(literal)
            else:
                error_message = ErrorStrings.message_unit_base(self, expr.get_source_position())
                return Either.error(error_message)
        elif expr.is_unary_operator() and expr.get_unary_operator().is_unary_minus:
            term = self.calculate_numeric_value(expr.get_expression())
            if term.is_error():
                return term
            return Either.value(-term.get_value())
        error_message = ErrorStrings.message_non_constant_exponent(self, expr.get_source_position())
        return Either.error(error_message)