# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_return_stmt.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3090 bytes
from pynestml.meta_model.ast_expression import ASTExpression
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_simple_expression import ASTSimpleExpression

class ASTReturnStmt(ASTNode):
    __doc__ = "\n    This class is used to store a return statement.\n        A ReturnStmt Models the return statement in a function.\n        @attribute minus An optional sing\n        @attribute definingVariable Name of the variable\n        Grammar:\n            returnStmt : 'return' expr?;\n    Attributes:\n          expression (ASTSimpleExpression or ASTExpression): An rhs representing the returned value.\n    "

    def __init__(self, expression=None, source_position=None):
        """
        Standard constructor.
        :param expression: an rhs.
        :type expression: ASTExpression
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTReturnStmt, self).__init__(source_position)
        self.expression = expression

    def has_expression(self):
        """
        Returns whether the return statement has an rhs or not.
        :return: True if has rhs, otherwise False.
        :rtype: bool
        """
        return self.expression is not None

    def get_expression(self):
        """
        Returns the rhs.
        :return: an rhs.
        :rtype: ASTExpression
        """
        return self.expression

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.has_expression():
            if self.get_expression() is ast:
                return self
            if self.get_expression().get_parent(ast) is not None:
                pass
            return self.get_expression().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTReturnStmt):
            return False
        return self.get_expression().equals(other.get_expression())