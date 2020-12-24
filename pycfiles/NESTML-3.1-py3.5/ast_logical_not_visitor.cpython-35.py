# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_logical_not_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1281 bytes
"""
rhs: logicalNot='not' term=rhs
"""
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTLogicalNotVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single rhs and updates the type of the sub-rhs.\n    '

    def visit_expression(self, node):
        """
        Visits a single rhs with a logical operator and updates the type.
        :param node: a single rhs
        :type node: ast_expression
        """
        expr_type = node.get_expression().type
        expr_type.referenced_object = node.get_expression()
        node.type = expr_type.negate()