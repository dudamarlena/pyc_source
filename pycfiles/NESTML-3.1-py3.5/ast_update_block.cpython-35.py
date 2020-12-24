# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_update_block.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2706 bytes
from pynestml.meta_model.ast_block import ASTBlock
from pynestml.meta_model.ast_node import ASTNode

class ASTUpdateBlock(ASTNode):
    __doc__ = "\n    This class is used to store dynamic blocks.\n    ASTUpdateBlock is a special function definition:\n      update:\n        if r == 0: # not refractory\n          integrate(V)\n        end\n      end\n     @attribute block Implementation of the dynamics.\n   \n    Grammar:\n        updateBlock:\n            'update'\n            BLOCK_OPEN\n              block\n            BLOCK_CLOSE;\n    Attributes:\n        block = None\n    "

    def __init__(self, block, source_position):
        """
        Standard constructor.
        :param block: a block of definitions.
        :type block: ASTBlock
        :param source_position: the position of this element in the source file.
        :type source_position: ASTSourceLocation.
        """
        super(ASTUpdateBlock, self).__init__(source_position)
        self.block = block

    def get_block(self):
        """
        Returns the block of definitions.
        :return: the block
        :rtype: ast_block
        """
        return self.block

    def get_parent(self, ast):
        """
        Indicates whether a this node contains the handed over node.
        :param ast: an arbitrary meta_model node.
        :type ast: AST_
        :return: AST if this or one of the child nodes contains the handed over element.
        :rtype: AST_ or None
        """
        if self.get_block() is ast:
            return self
        if self.get_block().get_parent(ast) is not None:
            return self.get_block().get_parent(ast)

    def equals(self, other):
        """
        The equals method.
        :param other: a different object.
        :type other: object
        :return: True if equal, otherwise False.
        :rtype: bool
        """
        if not isinstance(other, ASTUpdateBlock):
            return False
        return self.get_block().equals(other.get_block())