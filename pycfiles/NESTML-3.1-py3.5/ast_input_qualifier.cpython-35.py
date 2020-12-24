# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_input_qualifier.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2625 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTInputQualifier(ASTNode):
    __doc__ = "\n    This class is used to store the qualifier of a buffer.\n    ASTInputQualifier represents the qualifier of the input port. Only valid for spiking inputs.\n    @attribute inhibitory true Indicates that this spiking input port is inhibitory.\n    @attribute excitatory true Indicates that this spiking input port is excitatory.\n\n    Grammar:\n        inputQualifier : ('inhibitory' | 'excitatory');\n\n    Attributes:\n        is_inhibitory = False\n        is_excitatory = False\n    "

    def __init__(self, is_inhibitory=False, is_excitatory=False, source_position=None):
        """
        Standard constructor.
        :param is_inhibitory: is inhibitory buffer.
        :type is_inhibitory: bool
        :param is_excitatory: is excitatory buffer.
        :type is_excitatory: book
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTInputQualifier, self).__init__(source_position)
        self.is_excitatory = is_excitatory
        self.is_inhibitory = is_inhibitory

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
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTInputQualifier):
            return False
        return self.is_excitatory == other.is_excitatory and self.is_inhibitory == other.is_inhibitory