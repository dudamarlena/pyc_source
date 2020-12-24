# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_function_calls_consistent.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 4079 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.error_type_symbol import ErrorTypeSymbol
from pynestml.symbols.template_type_symbol import TemplateTypeSymbol
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.utils.type_caster import TypeCaster
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoFunctionCallsConsistent(CoCo):
    __doc__ = '\n    This context condition checker ensures that for all function calls in the handed over neuron, if the called function has been declared, whether the number and types of arguments correspond to the declaration, etc.\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Checks the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ASTNeuron
        """
        node.accept(FunctionCallConsistencyVisitor())


class FunctionCallConsistencyVisitor(ASTVisitor):
    __doc__ = '\n    This visitor ensures that all function calls are consistent.\n    '

    def visit_function_call(self, node):
        """
        Check consistency for a single function call: check if the called function has been declared, whether the number and types of arguments correspond to the declaration, etc.

        :param node: a single function call.
        :type node: ASTFunctionCall
        """
        func_name = node.get_name()
        if func_name == 'convolve' or func_name == 'cond_sum' or func_name == 'curr_sum':
            return
        symbol = node.get_scope().resolve_to_symbol(node.get_name(), SymbolKind.FUNCTION)
        if symbol is None:
            code, message = Messages.get_function_not_declared(node.get_name())
            Logger.log_message(error_position=node.get_source_position(), log_level=LoggingLevel.ERROR, code=code, message=message)
            return
        if len(node.get_args()) != len(symbol.get_parameter_types()):
            code, message = Messages.get_wrong_number_of_args(str(node), len(symbol.get_parameter_types()), len(node.get_args()))
            Logger.log_message(code=code, message=message, log_level=LoggingLevel.ERROR, error_position=node.get_source_position())
            return
        expected_types = symbol.get_parameter_types()
        actual_args = node.get_args()
        actual_types = [arg.type for arg in actual_args]
        for actual_arg, actual_type, expected_type in zip(actual_args, actual_types, expected_types):
            if isinstance(actual_type, ErrorTypeSymbol):
                code, message = Messages.get_type_could_not_be_derived(actual_arg)
                Logger.log_message(code=code, message=message, log_level=LoggingLevel.ERROR, error_position=actual_arg.get_source_position())
                return
            if not actual_type.equals(expected_type) and not isinstance(expected_type, TemplateTypeSymbol):
                TypeCaster.try_to_recover_or_error(expected_type, actual_type, actual_arg)