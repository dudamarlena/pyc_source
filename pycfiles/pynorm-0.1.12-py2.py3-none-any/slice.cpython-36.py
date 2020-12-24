# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/slice.py
# Compiled at: 2019-03-28 07:58:10
# Size of source mod 2**32: 1594 bytes
from norm.executable import NormExecutable
from norm.executable.expression import NormExpression

class SliceExpr(NormExpression):

    def __init__(self, expr, start, end):
        super().__init__()
        self.expr = expr
        self.start = start
        self.end = end

    def compile(self, context):
        self.expr = self.expr.compile(context)
        from norm.executable.schema.variable import VariableName
        from norm.executable.expression.evaluation import EvaluationExpr
        if isinstance(self.expr, VariableName):
            self.expr = EvaluationExpr(args=[], variable=(self.expr)).compile(context)
        return self

    def execute(self, context):
        df = self.expr.execute(context)
        df = df.iloc[self.start:self.end].reset_index(drop=True)
        return df


class EvaluatedSliceExpr(SliceExpr):

    def __init__(self, expr, expr_range):
        super().__init__(expr, 0, -1)
        self.expr_range = expr_range