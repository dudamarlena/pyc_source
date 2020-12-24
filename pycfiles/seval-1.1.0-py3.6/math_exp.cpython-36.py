# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\seval\math_exp.py
# Compiled at: 2019-06-17 08:41:17
# Size of source mod 2**32: 852 bytes
import ast, typing
from .evalable import Evalable

class MathExp(Evalable):
    ALLOWED_NODES = (
     ast.Num,
     ast.UnaryOp,
     ast.UAdd,
     ast.USub,
     ast.Invert,
     ast.BinOp,
     ast.Add,
     ast.Sub,
     ast.Mult,
     ast.Div,
     ast.FloorDiv,
     ast.Mod,
     ast.Pow,
     ast.LShift,
     ast.RShift,
     ast.BitAnd,
     ast.BitOr,
     ast.BitXor)

    def __init__(self, expr: typing.Union[(str, ast.Expression)]):
        if isinstance(expr, str):
            expr = self.compile(expr, expected=(ast.Expression))
        elif not isinstance(expr, ast.Expression):
            raise AssertionError
        self.expr = expr

    def evalable(self):
        return (self.allowed_nodes)(self.expr.body, *self.ALLOWED_NODES)