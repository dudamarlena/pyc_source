# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_function_argument_template_types_consistent.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5096 bytes
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.meta_model.ast_declaration import ASTDeclaration
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.logging_helper import LoggingHelper
from pynestml.utils.messages import Messages
from pynestml.utils.type_caster import TypeCaster
from pynestml.visitors.ast_visitor import ASTVisitor
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.template_type_symbol import TemplateTypeSymbol
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.void_type_symbol import VoidTypeSymbol

class CoCoFunctionArgumentTemplateTypesConsistent(CoCo):
    __doc__ = '\n    This coco checks that if template types are used for function parameters, the types are mutually consistent.\n    '

    @classmethod
    def check_co_co(cls, neuron):
        """
        Ensures the coco for the handed over neuron.
        :param neuron: a single neuron instance.
        :type neuron: ASTNeuron
        """
        neuron.accept(CorrectTemplatedArgumentTypesVisitor())


class CorrectTemplatedArgumentTypesVisitor(ASTVisitor):
    __doc__ = '\n    This visitor checks that all expression correspond to the expected type.\n    '

    def visit_simple_expression(self, node):
        """
        Visits a single function call as stored in a simple expression and, if template types are used for function parameters, checks if all actual parameter types are mutually consistent.

        :param node: a simple expression
        :type node: ASTSimpleExpression
        :rtype None:
        """
        assert isinstance(node, ASTSimpleExpression), '(PyNestML.Visitor.FunctionCallVisitor) No or wrong type of simple expression provided (%s)!' % tuple(node)
        assert node.get_scope() is not None, '(PyNestML.Visitor.FunctionCallVisitor) No scope found, run symboltable creator!'
        scope = node.get_scope()
        if node.get_function_call() is None:
            return
        function_name = node.get_function_call().get_name()
        method_symbol = scope.resolve_to_symbol(function_name, SymbolKind.FUNCTION)
        if method_symbol is None:
            code, message = Messages.get_could_not_resolve(function_name)
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
            self._failure_occurred = True
            return
        return_type = method_symbol.get_return_type()
        template_symbol_to_actual_symbol = {}
        template_symbol_to_parameter_indices = {}
        for arg_idx, arg_type in enumerate(method_symbol.param_types):
            if isinstance(arg_type, TemplateTypeSymbol):
                actual_symbol = node.get_function_call().get_args()[arg_idx].type
                if arg_type._i in template_symbol_to_actual_symbol.keys():
                    if not template_symbol_to_actual_symbol[arg_type._i].differs_only_in_magnitude(actual_symbol) and not template_symbol_to_actual_symbol[arg_type._i].is_castable_to(actual_symbol):
                        code, message = Messages.templated_arg_types_inconsistent(function_name, arg_idx, template_symbol_to_parameter_indices[arg_type._i], failing_arg_type_str=actual_symbol.print_nestml_type(), other_type_str=template_symbol_to_actual_symbol[arg_type._i].print_nestml_type())
                        Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
                        self._failure_occurred = True
                        return
                    template_symbol_to_parameter_indices[arg_type._i] += [arg_idx]
                else:
                    template_symbol_to_actual_symbol[arg_type._i] = actual_symbol
                    template_symbol_to_parameter_indices[arg_type._i] = [arg_idx]