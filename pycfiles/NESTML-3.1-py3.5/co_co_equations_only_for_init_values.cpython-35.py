# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_equations_only_for_init_values.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2482 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoEquationsOnlyForInitValues(CoCo):
    __doc__ = "\n    This coco ensures that ode equations are only provided for variables which have been defined in the\n    initial_values block.\n    Allowed:\n        initial_values:\n            V_m mV = 10mV\n        end\n        equations:\n            V_m' = ....\n        end\n    Not allowed:\n        state:\n            V_m mV = 10mV\n        end\n        equations:\n            V_m' = ....\n        end\n    "

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(EquationsOnlyForInitValues())


class EquationsOnlyForInitValues(ASTVisitor):
    __doc__ = '\n    This visitor ensures that for all ode equations exists an initial value.\n    '

    def visit_ode_equation(self, node):
        """
        Ensures the coco.
        :param node: a single equation object.
        :type node: ast_ode_equation
        """
        symbol = node.get_scope().resolve_to_symbol(node.get_lhs().get_name_of_lhs(), SymbolKind.VARIABLE)
        if symbol is not None and not symbol.is_init_values():
            code, message = Messages.get_equation_var_not_in_init_values_block(node.get_lhs().get_name_of_lhs())
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)
            return