# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_dot_operator_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1704 bytes
"""
rhs : left=rhs (timesOp='*' | divOp='/' | moduloOp='%') right=rhs
"""
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTDotOperatorVisitor(ASTVisitor):
    __doc__ = '\n    This visitor is used to derive the correct type of expressions which use a binary dot operator.\n    '

    def visit_expression(self, node):
        """
        Visits a single rhs and updates the type.
        :param node: a single rhs
        :type node: ast_expression
        """
        lhs_type = node.get_lhs().type
        rhs_type = node.get_rhs().type
        arith_op = node.get_binary_operator()
        lhs_type.referenced_object = node.get_lhs()
        rhs_type.referenced_object = node.get_rhs()
        if arith_op.is_modulo_op:
            node.type = lhs_type % rhs_type
            return
        if arith_op.is_div_op:
            node.type = lhs_type / rhs_type
            return
        if arith_op.is_times_op:
            node.type = lhs_type * rhs_type
            return