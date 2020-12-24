# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/pylp/expression.py
# Compiled at: 2019-07-03 20:43:27
# Size of source mod 2**32: 5456 bytes
"""
Contains functionality for dealing with expressions.

Exports:
    >>> from pylp.expression import Expression
"""
from contextlib import suppress
from typing import Iterable, List
from pylp.constraint import Constraint

class Expression:
    __doc__ = '\n    Represents an expression in a linear programming problem.\n\n    Notes:\n        A list of operands is given in order to reduce the height of the\n        expression tree.\n\n        Normally, an operator operates on two operands. Thus the expression:\n            5 + 5 + 5\n        can be represented as a tree:\n            +\n           /          5  +\n            /            5   5\n\n        But as the expression gets longer, a naive approach would result in\n        a very tall tree. In order to evaluate the tree, we would have to\n        traverse all the way to its leafs, which at its deepest part would\n        probably result in a stack overflow (maximum recursion error).\n\n        But treating the operands as a list, results in a nicer tree:\n           +\n         / |         5  5  5\n\n        And this tree stays at the same height the more operands it holds.\n\n        This prevents a stack overflow from occurring. This also results in\n        better performance as well.\n    '

    def __init__(self, operator: str, operands: list) -> None:
        """
        Create a new expression for the given operator and operands.

        Args:
            operator: The str of the operator
            operands: A list of operands
        """
        self.operator = operator
        self.arguments = []
        self._set_arguments(operands)

    def _set_arguments(self, arguments: list) -> None:
        for arg in arguments:
            if isinstance(arg, Expression) and self.is_same_type(arg):
                self.arguments += arg.arguments
            else:
                self.arguments += [arg]

    def is_same_type(self, other: 'Expression') -> bool:
        """Return True if the other expression is of the same type."""
        return self.operator == other.operator

    def __str__(self) -> str:
        arguments = (str(arg) for arg in self.arguments)
        expression = f" {self.operator} ".join(arguments)
        return f"({expression})"

    def __le__(self, other) -> Constraint:
        return Constraint(self, '<=', other)

    def __ge__(self, other) -> Constraint:
        return Constraint(self, '>=', other)

    def __eq__(self, other) -> Constraint:
        return Constraint(self, '==', other)

    def __ne__(self, other) -> Constraint:
        raise TypeError('Cannot have != in linear programming.')

    def __lt__(self, other) -> Constraint:
        return Constraint(self, '<', other)

    def __gt__(self, other) -> Constraint:
        return Constraint(self, '>', other)

    def __sub__(self, other) -> 'Expression':
        return Expression('-', [self, other])

    def __rsub__(self, other) -> 'Expression':
        return Expression('-', [other, self])

    def __add__(self, other) -> 'Expression':
        return Expression('+', [self, other])

    def __radd__(self, other) -> 'Expression':
        return Expression('+', [other, self])

    def __mul__(self, other) -> 'Expression':
        return Expression('*', [self, other])

    def __rmul__(self, other) -> 'Expression':
        return Expression('*', [other, self])

    def __neg__(self) -> 'Expression':
        return Expression('*', [-1, self])

    def __truediv__(self, other) -> 'Expression':
        return Expression('*', [self, 1 / other])

    def __rtruediv__(self, other):
        raise TypeError('Cannot divide by a variable in linear programming.')

    def _handle(self, arguments):
        return {'+':lambda : self._handle_add(arguments), 
         '*':lambda : self._handle_multiplication(arguments), 
         '-':lambda : self._handle_subtraction(arguments)}[self.operator]()

    @staticmethod
    def _handle_add(arguments: Iterable['Expression']):
        result = 0
        for arg in arguments:
            result += arg

        return result

    @staticmethod
    def _handle_subtraction(arguments: List['Expression']):
        result = arguments[0]
        for arg in arguments[1:]:
            result -= arg

        return result

    @staticmethod
    def _handle_multiplication(arguments: Iterable['Expression']):
        result = 1
        for arg in arguments:
            result *= arg

        return result

    def evaluate(self):
        """Evaluate the expression."""
        arguments = []
        for arg in self.arguments:
            with suppress(AttributeError):
                arg = arg.evaluate()
            arguments.append(arg)

        try:
            return self._handle(arguments)
        except KeyError:
            raise ValueError(f"Using unsupported operator: {self.operator}")

    def construct(self):
        """Build the expression for use in the solver."""
        arguments = []
        for arg in self.arguments:
            with suppress(AttributeError):
                arg = arg.construct()
            arguments.append(arg)

        try:
            return self._handle(arguments)
        except KeyError:
            raise ValueError(f"Using unsupported operator: {self.operator}")