# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_variable_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2914 bytes
"""
simpleExpression : variable
"""
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import MessageCode
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTVariableVisitor(ASTVisitor):
    __doc__ = '\n    This visitor visits a single variable and updates its type.\n    '

    def visit_simple_expression(self, node):
        """
        Visits a single variable as contained in a simple expression and derives its type.
        :param node: a single simple expression
        :type node: ASTSimpleExpression
        """
        assert isinstance(node, ASTSimpleExpression), '(PyNestML.Visitor.VariableVisitor) No or wrong type of simple expression provided (%s)!' % type(node)
        assert node.get_scope() is not None, '(PyNestML.Visitor.VariableVisitor) No scope found, run symboltable creator!'
        scope = node.get_scope()
        var_name = node.get_variable().get_name()
        var_resolve = scope.resolve_to_symbol(var_name, SymbolKind.VARIABLE)
        if var_resolve is not None:
            node.type = var_resolve.get_type_symbol()
            node.type.referenced_object = node
        else:
            var_resolve = scope.resolve_to_symbol(var_name, SymbolKind.TYPE)
            if var_resolve is not None:
                node.type = var_resolve
                node.type.referenced_object = node
            else:
                message = 'Variable ' + str(node) + ' could not be resolved!'
                Logger.log_message(code=MessageCode.SYMBOL_NOT_RESOLVED, error_position=node.get_source_position(), message=message, log_level=LoggingLevel.ERROR)
                node.type = ErrorTypeSymbol()

    def visit_expression(self, node):
        raise Exception('Deprecated method used!')