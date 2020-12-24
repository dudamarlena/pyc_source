# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_buffer_data_type.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2142 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoBufferDataType(CoCo):
    __doc__ = '\n    This coco ensures that all spike and current buffers have a data type stated.\n    Allowed:\n        input:\n            spikeIn integer <- inhibitory spike\n            current pA <- current\n        end\n\n    Not allowed:\n        input:\n            spikeIn <- inhibitory spike\n            current <- current\n        end\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(BufferDatatypeVisitor())


class BufferDatatypeVisitor(ASTVisitor):
    __doc__ = '\n    This visitor checks if each buffer has a datatype selected according to the coco.\n    '

    def visit_input_port(self, node):
        """
        Checks the coco on the current node.
        :param node: a single input port node.
        :type node: ASTInputPort
        """
        if not node.has_datatype():
            code, message = Messages.get_data_type_not_specified(node.get_name())
            Logger.log_message(error_position=node.get_source_position(), log_level=LoggingLevel.ERROR, code=code, message=message)