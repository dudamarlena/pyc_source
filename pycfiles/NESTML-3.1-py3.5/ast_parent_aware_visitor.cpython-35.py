# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_parent_aware_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1391 bytes
from pynestml.utils.stack import Stack
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTParentAwareVisitor(ASTVisitor):
    __doc__ = '\n    The parent aware visitor storing a trace. This visitor enables a given visitor to inspect the corresponding\n    parent node.\n    Attributes:\n        parents type(Stack): A stack containing the predecessor of this node.\n    '

    def __init__(self):
        super(ASTParentAwareVisitor, self).__init__()
        self.parents = Stack()

    def handle(self, _node):
        self.visit(_node)
        self.parents.push(_node)
        self.traverse(_node)
        self.parents.pop()
        self.endvisit(_node)