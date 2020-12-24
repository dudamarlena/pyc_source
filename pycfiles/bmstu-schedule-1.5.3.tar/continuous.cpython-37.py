# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/blocks/continuous.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 10187 bytes
__doc__ = 'Collection of continuous blocks\n\n'
from bms import Block
import numpy as np
from scipy.special import factorial

class Gain(Block):
    """Gain"""

    def __init__(self, input_variable, output_variable, value, offset=0):
        Block.__init__(self, [input_variable], [output_variable], 1, 0)
        self.value = value
        self.offset = offset

    def Evaluate(self, it, ts):
        return self.value * self.InputValues(it)[0] + self.offset

    def LabelBlock(self):
        return str(self.value)

    def LabelConnections(self):
        return [
         '', '']


class Sum(Block):
    """Sum"""

    def __init__(self, inputs, output_variable):
        Block.__init__(self, inputs, [output_variable], 1, 0)

    def Evaluate(self, it, ts):
        return np.array([np.sum(self.InputValues(it))])

    def LabelBlock(self):
        return '+'

    def LabelConnections(self):
        return [
         '+', '+']


class WeightedSum(Block):
    """WeightedSum"""

    def __init__(self, inputs, output_variable, weights, offset=0):
        Block.__init__(self, inputs, [output_variable], 1, 0)
        self.weights = weights
        self.offset = offset

    def Evaluate(self, it, ts):
        value = np.dot(self.weights, self.InputValues(it)) + self.offset
        return value

    def LabelBlock(self):
        return 'W+' + str(self.weights)

    def LabelConnections(self):
        return self.weights


class Subtraction(Block):
    """Subtraction"""

    def __init__(self, input_variable1, input_variable2, output_variable):
        Block.__init__(self, [input_variable1, input_variable2], [
         output_variable], 1, 0)

    def Evaluate(self, it, ts):
        return np.dot(np.array([1, -1]), self.InputValues(it))

    def LabelBlock(self):
        return '-'

    def LabelConnections(self):
        return [
         '+', '-']


class Product(Block):
    """Product"""

    def __init__(self, input_variable1, input_variable2, output_variable):
        Block.__init__(self, [input_variable1, input_variable2], [
         output_variable], 1, 0)

    def Evaluate(self, it, ts):
        value1, value2 = self.InputValues(it)
        return np.array([value1 * value2])

    def LabelBlock(self):
        return 'x'

    def LabelConnections(self):
        return [
         '', '']


class Division(Block):
    """Division"""

    def __init__(self, input_variable1, input_variable2, output_variable):
        Block.__init__(self, [input_variable1, input_variable2], [
         output_variable], 1, 0)

    def Evaluate(self, it, ts):
        value1, value2 = self.InputValues(it)
        return value1 / value2

    def LabelBlock(self):
        return '/'

    def LabelConnections(self):
        return [
         '', '']


class ODE(Block):
    """ODE"""

    def __init__(self, input_variable, output_variable, a, b):
        Block.__init__(self, [input_variable], [
         output_variable], len(a), len(b) - 1)
        self.a = a
        self.b = b
        self._M = {}

    def _get_M(self, delta_t):
        n = len(self.a)
        A = np.zeros(n)
        for i, ai in enumerate(self.a):
            Ae = [self.a[i] * (-1) ** j * factorial(i) / factorial(j) / factorial(i - j) / delta_t ** i for j in range(i + 1)]
            for j, aej in enumerate(Ae):
                A[j] += aej

        n = len(self.b)
        B = np.zeros(n)
        for i, ai in enumerate(self.b):
            Be = [self.b[i] * (-1) ** j * factorial(i) / factorial(j) / factorial(i - j) / delta_t ** i for j in range(i + 1)]
            for j, bej in enumerate(Be):
                B[j] += bej

        Mo = [-x / B[0] for x in B[1:][::-1]]
        Mi = [x / B[0] for x in A[::-1]]
        return (
         Mi, Mo)

    def OutputMatrices(self, delta_t):
        try:
            Mi, Mo = self._M[delta_t]
        except KeyError:
            Mi, Mo = self._get_M(delta_t)
            self._M[delta_t] = (Mi, Mo)

        return (Mi, Mo)

    def Evaluate(self, it, ts):
        Mi, Mo = self.OutputMatrices(ts)
        return np.dot(Mi, self.InputValues(it).T) + np.dot(Mo, self.OutputValues(it).T)

    def LabelBlock(self):
        return str(self.a) + '\n' + str(self.b)

    def LabelConnections(self):
        return [
         '', '']


class IntegrationBlock(ODE):
    """IntegrationBlock"""

    def __init__(self, input_variable, output_variable):
        ODE.__init__(self, input_variable, output_variable, a=[1], b=[0, 1])

    def LabelBlock(self):
        return 'Integral'


class DifferentiationBlock(ODE):
    """DifferentiationBlock"""

    def __init__(self, input_variable, output_variable):
        ODE.__init__(self, input_variable, output_variable, a=[0, 1], b=[1])

    def LabelBlock(self):
        return 'dx/dt'


class FunctionBlock(Block):
    """FunctionBlock"""

    def __init__(self, input_variable, output_variable, function):
        self.list_as_input = isinstance(input_variable, list)
        if self.list_as_input:
            Block.__init__(self, input_variable, [output_variable], 1, 0)
        else:
            Block.__init__(self, [input_variable], [output_variable], 1, 0)
        self.function = function

    def Evaluate(self, it, ts):
        if self.list_as_input:
            return np.array([(self.function)(*self.InputValues(it))])
        return np.array([self.function(self.InputValues(it)[0])])

    def LabelBlock(self):
        return 'f(t)'

    def LabelConnections(self):
        return [
         '', '']