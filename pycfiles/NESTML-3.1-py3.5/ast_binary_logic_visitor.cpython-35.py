# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_binary_logic_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2359 bytes
"""
rhs: left=rhs logicalOperator right=rhs
"""
from pynestml.symbols.boolean_type_symbol import BooleanTypeSymbol
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTBinaryLogicVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single binary logical operator rhs and updates its types.\n    '

    def visit_expression(self, node):
        """
        Visits an expression which uses a binary logic operator and updates the type.
        :param node: a single expression.
        :type node: ast_expression
        """
        lhs_type = node.get_lhs().type
        rhs_type = node.get_rhs().type
        lhs_type.referenced_object = node.get_lhs()
        rhs_type.referenced_object = node.get_rhs()
        if isinstance(lhs_type, BooleanTypeSymbol) and isinstance(rhs_type, BooleanTypeSymbol):
            node.type = PredefinedTypes.get_boolean_type()
        else:
            if isinstance(lhs_type, BooleanTypeSymbol):
                offending_type = lhs_type
            else:
                offending_type = rhs_type
            code, message = Messages.get_type_different_from_expected(BooleanTypeSymbol(), offending_type)
            Logger.log_message(code=code, message=message, error_position=lhs_type.referenced_object.get_source_position(), log_level=LoggingLevel.ERROR)
            node.type = ErrorTypeSymbol()