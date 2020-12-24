# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/code.py
# Compiled at: 2019-03-14 23:15:58
# Size of source mod 2**32: 349 bytes
from norm.executable.expression import NormExpression

class CodeExpr(NormExpression):

    def __init__(self, code):
        super().__init__()
        self.code = code

    def serialize(self):
        pass