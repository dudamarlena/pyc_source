# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_buffer_not_assigned.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2192 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.symbols.symbol import SymbolKind
from pynestml.symbols.variable_symbol import BlockType
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoBufferNotAssigned(CoCo):
    __doc__ = '\n    This coco ensures that no values are assigned to buffers.\n    Allowed:\n        currentSum = current + 10mV # current being a buffer\n    Not allowed:\n        current = currentSum + 10mV\n    \n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(NoBufferAssignedVisitor())


class NoBufferAssignedVisitor(ASTVisitor):

    def visit_assignment(self, node):
        symbol = node.get_scope().resolve_to_symbol(node.get_variable().get_name(), SymbolKind.VARIABLE)
        if symbol is not None and (symbol.block_type == BlockType.INPUT_BUFFER_SPIKE or symbol.block_type == BlockType.INPUT_BUFFER_CURRENT):
            code, message = Messages.get_value_assigned_to_buffer(node.get_variable().get_complete_name())
            Logger.log_message(code=code, message=message, error_position=node.get_source_position(), log_level=LoggingLevel.ERROR)