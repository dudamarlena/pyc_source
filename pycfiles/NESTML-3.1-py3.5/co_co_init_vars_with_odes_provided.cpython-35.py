# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_init_vars_with_odes_provided.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3687 bytes
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoInitVarsWithOdesProvided(CoCo):
    __doc__ = '\n    This CoCo ensures that all variables which have been declared in the "initial_values" block are provided \n    with a corresponding ode.\n    Allowed:\n        initial_values:\n            V_m mV = E_L\n        end\n        ...\n        equations:\n            V_m\' = ...\n        end\n    Not allowed:        \n        initial_values:\n            V_m mV = E_L\n        end\n        ...\n        equations:\n            # no ode declaration given\n        end\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Checks this coco on the handed over neuron.
        :param node: a single neuron instance.
        :type node: ASTNeuron
        """
        assert node is not None and isinstance(node, ASTNeuron), '(PyNestML.CoCo.VariablesDefined) No or wrong type of neuron provided (%s)!' % type(node)
        node.accept(InitVarsVisitor())


class InitVarsVisitor(ASTVisitor):
    __doc__ = '\n    This visitor checks that all variables as provided in the init block have been provided with an ode.\n    '

    def visit_declaration(self, node):
        """
        Checks the coco on the current node.
        :param node: a single declaration.
        :type node: ast_declaration
        """
        for var in node.get_variables():
            symbol = node.get_scope().resolve_to_symbol(var.get_complete_name(), SymbolKind.VARIABLE)
            if symbol is not None and symbol.is_init_values() and not node.has_expression():
                code, message = Messages.get_no_rhs(symbol.get_symbol_name())
                Logger.log_message(error_position=var.get_source_position(), code=code, message=message, log_level=LoggingLevel.WARNING)
            if symbol is not None and symbol.is_init_values() and not symbol.is_ode_defined() and not symbol.is_function:
                code, message = Messages.get_no_ode(symbol.get_symbol_name())
                Logger.log_message(error_position=var.get_source_position(), code=code, message=message, log_level=LoggingLevel.WARNING)
            if symbol is not None and symbol.is_init_values() and not symbol.has_initial_value():
                code, message = Messages.get_no_init_value(symbol.get_symbol_name())
                Logger.log_message(error_position=var.get_source_position(), code=code, message=message, log_level=LoggingLevel.WARNING)