# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_function_call_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5243 bytes
"""
simpleExpression : functionCall
"""
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.template_type_symbol import TemplateTypeSymbol
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.void_type_symbol import VoidTypeSymbol
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTFunctionCallVisitor(ASTVisitor):
    __doc__ = '\n    Visits a single function call and updates its type.\n    '

    def visit_simple_expression(self, node):
        """
        Visits a single function call as stored in a simple expression and derives the correct type of all its
        parameters. :param node: a simple expression :type node: ASTSimpleExpression :rtype void
        """
        assert isinstance(node, ASTSimpleExpression), '(PyNestML.Visitor.FunctionCallVisitor) No or wrong type of simple expression provided (%s)!' % tuple(node)
        assert node.get_scope() is not None, '(PyNestML.Visitor.FunctionCallVisitor) No scope found, run symboltable creator!'
        scope = node.get_scope()
        function_name = node.get_function_call().get_name()
        method_symbol = scope.resolve_to_symbol(function_name, SymbolKind.FUNCTION)
        if method_symbol is None:
            code, message = Messages.get_could_not_resolve(function_name)
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
            node.type = ErrorTypeSymbol()
            return
        return_type = method_symbol.get_return_type()
        if isinstance(return_type, TemplateTypeSymbol):
            for i, arg_type in enumerate(method_symbol.param_types):
                if arg_type == return_type:
                    return_type = node.get_function_call().get_args()[i].type
                    break

            if isinstance(return_type, TemplateTypeSymbol):
                assert False
            from pynestml.cocos.co_co_function_argument_template_types_consistent import CorrectTemplatedArgumentTypesVisitor
            correctTemplatedArgumentTypesVisitor = CorrectTemplatedArgumentTypesVisitor()
            correctTemplatedArgumentTypesVisitor._failure_occurred = False
            node.accept(correctTemplatedArgumentTypesVisitor)
            if correctTemplatedArgumentTypesVisitor._failure_occurred:
                return_type = ErrorTypeSymbol()
        return_type.referenced_object = node
        if function_name == PredefinedFunctions.CONVOLVE:
            buffer_parameter = node.get_function_call().get_args()[1]
            if buffer_parameter.get_variable() is not None:
                buffer_name = buffer_parameter.get_variable().get_name()
                buffer_symbol_resolve = scope.resolve_to_symbol(buffer_name, SymbolKind.VARIABLE)
                if buffer_symbol_resolve is not None:
                    node.type = buffer_symbol_resolve.get_type_symbol()
                    return
                code, message = Messages.get_convolve_needs_buffer_parameter()
                Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
                node.type = ErrorTypeSymbol()
                return
        if isinstance(method_symbol.get_return_type(), VoidTypeSymbol):
            node.type = ErrorTypeSymbol()
            return
        node.type = return_type