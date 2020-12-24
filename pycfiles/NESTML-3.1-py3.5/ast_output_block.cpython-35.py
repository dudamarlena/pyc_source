# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_output_block.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2969 bytes
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_signal_type import ASTSignalType
from pynestml.meta_model.ast_source_location import ASTSourceLocation

class ASTOutputBlock(ASTNode):
    __doc__ = "\n    This class is used to store output buffer declarations.\n    ASTOutput represents the output block of the neuron:\n        output: spike\n      @attribute spike true iff the neuron has a spike output.\n      @attribute current true iff. the neuron is a current output.\n    Grammar:\n        outputBlock: 'output' BLOCK_OPEN ('spike' | 'current') ;\n    Attributes:\n        type = None\n    "

    def __init__(self, o_type, source_position):
        """
        Standard constructor.
        :param o_type: the type of the output buffer.
        :type o_type: SignalType
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTOutputBlock, self).__init__(source_position)
        self.type = o_type

    def is_spike(self):
        """
        Returns whether it is a spike buffer or not.
        :return: True if spike, otherwise False.
        :rtype: bool
        """
        return self.type is ASTSignalType.SPIKE

    def is_current(self):
        """
        Returns whether it is a current buffer or not.
        :return: True if current, otherwise False.
        :rtype: bool
        """
        return self.type is ASTSignalType.CURRENT

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        pass

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equals, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTOutputBlock):
            return False
        return self.is_spike() == other.is_spike() and self.is_current() == other.is_current()