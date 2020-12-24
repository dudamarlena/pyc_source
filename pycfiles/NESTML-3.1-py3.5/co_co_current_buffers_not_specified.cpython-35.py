# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/cocos/co_co_current_buffers_not_specified.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2180 bytes
from pynestml.cocos.co_co import CoCo
from pynestml.utils.logger import LoggingLevel, Logger
from pynestml.utils.messages import Messages
from pynestml.visitors.ast_visitor import ASTVisitor

class CoCoCurrentBuffersNotSpecified(CoCo):
    __doc__ = '\n    This coco ensures that current buffers are not specified with a qualifier.\n    Allowed:\n        input:\n            current <- current\n        end\n    Not allowed:\n        input:\n            current <- inhibitory current\n        end\n    '

    @classmethod
    def check_co_co(cls, node):
        """
        Ensures the coco for the handed over neuron.
        :param node: a single neuron instance.
        :type node: ast_neuron
        """
        node.accept(CurrentQualifierSpecifiedVisitor())


class CurrentQualifierSpecifiedVisitor(ASTVisitor):
    __doc__ = '\n    This visitor ensures that current buffers are not specified with an `inputQualifier`, e.g. excitatory, inhibitory.\n    '

    def visit_input_port(self, node):
        if node.is_current() and node.has_input_qualifiers() and len(node.get_input_qualifiers()) > 0:
            code, message = Messages.get_current_buffer_specified(node.get_name(), list(str(buf) for buf in node.get_input_qualifiers()))
            Logger.log_message(error_position=node.get_source_position(), code=code, message=message, log_level=LoggingLevel.ERROR)