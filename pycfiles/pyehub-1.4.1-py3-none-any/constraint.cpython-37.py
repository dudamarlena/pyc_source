# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/pylp/constraint.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 1513 bytes
__doc__ = '\nContains a class for a linear programming constraint.\n\nExports:\n    >>> from pylp.constraint import Constraint\n\n'
from contextlib import suppress

class Constraint:
    """Constraint"""

    def __init__(self, lhs, operator: str, rhs) -> None:
        """
        Create a new constraint between lhs and rhs.

        Args:
            lhs: The left-hand side of the constraint
            operator: The boolean operator as a str
            rhs: The right-hand side of the constraint
        """
        self._constraint = (
         lhs, operator, rhs)

    def __str__(self) -> str:
        lhs, operator, rhs = self._constraint
        return f"{lhs} {operator} {rhs}"

    @property
    def rhs(self):
        return self._constraint[2]

    @property
    def lhs(self):
        return self._constraint[0]

    @property
    def operator(self):
        return self._constraint[1]

    def construct(self):
        """Build the constraint for use in the solver."""
        lhs, operator, rhs = self._constraint
        with suppress(AttributeError):
            lhs = lhs.construct()
        with suppress(AttributeError):
            rhs = rhs.construct()
        return {'<=':lambda : lhs <= rhs, 
         '>=':lambda : lhs >= rhs, 
         '<':lambda : lhs < rhs, 
         '>':lambda : lhs > rhs, 
         '==':lambda : lhs == rhs}[operator]()