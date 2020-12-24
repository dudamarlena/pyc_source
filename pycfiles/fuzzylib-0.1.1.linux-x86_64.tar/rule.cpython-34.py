# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzylib/rule.py
# Compiled at: 2015-09-29 17:24:14
# Size of source mod 2**32: 977 bytes
from collections import OrderedDict

class Rule:

    def __init__(self, antecedent, consequent):
        self._antecedent = antecedent
        self._consequent = consequent
        self._varValues = OrderedDict()

    def set_value(self, varname, value):
        self._varValues[varname] = value

    def get_antecedent(self):
        return self._antecedent

    def get_consequent(self):
        return self._consequent

    def eval_antecedent(self):
        eval_stack = []
        for x in self._antecedent:
            if type(x) == tuple:
                value = self._varValues[x[0]]
                function = x[1]
                eval_stack.append(function(value))
            elif callable(x):
                op1 = eval_stack.pop()
                op2 = eval_stack.pop()
                eval_stack.append(x(op1, op2))
                continue

        return eval_stack[0]