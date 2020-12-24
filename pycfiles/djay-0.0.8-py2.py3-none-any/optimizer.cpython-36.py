# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/jinja2/jinja2/optimizer.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 1722 bytes
"""
    jinja2.optimizer
    ~~~~~~~~~~~~~~~~

    The jinja optimizer is currently trying to constant fold a few expressions
    and modify the AST in place so that it should be easier to evaluate it.

    Because the AST does not contain all the scoping information and the
    compiler has to find that out, we cannot do all the optimizations we
    want.  For example loop unrolling doesn't work because unrolled loops would
    have a different scoping.

    The solution would be a second syntax tree that has the scoping rules stored.

    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD.
"""
from jinja2 import nodes
from jinja2.visitor import NodeTransformer

def optimize(node, environment):
    """The context hint can be used to perform an static optimization
    based on the context given."""
    optimizer = Optimizer(environment)
    return optimizer.visit(node)


class Optimizer(NodeTransformer):

    def __init__(self, environment):
        self.environment = environment

    def fold(self, node, eval_ctx=None):
        """Do constant folding."""
        node = self.generic_visit(node)
        try:
            return nodes.Const.from_untrusted((node.as_const(eval_ctx)), lineno=(node.lineno),
              environment=(self.environment))
        except nodes.Impossible:
            return node

    visit_Add = visit_Sub = visit_Mul = visit_Div = visit_FloorDiv = visit_Pow = visit_Mod = visit_And = visit_Or = visit_Pos = visit_Neg = visit_Not = visit_Compare = visit_Getitem = visit_Getattr = visit_Call = visit_Filter = visit_Test = visit_CondExpr = fold
    del fold