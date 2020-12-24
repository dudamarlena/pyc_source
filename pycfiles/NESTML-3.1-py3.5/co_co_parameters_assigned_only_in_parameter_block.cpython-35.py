# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_parameters_assigned_only_in_parameter_block.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2858 bytes
from pynestml.meta_model.ast_neuron import ASTNeuron
from pynestml.cocos.co_co import CoCo
from pynestml.symbol_table.scope import ScopeType
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.variable_symbol import BlockType
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoParametersAssignedOnlyInParameterBlock(CoCo):
    __doc__ = '\n    This coco checks that no parameters are assigned outside the parameters block.\n    Allowed:\n        parameters:\n            par mV = 10mV\n        end\n    Not allowed:\n        parameters:\n            par mV = 10mV\n        end\n        ...\n        update:\n           par = 20mV\n        end    \n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ASTNeuron
        """
        assert node is not None and isinstance(node, ASTNeuron), '(PyNestML.CoCo.BufferNotAssigned) No or wrong type of neuron provided (%s)!' % type(node)
        node.accept(ParametersAssignmentVisitor())


class ParametersAssignmentVisitor(ASTVisitor):
    __doc__ = '\n    This visitor checks that no parameters have been assigned outside the parameters block.\n    '

    def visit_assignment(self, node):
        """
        Checks the coco on the current node.
        :param node: a single node.
        :type node: ast_assignment
        """
        symbol = node.get_scope().resolve_to_symbol(node.get_variable().get_name(), SymbolKind.VARIABLE)
        if symbol is not None and symbol.block_type == BlockType.PARAMETERS and node.get_scope().get_scope_type() != ScopeType.GLOBAL:
            code, message = Messages.get_assignment_not_allowed(node.get_variable().get_complete_name())
            Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)