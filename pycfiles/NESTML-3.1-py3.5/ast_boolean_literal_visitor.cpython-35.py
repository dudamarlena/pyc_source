# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_boolean_literal_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1364 bytes
"""
simpleExpression : BOOLEAN_LITERAL // true & false ;
"""
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTBooleanLiteralVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single boolean literal and updates its type.\n    '

    def visit_simple_expression(self, node):
        """
        Visits a single simple rhs containing a boolean literal and updates its type.
        :param node: a simple rhs.
        :type node: ast_simple_expression
        """
        node.type = PredefinedTypes.get_boolean_type()
        node.type.referenced_object = node