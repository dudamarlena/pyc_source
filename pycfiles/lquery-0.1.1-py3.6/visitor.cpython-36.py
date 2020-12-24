# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\lquery\expr\visitor.py
# Compiled at: 2018-08-03 17:34:44
# Size of source mod 2**32: 1827 bytes
from .core import ValueExpr, AttrExpr, Make

class ExprVisitor:

    def visit(self, expr):
        return expr

    def visit_attr_expr(self, expr):
        return expr

    def visit_index_expr(self, expr):
        return expr

    def visit_call_expr(self, expr):
        return expr

    def visit_binary_expr(self, expr):
        return expr

    def visit_func_expr(self, expr):
        return expr


class DefaultExprVisitor(ExprVisitor):

    def visit_attr_expr(self, expr):
        src_expr = expr.expr.accept(self)
        if src_expr is expr.expr:
            return expr
        else:
            return Make.attr(src_expr, expr.name)

    def visit_index_expr(self, expr):
        src_expr = expr.expr.accept(self)
        key_expr = expr.key.accept(self)
        if src_expr is expr.expr:
            if key_expr is expr.key:
                return expr
        return Make.attr(src_expr, expr.name)

    def visit_call_expr(self, expr):
        if expr.func is getattr:
            if len(expr.args) == 2:
                if not expr.kwargs:
                    attr_expr = expr.args[1]
                    if isinstance(attr_expr, ValueExpr):
                        if isinstance(attr_expr.value, str):
                            return Make.attr(expr.args[0], attr_expr.value)
        return expr

    def visit_binary_expr(self, expr):
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        if left is expr.left:
            if right is expr.right:
                return expr
        return Make.binary_op(left, right, expr.op)

    def visit_func_expr(self, expr):
        body = expr.body.accept(self)
        if body is not expr.body:
            return (Make.func)(body, *expr.args)
        else:
            return expr