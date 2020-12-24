# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bms/signals/functions.py
# Compiled at: 2020-04-02 08:37:19
# Size of source mod 2**32: 2682 bytes
__doc__ = '\nCollection of mathematical function signals\n'
from bms import Signal
import numpy as np

class Step(Signal):
    """Step"""

    def __init__(self, name='Step', amplitude=1, delay=0, offset=0):
        Signal.__init__(self, name)

        def function(t):
            if t < delay:
                return offset
            return amplitude + offset

        self.function = function


class Ramp(Signal):
    """Ramp"""

    def __init__(self, name='Ramp', amplitude=1, delay=0, offset=0):
        Signal.__init__(self, name)

        def function(t):
            if t < delay:
                return offset
            return (t - delay) * amplitude + offset

        self.function = function


unit_ramp = Ramp(amplitude=1, name='Unit ramp')

class Sinus(Signal):
    """Sinus"""

    def __init__(self, name='Sinus', amplitude=1, w=1, phase=0, offset=0):
        Signal.__init__(self, name)
        self.function = lambda t: amplitude * np.sin(w * t + phase) + offset


class SignalFunction(Signal):
    """SignalFunction"""

    def __init__(self, name, function):
        Signal.__init__(self, name)
        self.function = function