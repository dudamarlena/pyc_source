# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_stmt.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2439 bytes
from pynestml.meta_model.ast_compound_stmt import ASTCompoundStmt
from pynestml.meta_model.ast_node import ASTNode
from pynestml.meta_model.ast_small_stmt import ASTSmallStmt

class ASTStmt(ASTNode):
    __doc__ = '\n    Stores a reference to either small or compound statement.\n    Grammar:\n        stmt : smallStmt | compoundStmt;\n    Attributes:\n        small_stmt = None\n        compound_stmt = None\n    '

    def __init__(self, small_stmt, compound_stmt, source_position):
        super(ASTStmt, self).__init__(source_position)
        self.small_stmt = small_stmt
        self.compound_stmt = compound_stmt

    def get_parent(self, ast=None):
        """
        Returns the parent node of a handed over AST object.
        """
        if self.small_stmt is ast:
            return self
        if self.small_stmt is not None and self.small_stmt.get_parent(ast) is not None:
            return self.small_stmt.get_parent(ast)
        if self.compound_stmt is ast:
            return self
        if self.compound_stmt is not None and self.compound_stmt.get_parent(ast) is not None:
            return self.compound_stmt.get_parent(ast)

    def is_small_stmt(self):
        return self.small_stmt is not None

    def is_compound_stmt(self):
        return self.compound_stmt is not None

    def equals(self, other=None):
        if not isinstance(other, ASTStmt):
            return False
        if self.is_small_stmt() and other.is_small_stmt():
            return self.small_stmt.equals(other.small_stmt)
        if self.is_compound_stmt() and other.is_compound_stmt():
            return self.compound_stmt.equals(other.compound_stmt)