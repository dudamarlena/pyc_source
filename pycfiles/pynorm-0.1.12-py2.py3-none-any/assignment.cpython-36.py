# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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