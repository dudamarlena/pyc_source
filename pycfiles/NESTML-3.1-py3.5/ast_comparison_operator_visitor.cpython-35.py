# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_comparison_operator_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3284 bytes
"""
rhs : left=rhs comparisonOperator right=rhs
"""
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.unit_type_symbol import UnitTypeSymbol
from pynestml.utils.error_strings import ErrorStrings
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import MessageCode
from pynestml.visitors.ast_visitor import ASTVisitor
from pynestml.symbols.boolean_type_symbol import BooleanTypeSymbol
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol

class ASTComparisonOperatorVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single rhs consisting of a binary comparison operator.\n    '

    def visit_expression(self, expr):
        """
        Visits a single comparison operator expression and updates the type.
        :param expr: an expression
        :type expr: ast_expression
        """
        lhs_type = expr.get_lhs().type
        rhs_type = expr.get_rhs().type
        lhs_type.referenced_object = expr.get_lhs()
        rhs_type.referenced_object = expr.get_rhs()
        if lhs_type.is_numeric_primitive() and rhs_type.is_numeric_primitive() or lhs_type.equals(rhs_type) and lhs_type.is_numeric() or isinstance(lhs_type, BooleanTypeSymbol) and isinstance(rhs_type, BooleanTypeSymbol):
            expr.type = PredefinedTypes.get_boolean_type()
            return
        else:
            if isinstance(lhs_type, UnitTypeSymbol) and rhs_type.is_numeric() or isinstance(rhs_type, UnitTypeSymbol) and lhs_type.is_numeric():
                error_msg = ErrorStrings.message_comparison(self, expr.get_source_position())
                expr.type = PredefinedTypes.get_boolean_type()
                Logger.log_message(message=error_msg, code=MessageCode.SOFT_INCOMPATIBILITY, error_position=expr.get_source_position(), log_level=LoggingLevel.WARNING)
                return
            error_msg = ErrorStrings.message_comparison(self, expr.get_source_position())
            expr.type = ErrorTypeSymbol()
            Logger.log_message(code=MessageCode.HARD_INCOMPATIBILITY, error_position=expr.get_source_position(), message=error_msg, log_level=LoggingLevel.ERROR)
            return