# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/blocks/nonlinear.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 7425 bytes
"""Collection of non-linear blocks

"""
from bms import Block
import numpy as np

class Delay(Block):
    __doc__ = '\n    Simple block to delay output with respect to input.\n    \n    :param delay: a delay in seconds\n    '

    def __init__(self, input_variable, output_variable, delay):
        Block.__init__(self, [input_variable], [output_variable], 1, 0)
        self.delay = delay
        if delay < 0:
            raise ValueError

    def Evaluate(self, it, ts):
        delay_in_steps = int(self.delay // ts)
        delay_remainder = self.delay % ts
        if it - delay_in_steps - 1 < 0:
            return self.inputs[0].initial_values[(-1)]
        v1 = self.inputs[0]._values[(it - delay_in_steps - 1)]
        v2 = self.inputs[0]._values[(it - delay_in_steps)]
        return (ts - delay_remainder) / ts * (v2 - v1) + v1

    def Label(self):
        return 'delay'


class Saturation(Block):
    __doc__ = 'Defines a saturation block.\n\n    .. math::\n        output = \n        \\begin{cases}\n            min\\_value, & \\textrm{if } input < min\\_value\n\n            max\\_value, & \\textrm{if } input > max\\_value\n\n            input, & \\textrm{if } min\\_value \\leq input \\leq max\\_value\n        \\end{cases}\n\n    Args:\n        input_variable (Variable): This is the input of the block.\n        output_variable (Variable): This is the output of the block.\n        min_value: This is the lower bound for the output.\n        max_value: This is the upper bound for the output.\n    '

    def __init__(self, input_variable, output_variable, min_value, max_value):
        Block.__init__(self, [input_variable], [output_variable], 1, 0)
        self.min_value = min_value
        self.max_value = max_value

    def Evaluate(self, it, ts):
        value = self.InputValues(it)[0]
        if value < self.min_value:
            value = self.min_value
        else:
            if value > self.max_value:
                value = self.max_value
        return np.array([value])

    def LabelBlock(self):
        return 'Sat'


class Coulomb(Block):
    __doc__ = '\n        Return coulomb force under condition of speed and sum of forces (input)\n\n    '

    def __init__(self, input_variable, speed_variable, output_variable, max_value, tolerance=0):
        Block.__init__(self, [input_variable, speed_variable], [
         output_variable], 1, 0)
        self.max_value = max_value
        self.tolerance = tolerance

    def Evaluate(self, it, ts):
        input_value, speed = self.InputValues(it)
        if speed > self.tolerance:
            output = -self.max_value
        else:
            if speed < -self.tolerance:
                output = self.max_value
            else:
                if abs(input_value) < self.max_value:
                    output = -input_value
                else:
                    if input_value < 0:
                        output = self.max_value
                    else:
                        output = -self.max_value
        return np.array([output])

    def LabelBlock(self):
        return 'Clb'


class CoulombVariableValue(Block):
    __doc__ = '\n        Return coulomb force under condition of speed and sum of forces (input)\n        The max value is driven by an input\n    '

    def __init__(self, external_force, speed_variable, value_variable, output_variable, tolerance=0):
        Block.__init__(self, [external_force, speed_variable, value_variable], [
         output_variable], 1, 0)
        self.tolerance = tolerance

    def Evaluate(self, it, ts):
        external_force, speed, max_value = self.InputValues(it)
        if speed > self.tolerance:
            output = -max_value
        else:
            if speed < -self.tolerance:
                output = max_value
            else:
                if abs(external_force) < max_value:
                    output = -external_force
                else:
                    if external_force < 0:
                        output = max_value
                    else:
                        output = -max_value
        return output

    def LabelBlock(self):
        return 'Clb Var'


class RegCoulombVariableValue(Block):
    __doc__ = '\n        Return coulomb force under condition of speed and sum of forces (input)\n        The max value is driven by an input\n    '

    def __init__(self, external_force, speed_variable, value_variable, output_variable, tolerance=0):
        Block.__init__(self, [external_force, speed_variable, value_variable], [
         output_variable], 1, 0)
        self.tolerance = tolerance

    def Evaluate(self, it, ts):
        external_force, speed, max_value = self.InputValues(it)
        if speed > self.tolerance:
            output = -max_value
        else:
            if speed < -self.tolerance:
                output = max_value
            else:
                if abs(external_force) < max_value:
                    output = -external_force
                else:
                    if external_force < 0:
                        output = max_value
                    else:
                        output = -max_value
        return output

    def LabelBlock(self):
        return 'Clb Var'


class Sign(Block):
    __doc__ = 'Defines a sign operation on the input.\n\n    .. math::\n        output = \n        \\begin{cases}\n        -1, & \\textrm{if } input < 0\n\n        0, & \\textrm{if } input = 0\n\n        1, & \\textrm{if } input > 0\n        \\end{cases}\n        \n    '

    def __init__(self, input_variable, output_variable):
        Block.__init__(self, [input_variable], [output_variable], 1, 0)

    def Evaluate(self, it, ts):
        input_value = self.InputValues(it)[0]
        if input_value < 0:
            output = -1
        else:
            if input_value > 0:
                output = 1
            else:
                output = 0
        return np.array([output])

    def LabelBlock(self):
        return 'Sgn'