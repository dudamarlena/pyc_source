# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_numeric_literal_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2488 bytes
"""
simpleExpression : (UNSIGNED_INTEGER | FLOAT) (variable)?
"""
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.symbol import SymbolKind
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTNumericLiteralVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single numeric literal and updates its type.\n    '

    def visit_simple_expression(self, node):
        """
        Visit a simple rhs and update the type of a numeric literal.
        :param node: a single meta_model node
        :type node: ast_node
        :return: no value returned, the type is updated in-place
        :rtype: void
        """
        assert node.get_scope() is not None, 'Run symboltable creator.'
        if node.get_variable() is not None:
            scope = node.get_scope()
            var_name = node.get_variable().get_name()
            variable_symbol_resolve = scope.resolve_to_symbol(var_name, SymbolKind.VARIABLE)
            if variable_symbol_resolve is not None:
                node.type = variable_symbol_resolve.get_type_symbol()
            else:
                node.type = scope.resolve_to_symbol(var_name, SymbolKind.TYPE)
            node.type.referenced_object = node
            return
        if node.get_numeric_literal() is not None and isinstance(node.get_numeric_literal(), float):
            node.type = PredefinedTypes.get_real_type()
            node.type.referenced_object = node
            return
        if node.get_numeric_literal() is not None and isinstance(node.get_numeric_literal(), int):
            node.type = PredefinedTypes.get_integer_type()
            node.type.referenced_object = node
            return