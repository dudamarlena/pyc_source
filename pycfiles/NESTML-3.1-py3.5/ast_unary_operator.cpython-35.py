# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_unary_operator.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2821 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTUnaryOperator(ASTNode):
    __doc__ = "\n    This class is used to store a single unary operator, e.g., ~.\n    Grammar:\n        unaryOperator : (unaryPlus='+' | unaryMinus='-' | unaryTilde='~');\n    Attributes:\n        is_unary_plus = False\n        is_unary_minus = False\n        is_unary_tilde = False\n    "

    def __init__(self, is_unary_plus=False, is_unary_minus=False, is_unary_tilde=False, source_position=None):
        """
        Standard constructor.
        :param is_unary_plus: is a unary plus.
        :type is_unary_plus: bool
        :param is_unary_minus: is a unary minus.
        :type is_unary_minus: bool
        :param is_unary_tilde: is a unary tilde.
        :type is_unary_tilde: bool
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        assert is_unary_tilde + is_unary_minus + is_unary_plus == 1, '(PyNestML.AST.UnaryOperator) Type of unary operator not correctly specified!'
        super(ASTUnaryOperator, self).__init__(source_position)
        self.is_unary_plus = is_unary_plus
        self.is_unary_minus = is_unary_minus
        self.is_unary_tilde = is_unary_tilde

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
        if not isinstance(other, ASTUnaryOperator):
            return False
        return self.is_unary_minus == other.is_unary_minus and self.is_unary_plus == other.is_unary_plus and self.is_unary_tilde == other.is_unary_tilde