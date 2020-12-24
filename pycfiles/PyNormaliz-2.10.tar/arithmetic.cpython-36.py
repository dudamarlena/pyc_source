# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/arithmetic.py
# Compiled at: 2019-05-21 17:25:19
# Size of source mod 2**32: 3005 bytes
import uuid
from norm.grammar.literals import AOP
from norm.executable import NormError
from norm.executable.expression import NormExpression
from norm.executable.expression.evaluation import EvaluationExpr
import logging
logger = logging.getLogger(__name__)

class ArithmeticExpr(NormExpression):

    def __init__(self, op, expr1, expr2=None, projection=None):
        """
        Arithmetic expression
        :param op: the operation, e.g., [+, -, *, /, %, **]
        :type op: AOP
        :param expr1: left expression
        :type expr1: ArithmeticExpr
        :param expr2: right expression
        :type expr2: ArithmeticExpr
        """
        super().__init__()
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2
        self.projection = projection
        self._projection_name = None
        if not self.op is not None:
            raise AssertionError
        elif not self.expr2 is not None:
            raise AssertionError
        self._exprstr = None

    def __str__(self):
        if self._exprstr is None:
            msg = 'Compile the expression first'
            logger.error(msg)
            raise NormError(msg)
        return self._exprstr

    def compile(self, context):
        if self.expr1:
            if isinstance(self.expr1, EvaluationExpr):
                if self.expr1.variable is None:
                    if len(self.expr1.args) == 1:
                        self.expr1 = self.expr1.args[0].expr
                if isinstance(self.expr2, EvaluationExpr):
                    if self.expr2.variable is None:
                        if len(self.expr2.args) == 1:
                            self.expr2 = self.expr2.args[0].expr
            else:
                if self.op is AOP.SUB and self.expr1 is None:
                    self._exprstr = '-({})'.format(self.expr2)
            self._exprstr = '({}) {} ({})'.format(self.expr1, self.op, self.expr2)
        else:
            self.eval_lam = context.scope
            from norm.models import Lambda, Variable, lambdas
            if self.projection:
                if self.projection.num > 0:
                    self._projection_name = self.projection.variables[0].name
            self._projection_name = Lambda.VAR_OUTPUT
        self.lam = Lambda((context.context_namespace), (context.TMP_VARIABLE_STUB + str(uuid.uuid4())), variables=[
         Variable(self._projection_name, lambdas.Any)])
        self.lam.cloned_from = self.eval_lam
        return self

    def execute(self, context):
        df = self.eval_lam.data.eval(self._exprstr)
        if self.projection:
            if self.projection.num > 0:
                from pandas import DataFrame, Series
                if isinstance(df, DataFrame):
                    raise NormError('cant be here')
                    self.data = df.renames({old_name:new_var.name for old_name, new_var in zip(df.columns, self.projection.variables)})
        elif not isinstance(df, Series):
            raise AssertionError
        self.lam.data = DataFrame({self._projection_name: df})
        return self.lam.data