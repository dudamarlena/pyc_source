# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/fuzzylib/fis.py
# Compiled at: 2015-09-29 17:24:14
# Size of source mod 2**32: 1779 bytes
import math

class FIS:

    def __init__(self):
        self._rules = {}
        self._variables = {}

    def add_rule(self, rule):
        outvar = rule.get_consequent()[0]
        if outvar not in self._rules:
            self._rules[outvar] = []
        self._rules[outvar].append(rule)

    def add_variable(self, var):
        self._variables[var.get_name()] = var

    def _process_output(self, rules, vars_values):
        outvar = self._variables[rules[0].get_consequent()[0]]
        center_num = 0
        center_den = 0
        xmin, xmax = outvar.get_range()
        x = xmin
        xstep = (xmax - xmin) / 1000
        while x < xmax:
            activation = []
            for r in rules:
                for var in vars_values:
                    r.set_value(var, vars_values[var])

                ant = r.eval_antecedent()
                function = r.get_consequent()[1]
                activation.append(min(ant, function(x)))

            fx = max(activation)
            center_num += x * fx
            center_den += fx
            x += xstep

        try:
            value = center_num / center_den
        except ZeroDivisionError:
            value = float('inf')

        return value

    def defuzzy(self, vars_values):
        outputs = {}
        for o in self._rules:
            outputs[o] = self._process_output(self._rules[o], vars_values)

        return outputs