# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\extras\_common_visitor.py
# Compiled at: 2018-08-03 15:00:40
# Size of source mod 2**32: 570 bytes
from ..expr import Make, AttrExpr
from ..expr.visitor import DefaultExprVisitor

class DbExprVisitor(DefaultExprVisitor):
    __doc__ = '\n    provide many method for rewrite expr, but you need to manual call it.\n    '

    def rewrite_attr_expr_to_index_expr(self, expr: AttrExpr):
        """
        rewrite `expr.name` => `expr['name']`
        """
        return Make.index(expr.expr, Make.const(expr.name))