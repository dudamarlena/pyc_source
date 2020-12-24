# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_block.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3679 bytes
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_source_location import ASTSourceLocation

class ASTBlock(ASTNode):
    __doc__ = '\n    This class is used to store a single block of declarations, i.e., statements.\n    Grammar:\n        block : ( smallStmt | compoundStmt | NEWLINE )*;\n    Attribute:\n        stmts = None\n    '

    def __init__(self, _stmts=list(), source_position=None):
        """
        Standard constructor.
        :param _stmts: a list of statements 
        :type _stmts: list(ASTSmallStmt/ASTCompoundStmt)
        :param source_position: the position of this element
        :type source_position: ASTSourceLocation
        """
        from pynestml.meta_model.ast_stmt import ASTStmt
        assert _stmts is not None and isinstance(_stmts, list), '(PyNestML.AST.Bloc) No or wrong type of statements provided (%s)!' % type(_stmts)
        for stmt in _stmts:
            if not (stmt is not None and isinstance(stmt, ASTStmt)):
                raise AssertionError('(PyNestML.AST.Bloc) No or wrong type of statement provided (%s)!' % type(stmt))

        super(ASTBlock, self).__init__(source_position)
        self.stmts = _stmts

    def get_stmts(self):
        """
        Returns the list of statements.
        :return: list of stmts.
        :rtype: list(ASTSmallStmt/ASTCompoundStmt)
        """
        return self.stmts

    def add_stmt(self, stmt):
        """
        Adds a single statement to the list of statements.
        :param stmt: a statement
        :type stmt: ASTSmallStmt,ASTCompoundStmt
        """
        self.stmts.append(stmt)

    def delete_stmt(self, stmt):
        """
        Deletes the handed over statement.
        :param stmt:
        :type stmt:
        :return: True if deleted, otherwise False.
        :rtype: bool
        """
        self.stmts.remove(stmt)

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        for stmt in self.get_stmts():
            if stmt is ast:
                return self
            if stmt.get_parent(ast) is not None:
                return stmt.get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTBlock):
            return False
        if len(self.get_stmts()) != len(other.get_stmts()):
            return False
        my_stmt = self.get_stmts()
        your_stmts = other.get_stmts()
        for i in range(0, len(self.get_stmts())):
            if not my_stmt[i].equals(your_stmts[i]):
                return False

        return True