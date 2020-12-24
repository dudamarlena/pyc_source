# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/query.py
# Compiled at: 2019-04-30 03:35:19
# Size of source mod 2**32: 4431 bytes
from collections import OrderedDict
from norm.executable import NormError
from norm.executable.constant import ListConstant, Constant
from norm.executable.expression import NormExpression
from norm.executable.expression.argument import ArgumentExpr
from norm.executable.expression.condition import ConditionExpr, CombinedConditionExpr
from norm.executable.expression.evaluation import EvaluationExpr, AddDataEvaluationExpr
from norm.grammar.literals import LOP
import logging
logger = logging.getLogger(__name__)

class QueryExpr(NormExpression):

    def __init__(self, op, expr1, expr2):
        super().__init__()
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2

    def __combine_value(self, value1, value2):
        if value1 is None or value2 is None:
            return
        elif isinstance(value1, ListConstant):
            if isinstance(value2, ListConstant):
                value1.value.extend(value2.value)
                return value1
            else:
                if isinstance(value1, ListConstant):
                    if isinstance(value2, Constant):
                        value1.value.append(value2.value)
                        return value1
                if isinstance(value1, Constant):
                    if isinstance(value2, ListConstant):
                        value2.value.append(value1.value)
                        return value2
                if isinstance(value1, Constant):
                    if isinstance(value2, Constant):
                        return ListConstant(value1.type_, [value1.value, value2.value])
        else:
            if isinstance(value1, AddDataEvaluationExpr):
                if isinstance(value2, AddDataEvaluationExpr):
                    if value1.lam is value2.lam:
                        combined = self._QueryExpr__combine_data(value1.data, value2.data)
                        if combined is not None:
                            value1.data = combined
                            return value1

    def __combine_data(self, data1, data2):
        cols = list(data1.keys())
        cols.extend(col for col in data2.keys() if col not in data1.keys())
        data = OrderedDict()
        for col in cols:
            combined = self._QueryExpr__combine_value(data1.get(col), data2.get(col))
            if combined is None:
                return
            data[col] = combined

        return data

    def compile(self, context):
        if isinstance(self.expr1, AddDataEvaluationExpr):
            if isinstance(self.expr2, AddDataEvaluationExpr):
                if self.expr1.lam is self.expr2.lam:
                    combined = self._QueryExpr__combine_data(self.expr1.data, self.expr2.data)
                    if combined is not None:
                        self.expr1.data = combined
                        return self.expr1
        if isinstance(self.expr1, ConditionExpr):
            if isinstance(self.expr2, ConditionExpr):
                return CombinedConditionExpr(self.op, self.expr1, self.expr2).compile(context)
        return self

    def execute(self, context):
        df1 = self.expr1.execute(context)
        df2 = self.expr2.execute(context)
        return df2


class NegatedQueryExpr(NormExpression):

    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def compile(self, context):
        if isinstance(self.expr, QueryExpr):
            self.expr.expr1 = NegatedQueryExpr(self.expr.expr1).compile(context)
            self.expr.expr2 = NegatedQueryExpr(self.expr.expr2).compile(context)
            self.expr.op = self.expr.op.negate()
        else:
            if isinstance(self.expr, ConditionExpr):
                self.expr.op = self.expr.op.negate()
            else:
                msg = 'Currently NOT only works on logically combined query or conditional query'
                logger.error(msg)
                raise NotImplementedError(msg)
        return self.expr

    def execute(self, context):
        msg = 'Negated query is not executable, but only compilable'
        logger.error(msg)
        raise NormError(msg)