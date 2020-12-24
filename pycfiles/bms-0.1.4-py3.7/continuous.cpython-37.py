# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/blocks/continuous.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 10187 bytes
"""Collection of continuous blocks

"""
from bms import Block
import numpy as np
from scipy.special import factorial

class Gain(Block):
    __doc__ = 'Defines a gain operation.\n\n    .. math:: output = (value \\times input) + offset\n\n    Args:\n        input_variable (Variable): This is the input of the block.\n        output_variable (Variable): This is the output of the block.\n        gain: This is what multiplies the input.\n        offset: This is added to the input after being multiplied.\n\n    '

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
    __doc__ = 'Defines a sum over its inputs.\n\n    .. math:: output = \\sum{input_i}\n       \n    Args: \n        input_variable (list[Variables]): This is the list of inputs of the block.\n        output_variable (Variable): This is the output of the block.\n\n    '

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
    __doc__ = 'Defines a weighted sum over its inputs.\n\n    .. math:: output = \\sum{w_i \\times input_i}\n\n    Args:        \n        input_variable (list[Variables]): This is the list of inputs of the block.\n        output_variable (Variable): This is the output of the block.\n        weights: These are the weights that are multiplied by the elements of the input.\n        offset: This offset is added to the final result.\n\n    '

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
    __doc__ = 'Defines a subtraction between its two inputs.\n\n    .. math:: output = input_1 - input_2\n        \n    Args:\n        input_variable1 (Variable): This is the first input of the block, the minuend.\n        input_variable2 (Variable): This is the second input of the block, the subtrahend.\n        output_variable (Variable): This is the output of the block, the difference.\n\n    '

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
    __doc__ = 'Defines a multiplication between its inputs.\n\n    .. math:: output = input_1 \\times input_2\n        \n    Args:\n        input_variable1 (Variable): This is the first input of the block, one factor.\n        input_variable2 (Variable): This is the second input of the block, another factor.\n        output_variable (Variable): This is the output of the block, the product.\n\n    '

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
    __doc__ = 'Defines a division between its inputs.\n\n    .. math:: output = \\frac{input1}{input2}\n    \n    Args:    \n        input_variable1 (Variable): This is the first input of the block, the dividend.\n        input_variable2 (Variable): This is the second input of the block, the divisor.\n        output_variable (Variable): This is the output of the block, the quotient.\n\n    '

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
    __doc__ = "Defines an ordinary differential equation based on the input.\n\n    a, b are vectors of coefficients so that H, the transfer function of\n    the block, can be written as:\n\n    .. math:: H(p) = \\frac{a_i p^i}{b_j p^j}\n\n    with Einstein sum on i and j, and p is Laplace's variable.\n\n    For example, :code:`a=[1], b=[0,1]` is an integration, \n    and :code:`a=[0,1], b=[1]` is a differentiation.\n        \n    Args:\n        input_variable (Variable): This is the input of the block.\n        output_variable (Variable): This is the output of the block.\n        a: This is the a vector for the transfer function.\n        b: This is the b vector for the transfer function.\n\n    "

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
        return (Mi, Mo)

    def OutputMatrices(self, delta_t):
        try:
            Mi, Mo = self._M[delta_t]
        except KeyError:
            Mi, Mo = self._get_M(delta_t)
            self._M[delta_t] = (Mi, Mo)

        return (
         Mi, Mo)

    def Evaluate(self, it, ts):
        Mi, Mo = self.OutputMatrices(ts)
        return np.dot(Mi, self.InputValues(it).T) + np.dot(Mo, self.OutputValues(it).T)

    def LabelBlock(self):
        return str(self.a) + '\n' + str(self.b)

    def LabelConnections(self):
        return [
         '', '']


class IntegrationBlock(ODE):
    __doc__ = 'Creates an ODE block that performs integration of the input over time.\n    \n    .. math:: output = \\int_{0}^{t} input\\ dt\n    \n    Args:\n        input_variable: This is the input or list of inputs of the block.\n        output_variable (Variable): This is the output of the block.\n\n    '

    def __init__(self, input_variable, output_variable):
        ODE.__init__(self, input_variable, output_variable, a=[1], b=[0, 1])

    def LabelBlock(self):
        return 'Integral'


class DifferentiationBlock(ODE):
    __doc__ = 'Creates an ODE block that performs differentation of the input relative to time.\n        \n    .. math:: output = \\frac{d[input]}{dt}\n    \n    Args:\n        input_variable: This is the input or list of inputs of the block.\n        output_variable (Variable): This is the output of the block.\n    \n    '

    def __init__(self, input_variable, output_variable):
        ODE.__init__(self, input_variable, output_variable, a=[0, 1], b=[1])

    def LabelBlock(self):
        return 'dx/dt'


class FunctionBlock(Block):
    __doc__ = 'This defines a custom function over the input(s).\n\n    .. math:: output = f(input)\n        \n    Args:\n        input_variable: This is the input or list of inputs of the block.\n        output_variable (Variable): This is the output of the block.\n        function: This is the function that takes the inputs and returns the output.\n\n    '

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