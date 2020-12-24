# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/blocks/nonlinear.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 7425 bytes
__doc__ = 'Collection of non-linear blocks\n\n'
from bms import Block
import numpy as np

class Delay(Block):
    """Delay"""

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
    """Saturation"""

    def __init__(self, input_variable, output_variable, min_value, max_value):
        Block.__init__(self, [input_variable], [output_variable], 1, 0)
        self.min_value = min_value
        self.max_value = max_value

    def Evaluate(self, it, ts):
        value = self.InputValues(it)[0]
        if value < self.min_value:
            value = self.min_value
        elif value > self.max_value:
            value = self.max_value
        return np.array([value])

    def LabelBlock(self):
        return 'Sat'


class Coulomb(Block):
    """Coulomb"""

    def __init__(self, input_variable, speed_variable, output_variable, max_value, tolerance=0):
        Block.__init__(self, [input_variable, speed_variable], [
         output_variable], 1, 0)
        self.max_value = max_value
        self.tolerance = tolerance

    def Evaluate(self, it, ts):
        input_value, speed = self.InputValues(it)
        if speed > self.tolerance:
            output = -self.max_value
        elif speed < -self.tolerance:
            output = self.max_value
        elif abs(input_value) < self.max_value:
            output = -input_value
        elif input_value < 0:
            output = self.max_value
        else:
            output = -self.max_value
        return np.array([output])

    def LabelBlock(self):
        return 'Clb'


class CoulombVariableValue(Block):
    """CoulombVariableValue"""

    def __init__(self, external_force, speed_variable, value_variable, output_variable, tolerance=0):
        Block.__init__(self, [external_force, speed_variable, value_variable], [
         output_variable], 1, 0)
        self.tolerance = tolerance

    def Evaluate(self, it, ts):
        external_force, speed, max_value = self.InputValues(it)
        if speed > self.tolerance:
            output = -max_value
        elif speed < -self.tolerance:
            output = max_value
        elif abs(external_force) < max_value:
            output = -external_force
        elif external_force < 0:
            output = max_value
        else:
            output = -max_value
        return output

    def LabelBlock(self):
        return 'Clb Var'


class RegCoulombVariableValue(Block):
    """RegCoulombVariableValue"""

    def __init__(self, external_force, speed_variable, value_variable, output_variable, tolerance=0):
        Block.__init__(self, [external_force, speed_variable, value_variable], [
         output_variable], 1, 0)
        self.tolerance = tolerance

    def Evaluate(self, it, ts):
        external_force, speed, max_value = self.InputValues(it)
        if speed > self.tolerance:
            output = -max_value
        elif speed < -self.tolerance:
            output = max_value
        elif abs(external_force) < max_value:
            output = -external_force
        elif external_force < 0:
            output = max_value
        else:
            output = -max_value
        return output

    def LabelBlock(self):
        return 'Clb Var'


class Sign(Block):
    """Sign"""

    def __init__(self, input_variable, output_variable):
        Block.__init__(self, [input_variable], [output_variable], 1, 0)

    def Evaluate(self, it, ts):
        input_value = self.InputValues(it)[0]
        if input_value < 0:
            output = -1
        elif input_value > 0:
            output = 1
        else:
            output = 0
        return np.array([output])

    def LabelBlock(self):
        return 'Sgn'