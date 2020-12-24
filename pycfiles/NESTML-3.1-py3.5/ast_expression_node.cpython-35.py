# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/meta_model/ast_expression_node.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1682 bytes
from abc import ABCMeta
from copy import copy
from pynestml.meta_model.ast_node import ASTNode

class ASTExpressionNode(ASTNode):
    __doc__ = '\n    This class is not a part of the grammar but is used to store commonalities of all possible meta_model classes, e.g.,\n    the source position. This class is abstract, thus no instances can be created.\n    '
    _ASTExpressionNode__type = None
    _ASTExpressionNode__typeEither = None
    __metaclass__ = ABCMeta

    def __init__(self, source_position, scope=None):
        super(ASTExpressionNode, self).__init__(source_position, scope)

    @property
    def type(self):
        from pynestml.visitors.ast_expression_type_visitor import ASTExpressionTypeVisitor
        if self._ASTExpressionNode__type is None:
            self.accept(ASTExpressionTypeVisitor())
        return copy(self._ASTExpressionNode__type)

    @type.setter
    def type(self, _value):
        self._ASTExpressionNode__type = _value

    def get_parent(self, ast):
        pass

    def equals(self, other):
        pass