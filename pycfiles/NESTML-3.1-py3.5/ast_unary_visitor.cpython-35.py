# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_unary_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1653 bytes
"""
Expr = unaryOperator term=rhs
unaryOperator : (unaryPlus='+' | unaryMinus='-' | unaryTilde='~');
"""
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTUnaryVisitor(ASTVisitor):
    __doc__ = '\n    Visits an rhs consisting of a unary operator, e.g., -, and a sub-rhs.\n    '

    def visit_expression(self, node):
        """
        Visits a single unary operator and updates the type of the corresponding expression.
        :param node: a single expression
        :type node: ast_expression
        """
        term_type = node.get_expression().type
        unary_op = node.get_unary_operator()
        term_type.referenced_object = node.get_expression()
        if unary_op.is_unary_minus:
            node.type = -term_type
            return
        if unary_op.is_unary_plus:
            node.type = +term_type
            return
        if unary_op.is_unary_tilde:
            node.type = ~term_type
            return