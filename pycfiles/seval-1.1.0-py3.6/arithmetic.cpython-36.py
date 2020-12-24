# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\seval\arithmetic.py
# Compiled at: 2019-06-19 14:25:54
# Size of source mod 2**32: 2149 bytes
import ast
from .evalable import Evalable

class Arithmetic(metaclass=Evalable, evalable_nodes=(
 ast.Num,
 ast.UnaryOp,
 ast.BinOp)):
    _NUM_TYPES = (
     int,
     float,
     complex)

    @classmethod
    def num(cls, node: ast.Num):
        yield node.n

    @classmethod
    def unaryop(cls, node: ast.UnaryOp):
        yield node.operand
        operand = yield
        if not isinstance(operand, cls._NUM_TYPES):
            raise ValueError('unsupported operand type')
        if isinstance(node.op, ast.UAdd):
            yield +operand
        else:
            if isinstance(node.op, ast.USub):
                yield -operand
            else:
                if isinstance(node.op, complex):
                    raise ValueError('unsupported operand for complex type')
                yield ~operand

    @classmethod
    def binop(cls, node: ast.BinOp):
        yield node.left
        left = yield
        yield node.right
        right = yield
        if not isinstance(left, cls._NUM_TYPES) or not isinstance(right, cls._NUM_TYPES):
            raise ValueError('unsupported type')
        else:
            op = node.op
            if isinstance(op, ast.Add):
                yield left + right
            else:
                if isinstance(op, ast.Sub):
                    yield left - right
                else:
                    if isinstance(op, ast.Mult):
                        yield left * right
                    else:
                        if isinstance(op, ast.Div):
                            yield left / right
                        else:
                            if isinstance(op, ast.FloorDiv):
                                yield left // right
                            else:
                                if isinstance(op, ast.Mod):
                                    yield left % right
                                else:
                                    if isinstance(op, ast.Pow):
                                        yield left ** right
                                    else:
                                        if isinstance(op, ast.LShift):
                                            yield left << right
                                        else:
                                            if isinstance(op, ast.RShift):
                                                yield left >> right
                                            else:
                                                if isinstance(op, ast.BitAnd):
                                                    yield left & right
                                                else:
                                                    if isinstance(op, ast.BitOr):
                                                        yield left | right
                                                    else:
                                                        yield left ^ right