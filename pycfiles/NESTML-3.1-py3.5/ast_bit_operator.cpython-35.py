# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_bit_operator.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3189 bytes
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_source_location import ASTSourceLocation

class ASTBitOperator(ASTNode):
    __doc__ = "\n    This class is used to store a single bit operator.\n    Grammar:\n        bitOperator : (bitAnd='&'| bitXor='^' | bitOr='|' | bitShiftLeft='<<' | bitShiftRight='>>');\n    Attributes:\n        is_bit_and = False\n        is_bit_xor = False\n        is_bit_or = False\n        is_bit_shift_left = False\n        is_bit_shift_right = False\n    "

    def __init__(self, is_bit_and=False, is_bit_xor=False, is_bit_or=False, is_bit_shift_left=False, is_bit_shift_right=False, source_position=None):
        """
        Standard constructor.
        :param source_position: the position of the element in the source
        :type source_position: ASTSourceLocation
        :param is_bit_and: is bit and operator.
        :type is_bit_and: bool
        :param is_bit_xor: is bit xor operator.
        :type is_bit_xor: bool
        :param is_bit_or: is bit or operator.
        :type is_bit_or: bool
        :param is_bit_shift_left: is bit shift left operator.
        :type is_bit_shift_left: bool
        :param is_bit_shift_right: is bit shift right operator.
        :type is_bit_shift_right: bool
        """
        super(ASTBitOperator, self).__init__(source_position)
        self.is_bit_shift_right = is_bit_shift_right
        self.is_bit_shift_left = is_bit_shift_left
        self.is_bit_or = is_bit_or
        self.is_bit_xor = is_bit_xor
        self.is_bit_and = is_bit_and

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
        if not isinstance(other, ASTBitOperator):
            return False
        return self.is_bit_and == other.is_bit_and and self.is_bit_or == other.is_bit_or and self.is_bit_xor == other.is_bit_xor and self.is_bit_shift_left == self.is_bit_shift_left and self.is_bit_shift_right == other.is_bit_shift_right