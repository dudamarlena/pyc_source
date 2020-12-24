# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_string_literal_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1358 bytes
"""
simpleExpression : string=STRING_LITERAL
"""
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTStringLiteralVisitor(ASTVisitor):
    __doc__ = '\n    Visits a string literal and updates its type.\n    '

    def visit_simple_expression(self, node):
        """
        Visits a singe simple rhs which consists of a string literal and updates the type.
        :param node: a simple rhs containing a string literal
        :type node: ast_simple_expression
        """
        node.type = PredefinedTypes.get_string_type()
        node.type.referenced_object = node