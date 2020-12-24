# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_buffer_qualifier_unique.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2769 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoBufferQualifierUnique(CoCo):
    __doc__ = '\n    This coco ensures that each spike buffer has at most one type of modifier inhibitory and excitatory.\n    Allowed:\n        spike <- inhibitory spike\n    Not allowed:\n        spike <- inhibitory inhibitory spike\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        cls.neuronName = node.get_name()
        node.accept(BufferQualifierUniqueVisitor())


class BufferQualifierUniqueVisitor(ASTVisitor):
    __doc__ = '\n    This visitor ensures that all buffers are qualified uniquely by keywords.\n    '

    def visit_input_port(self, node):
        """
        Checks the coco on the current node.
        :param node: a single input port.
        :type node: ASTInputPort
        """
        if node.is_spike() and node.has_input_qualifiers() and len(node.get_input_qualifiers()) > 1:
            inh = 0
            ext = 0
            for typ in node.get_input_qualifiers():
                if typ.is_excitatory:
                    ext += 1
                if typ.is_inhibitory:
                    inh += 1

            if inh > 1:
                code, message = Messages.get_multiple_keywords('inhibitory')
                Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)
            if ext > 1:
                code, message = Messages.get_multiple_keywords('excitatory')
                Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)