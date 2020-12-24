# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/argument.py
# Compiled at: 2019-05-08 19:49:18
# Size of source mod 2**32: 2495 bytes
from norm.grammar.literals import COP
from norm.executable import Projection
from norm.executable.constant import Constant
from norm.executable.expression import NormExpression
from typing import Union
import logging
logger = logging.getLogger(__name__)

class ArgumentExpr(NormExpression):

    def __init__(self, variable=None, op=None, expr=None, projection=None):
        """
        The argument expression project to a new variable, either assigning or conditional.
        :param variable: the variable
        :type variable: VariableName
        :param expr: the arithmetic expression for the variable
        :type expr: Union[norm.executable.expression.arithmetic.ArithmeticExpr,
                          norm.executable.expression.slice.SliceExpr,
                          norm.executable.expression.evaluation.EvaluationExpr,
                          norm.executable.variable.VariableName]
        :param op: the conditional operation
        :type op: COP
        :param projection: the projection
        :type projection: Projection
        """
        super().__init__()
        from norm.executable.expression.arithmetic import ArithmeticExpr
        from norm.executable.expression.slice import SliceExpr
        from norm.executable.expression.evaluation import EvaluationExpr
        from norm.executable.schema.variable import VariableName
        self.variable = variable
        self.expr = expr
        self.op = op
        self.projection = projection

    def __str__(self):
        return '{} {} {} {}'.format(self.variable if self.variable is not None else '', self.op if self.op is not None else '', self.expr if self.expr is not None else '', self.projection if self.projection is not None else '')

    @property
    def is_constant(self):
        return isinstance(self.expr, Constant)

    @property
    def is_assign_operator(self):
        return self.op is None

    def compile(self, context):
        from norm.executable.expression.evaluation import EvaluationExpr
        from norm.executable.schema.variable import VariableName
        if self.is_assign_operator:
            if self.projection is not None:
                if isinstance(self.expr, VariableName):
                    self.expr = EvaluationExpr([], self.expr, self.projection).compile(context)
        return self