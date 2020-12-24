# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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