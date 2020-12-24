# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_variable_once_per_scope.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3740 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.variable_symbol import VariableType
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages

class CoCoVariableOncePerScope(CoCo):
    __doc__ = '\n    This coco ensures that each variables is defined at most once per scope, thus no redeclaration occurs.\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Checks if each variable is defined at most once per scope. Obviously, this test does not check if a declaration
        is shadowed by an embedded scope.
        :param node: a single neuron
        :type node: ast_neuron
        """
        cls._CoCoVariableOncePerScope__check_scope(node, node.get_scope())

    @classmethod
    def __check_scope(cls, neuron, scope):
        """
        Checks a single scope and proceeds recursively.
        :param neuron: a single neuron object, required for correct printing of messages.
        :type neuron: ast_neuron
        :param scope: a single scope to check.
        :type scope: Scope
        """
        checked = list()
        for sym1 in scope.get_symbols_in_this_scope():
            if not sym1.get_symbol_kind() != SymbolKind.VARIABLE:
                if sym1.is_predefined:
                    pass
                else:
                    for sym2 in scope.get_symbols_in_complete_scope():
                        if sym1 is not sym2 and sym1.get_symbol_name() == sym2.get_symbol_name() and sym2 not in checked:
                            if sym2.get_symbol_kind() == SymbolKind.TYPE:
                                code, message = Messages.get_variable_with_same_name_as_type(sym1.get_symbol_name())
                                Logger.log_message(error_position=sym1.get_referenced_object().get_source_position(), neuron=neuron, log_level=LoggingLevel.WARNING, code=code, message=message)
                        elif sym1.get_symbol_kind() == sym2.get_symbol_kind():
                            if sym2.is_predefined:
                                code, message = Messages.get_variable_redeclared(sym1.get_symbol_name(), True)
                                Logger.log_message(error_position=sym1.get_referenced_object().get_source_position(), neuron=neuron, log_level=LoggingLevel.ERROR, code=code, message=message)
                            elif sym1.get_referenced_object().get_source_position().before(sym2.get_referenced_object().get_source_position()):
                                code, message = Messages.get_variable_redeclared(sym1.get_symbol_name(), False)
                                Logger.log_message(error_position=sym2.get_referenced_object().get_source_position(), neuron=neuron, log_level=LoggingLevel.ERROR, code=code, message=message)

                    checked.append(sym1)

        for scope in scope.get_scopes():
            cls._CoCoVariableOncePerScope__check_scope(neuron, scope)