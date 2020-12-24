# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_if_stmt.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 5043 bytes
from pynestml.meta_model.ast_node import ASTNode

class ASTIfStmt(ASTNode):
    __doc__ = '\n    This class is used to store a single if block.\n    Grammar:\n        ifStmt : ifClause\n                    elifClause*\n                    (elseClause)?\n                    BLOCK_CLOSE;\n    Attributes:\n        if_clause = None\n        elif_clauses = None\n        else_clause = None\n    '

    def __init__(self, if_clause, elif_clauses=list(), else_clause=None, source_position=None):
        """
        Standard construcotr.
        :param if_clause: the if-clause
        :type if_clause: ast_if_clause
        :param elif_clauses: (optional) list of elif clauses
        :type elif_clauses: ast_elif_clause
        :param else_clause: (optional) else clause
        :type else_clause: ast_else_clause
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        if not elif_clauses is None:
            assert isinstance(elif_clauses, list), '(PyNestML.AST.IfStmt) Wrong type of elif-clauses provided (%s)!' % type(elif_clauses)
            super(ASTIfStmt, self).__init__(source_position)
            self.else_clause = else_clause
            self.if_clause = if_clause
            self.elif_clauses = elif_clauses

    def get_if_clause(self):
        """
        Returns the if-clause.
        :return: the if clause
        :rtype: ASTfClause
        """
        return self.if_clause

    def has_elif_clauses(self):
        """
        Returns whether object contains elif clauses.
        :return: True if at leas one elif clause, False else.
        :rtype: bool
        """
        return len(self.elif_clauses) > 0

    def get_elif_clauses(self):
        """
        Returns a list of elif-clauses.
        :return: a list of elif-clauses.
        :rtype: list(ASTElifClause)
        """
        return self.elif_clauses

    def has_else_clause(self):
        """
        Returns whether object contains elif clauses.
        :return: True if object contains an else-clause, False else.
        :rtype: bool
        """
        return self.else_clause is not None

    def get_else_clause(self):
        """
        Returns the else-clause.
        :return: the else-clause.
        :rtype: ast_else_clause
        """
        return self.else_clause

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.get_if_clause() is ast:
            return self
        if self.get_if_clause().get_parent(ast) is not None:
            return self.get_if_clause().get_parent(ast)
        for elifClause in self.get_elif_clauses():
            if elifClause is ast:
                return self
            if elifClause.get_parent(ast) is not None:
                return elifClause.get_parent(ast)

        if self.has_else_clause():
            if self.get_else_clause() is ast:
                return self
            if self.get_else_clause().get_parent(ast) is not None:
                pass
            return self.get_else_clause().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equals, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTIfStmt):
            return False
        if not self.get_if_clause().equals(other.get_if_clause()):
            return False
        if len(self.get_elif_clauses()) != len(other.get_elif_clauses()):
            return False
        my_elif_clauses = self.get_elif_clauses()
        your_elif_clauses = other.get_elif_clauses()
        for i in range(0, len(my_elif_clauses)):
            if not my_elif_clauses[i].equals(your_elif_clauses[i]):
                return False

        if self.has_else_clause() + other.has_else_clause() == 1:
            return False
        if self.has_else_clause() and other.has_else_clause() and not self.get_else_clause().equals(other.get_else_clause()):
            return False
        return True