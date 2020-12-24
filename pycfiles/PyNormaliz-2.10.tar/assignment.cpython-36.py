# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/work/supernorm/norm/executable/expression/assignment.py
# Compiled at: 2019-02-27 21:40:16
# Size of source mod 2**32: 680 bytes
from norm.executable.expression import NormExpression
from norm.executable.variable import VariableName

class AssignmentExpr(NormExpression):

    def __init__(self, variable, expr):
        super().__init__()
        self.variable = variable
        self.expr = expr

    def serialize(self):
        pass

    def execute(self, context):
        pass