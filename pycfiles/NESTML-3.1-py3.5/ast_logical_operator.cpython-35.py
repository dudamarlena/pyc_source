# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_logical_operator.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2513 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTLogicalOperator(ASTNode):
    __doc__ = "\n    This class is used to store a single logical operator.\n    Grammar:\n        logicalOperator : (logicalAnd='and' | logicalOr='or');\n    Attributes:\n        is_logical_and = False\n        is_logical_or = False\n    "

    def __init__(self, is_logical_and=False, is_logical_or=False, source_position=None):
        """
        Standard constructor.
        :param is_logical_and: is logical and.
        :type is_logical_and: bool
        :param is_logical_or: is logical or.
        :type is_logical_or: bool
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        assert is_logical_and ^ is_logical_or, '(PyNestML.AST.LogicalOperator) Logical operator not correctly specified!'
        super(ASTLogicalOperator, self).__init__(source_position)
        self.is_logical_and = is_logical_and
        self.is_logical_or = is_logical_or

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
        if not isinstance(other, ASTLogicalOperator):
            return False
        return self.is_logical_and == other.is_logical_and and self.is_logical_or == other.is_logical_or