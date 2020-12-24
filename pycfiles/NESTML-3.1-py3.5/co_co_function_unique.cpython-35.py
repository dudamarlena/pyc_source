# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_function_unique.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3276 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages

class CoCoFunctionUnique(CoCo):
    __doc__ = '\n    This Coco ensures that each function is defined exactly once (thus no redeclaration occurs).\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Checks if each function is defined uniquely.
        :param node: a single neuron
        :type node: ast_neuron
        """
        checked_funcs_names = list()
        for func in node.get_functions():
            if func.get_name() not in checked_funcs_names:
                symbols = func.get_scope().resolve_to_all_symbols(func.get_name(), SymbolKind.FUNCTION)
                if isinstance(symbols, list) and len(symbols) > 1:
                    checked = list()
                    for funcA in symbols:
                        for funcB in symbols:
                            if funcA is not funcB and funcB not in checked:
                                if funcA.is_predefined:
                                    code, message = Messages.get_function_redeclared(funcA.get_symbol_name(), True)
                                    Logger.log_message(error_position=funcB.get_referenced_object().get_source_position(), log_level=LoggingLevel.ERROR, message=message, code=code)
                                else:
                                    if funcB.is_predefined:
                                        code, message = Messages.get_function_redeclared(funcA.get_symbol_name(), True)
                                        Logger.log_message(error_position=funcA.get_referenced_object().get_source_position(), log_level=LoggingLevel.ERROR, message=message, code=code)
                                    else:
                                        code, message = Messages.get_function_redeclared(funcA.get_symbol_name(), False)
                                        Logger.log_message(error_position=funcB.get_referenced_object().get_source_position(), log_level=LoggingLevel.ERROR, message=message, code=code)

                        checked.append(funcA)

                checked_funcs_names.append(func.get_name())