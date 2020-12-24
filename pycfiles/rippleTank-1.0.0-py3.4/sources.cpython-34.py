# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rippleTank/sources.py
# Compiled at: 2017-07-21 07:38:48
# Size of source mod 2**32: 2498 bytes
import numpy as np
from .masks import getPositions

class Source:
    __doc__ = '\n    Sources create perturbations on the ripple tank.\n    '

    def __init__(self, rippletank, function, xcorners=(-0.5, 0.5), ycorners=(-0.5, 0.5), freq=1, phase=0, amplitude=0.1):
        self.rippletank = rippletank
        self.X_grid = rippletank.X
        self.Y_grid = rippletank.Y
        self.xcorners = xcorners
        self.ycorners = ycorners
        self.freq = freq
        self.period = 1.0 / freq
        self.phase = phase
        self.function = function
        self.positions = getPositions(self.X_grid, self.Y_grid, self.xcorners, self.ycorners)
        if amplitude < 0 or amplitude > 1:
            raise Exception('Amplitude is not valid')
        self.amplitude = amplitude
        self.rippletank.addSource(self)

    def evaluate(self, i):
        """
        Receives an int number related with an iterator, evaluates `function` using that number.

        Returns:
            np.ndarray: source values.
        """
        answer = self.function(self, i)
        if type(answer) == type(None):
            return np.zeros_like(self.X_grid)
        return answer * self.amplitude * self.rippletank.deep


def dropSource(source, i):
    """
    Pulse function.

    Returns:
        np.ndarray: array with -1.0 values on source positions.
    """
    t = source.rippletank.dt * i
    if t != 0:
        return
    answer = np.zeros_like(source.X_grid)
    answer[source.positions] = -1.0
    return answer


def sineSource(source, i):
    """
    Sine function.

    Returns:
        np.ndarray: array with sine values on source positions.
    """
    t = source.rippletank.dt * i
    answer = np.zeros_like(source.X_grid)
    value = np.sin(2 * np.pi * source.freq * t + source.phase)
    answer[source.positions] = value
    return answer


def squareSource(source, i):
    """
    Square function.

    Returns:
        np.ndarray: array with square values on source positions.
    """
    answer = sineSource(source, i)
    answer[answer > 0] = 1.0
    answer[answer < 0] = -1.0
    return answer