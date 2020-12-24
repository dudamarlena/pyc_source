# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/hardware_modules/sampler.py
# Compiled at: 2017-08-29 09:44:06
import numpy as np
from ..pyrpl_utils import time
from ..attributes import FloatRegister
from ..modules import HardwareModule
from . import DSP_INPUTS

class Sampler(HardwareModule):
    """ this module provides a sample of each signal.

    This is a momentary workaround, will be improved later on with an upgraded FPGA version """
    addr_base = 1076887552

    def stats(self, signal='in1', t=0.01):
        """
        computes the mean, standard deviation, min and max of the chosen signal over duration t

        Parameters
        ----------
        signal: input signal
        t: duration over which to average

        obsolete:
        n: equivalent number of FPGA clock cycles to average over

        Returns
        -------
        mean, stddev, max, min: mean and standard deviation of all samples

        """
        try:
            signal = signal.name
        except AttributeError:
            pass

        nn = 0
        cum = 0
        cumsq = 0
        max = -np.inf
        min = np.inf
        t0 = time()
        while nn == 0 or time() < t0 + t:
            nn += 1
            value = self.__getattribute__(signal)
            cum += value
            cumsq += value ** 2.0
            if value > max:
                max = value
            if value < min:
                min = value

        nn = float(nn)
        mean = cum / nn
        variance = cumsq / nn - mean ** 2.0
        if variance < 0:
            variance = 0
        stddev = variance ** 0.5
        return (
         mean, stddev, max, min)

    def mean_stddev(self, signal='in1', t=0.01):
        """
        computes the mean and standard deviation of the chosen signal

        Parameters
        ----------
        signal: input signal
        t: duration over which to average

        obsolete:
        n: equivalent number of FPGA clock cycles to average over

        Returns
        -------
        mean, stddev: mean and standard deviation of all samples

        """
        self._logger.warning('Sampler.mean_stddev() is obsolete. Please use Sampler.stats() instead!')
        mean, stddev, max, min = self.stats(signal=signal, t=t)
        return (
         mean, stddev)


for inp, num in DSP_INPUTS.items():
    setattr(Sampler, inp, FloatRegister(16 + num * 65536, bits=14, norm=8191, doc='current value of ' + inp))