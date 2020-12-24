# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_ode_equation.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3294 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTOdeEquation(ASTNode):
    __doc__ = '\n    This class is used to store meta_model equations, e.g., V_m\' = 10mV + V_m.\n    ASTOdeEquation Represents an equation, e.g. "I = exp(t)" or represents an differential equations,\n     e.g. "V_m\' = V_m+1".\n    @attribute lhs      Left hand side, e.g. a Variable.\n    @attribute rhs      Expression defining the right hand side.\n    Grammar:\n        odeEquation : lhs=variable \'=\' rhs=rhs;\n    Attributes:\n        lhs = None\n        rhs = None\n    '

    def __init__(self, lhs, rhs, source_position=None):
        """
        Standard constructor.
        :param lhs: an object of type ASTVariable
        :type lhs: ast_variable
        :param rhs: an object of type ASTExpression.
        :type rhs: ast_expression or ast_simple_expression
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTOdeEquation, self).__init__(source_position)
        self.lhs = lhs
        self.rhs = rhs

    def get_lhs(self):
        """
        Returns the left-hand side of the equation.
        :return: an object of the meta_model-variable class.
        :rtype: ast_variable
        """
        return self.lhs

    def get_rhs(self):
        """
        Returns the left-hand side of the equation.
        :return: an object of the meta_model-expr class.
        :rtype: ast_expression
        """
        return self.rhs

    def get_parent(self, ast=None):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.get_lhs() is ast:
            return self
        if self.get_lhs().get_parent(ast) is not None:
            return self.get_lhs().get_parent(ast)
        if self.get_rhs() is ast:
            return self
        if self.get_rhs().get_parent(ast) is not None:
            return self.get_rhs().get_parent(ast)

    def equals(self, other=None):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTOdeEquation):
            return False
        return self.get_lhs().equals(other.get_lhs()) and self.get_rhs().equals(other.get_rhs())