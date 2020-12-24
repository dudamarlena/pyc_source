# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/visitors/ast_higher_order_visitor.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1771 bytes
from pynestml.visitors.ast_visitor import ASTVisitor

class ASTHigherOrderVisitor(ASTVisitor):
    __doc__ = '\n    This visitor is used to visit each node of the meta_model and and preform an arbitrary on it..\n    '

    def __init__(self, visit_funcs=list(), endvisit_funcs=list()):
        self.visit_funcs = list()
        self.endvisit_funcs = list()
        super(ASTHigherOrderVisitor, self).__init__()
        if isinstance(visit_funcs, list):
            self.visit_funcs.extend(visit_funcs)
        else:
            if callable(visit_funcs):
                self.visit_funcs.append(visit_funcs)
            if isinstance(endvisit_funcs, list):
                self.endvisit_funcs.extend(endvisit_funcs)
            elif callable(endvisit_funcs):
                self.endvisit_funcs.append(endvisit_funcs)

    def visit(self, node):
        for fun in self.visit_funcs:
            fun(node)

    def endvisit(self, node):
        for fun in self.endvisit_funcs:
            fun(node)