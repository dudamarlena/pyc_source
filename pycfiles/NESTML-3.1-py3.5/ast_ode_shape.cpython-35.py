# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_ode_shape.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3013 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTOdeShape(ASTNode):
    __doc__ = "\n    This class is used to store shapes. \n    Grammar:\n        odeShape : 'shape' lhs=variable '=' rhs=expr;\n    Attributes:\n        lhs = None\n        rhs = None\n    "

    def __init__(self, lhs, rhs, source_position):
        """
        Standard constructor of ASTOdeShape.
        :param lhs: the variable corresponding to the shape
        :type lhs: ast_variable
        :param rhs: the right-hand side rhs
        :type rhs: ast_expression or ast_simple_expression
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTOdeShape, self).__init__(source_position)
        self.lhs = lhs
        self.rhs = rhs

    def get_variable(self):
        """
        Returns the variable of the left-hand side.
        :return: the variable
        :rtype: ast_variable
        """
        return self.lhs

    def get_expression(self):
        """
        Returns the right-hand side rhs.
        :return: the rhs
        :rtype: ast_expression
        """
        return self.rhs

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.get_variable() is ast:
            return self
        if self.get_variable().get_parent(ast) is not None:
            return self.get_variable().get_parent(ast)
        if self.get_expression() is ast:
            return self
        if self.get_expression().get_parent(ast) is not None:
            return self.get_expression().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTOdeShape):
            return False
        return self.get_variable().equals(other.get_variable()) and self.get_expression().equals(other.get_expression())