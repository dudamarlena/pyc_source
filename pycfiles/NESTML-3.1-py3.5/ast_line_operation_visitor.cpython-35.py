# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_line_operation_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2233 bytes
"""
rhs : left=rhs (plusOp='+'  | minusOp='-') right=rhs
"""
from pynestml.visitors.ast_visitor import ASTVisitor
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages

class ASTLineOperatorVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single binary operation consisting of + or - and updates the type accordingly.\n    '

    def visit_expression(self, node):
        """
        Visits a single expression containing a plus or minus operator and updates its type.
        :param node: a single expression
        :type node: ast_expression
        """
        lhs_type = node.get_lhs().type
        rhs_type = node.get_rhs().type
        arith_op = node.get_binary_operator()
        lhs_type.referenced_object = node.get_lhs()
        rhs_type.referenced_object = node.get_rhs()
        node.type = ErrorTypeSymbol()
        if arith_op.is_plus_op:
            node.type = lhs_type + rhs_type
        elif arith_op.is_minus_op:
            node.type = lhs_type - rhs_type
        if isinstance(node.type, ErrorTypeSymbol):
            code, message = Messages.get_binary_operation_type_could_not_be_derived(lhs=str(node.get_lhs()), operator=str(arith_op), rhs=str(node.get_rhs()), lhs_type=str(lhs_type.print_nestml_type()), rhs_type=str(rhs_type.print_nestml_type()))
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)