# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/signals/functions.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 2682 bytes
"""
Collection of mathematical function signals
"""
from bms import Signal
import numpy as np

class Step(Signal):
    __doc__ = 'Create a Step with a certain amplitude, time delay and offset.\n\n    .. math:: f(t) = amplitude \\times u(t - delay) + offset\n\n    where\n\n    .. math::\n        u(t) =\n        \\begin{cases}\n            0, & \\textrm{if } t < 0\n\n            1, & \\textrm{if } t \\geq 0\n        \\end{cases}\n        \n\n    Args:\n        name (str): The name of this signal.\n        amplitude: The height of the step function.\n        delay: The time to wait before the function stops being zero.\n        offset: The vertical offset of the function.\n\n    '

    def __init__(self, name='Step', amplitude=1, delay=0, offset=0):
        Signal.__init__(self, name)

        def function(t):
            if t < delay:
                return offset
            return amplitude + offset

        self.function = function


class Ramp(Signal):
    __doc__ = 'Create a Ramp with a certain amplitude, time delay and offset.\n\n    .. math:: f(t) = amplitude \\times (t - delay) + offset\n\n    Args:\n        name (str): The name of this signal.\n        amplitude: The angular coefficient of the Ramp function.\n        delay: The horizontal offset of the function.\n        offset: The vertical offset of the function.\n\n    '

    def __init__(self, name='Ramp', amplitude=1, delay=0, offset=0):
        Signal.__init__(self, name)

        def function(t):
            if t < delay:
                return offset
            return (t - delay) * amplitude + offset

        self.function = function


unit_ramp = Ramp(amplitude=1, name='Unit ramp')

class Sinus(Signal):
    __doc__ = 'Create a Sine wave with a certain amplitude, angular velocity, phase and offset.\n\n    .. math:: f(t) = amplitude \\times sin(\\omega \\times t + phase) + offset\n\n    Args:\n        name (str): The name of this signal.\n        amplitude: The amplitude of the sine wave.\n        w: The angular velocity of the sine wave (:math:`\\omega`).\n        phase: The phase of the sine wave.\n        offset: The vertical offset of the function.\n\n    '

    def __init__(self, name='Sinus', amplitude=1, w=1, phase=0, offset=0):
        Signal.__init__(self, name)
        self.function = lambda t: amplitude * np.sin(w * t + phase) + offset


class SignalFunction(Signal):
    __doc__ = 'Create a signal based on a function defined by the user.\n\n    Args:\n        name (str): The name of this signal.\n        function: A function that depends on time.\n\n    '

    def __init__(self, name, function):
        Signal.__init__(self, name)
        self.function = function