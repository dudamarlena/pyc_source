# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swapsha96/mtp/MiraPy/build/lib/mirapy/fitting/models.py
# Compiled at: 2019-05-03 11:14:15
# Size of source mod 2**32: 1702 bytes
import autograd.numpy as np

class Model1D:

    def __init__(self):
        pass

    def __call__(self, x):
        return self.evaluate(x)

    def evaluate(self, x):
        pass

    def set_params_from_array(self, params):
        pass

    def get_params_as_array(self):
        pass


class Gaussian1D(Model1D):
    __doc__ = '\n        One dimensional Gaussian model.\n\n        Parameters\n        ----------\n        amplitude : float\n            Amplitude of the Gaussian.\n        mean : float\n            Mean of the Gaussian.\n        stddev : float\n            Standard deviation of the Gaussian.\n        '

    def __init__(self, amplitude=1.0, mean=0.0, stddev=1.0):
        self.amplitude = amplitude
        self.mean = mean
        self.stddev = stddev

    def __call__(self, x):
        return self.evaluate(x)

    def evaluate(self, x):
        """
        Gaussian1D model function.

        Parameters
        ----------
        x : array
            Input of the model.

        Returns
        -------
        array : Output of the Gaussian function.
        """
        return self.amplitude * np.exp(-0.5 * (x - self.mean) ** 2 / self.stddev ** 2)

    def set_params_from_array(self, params):
        """
        Sets the parameters of the model from an array.
        """
        if len(params) != 3:
            raise ValueError('The length of the parameter array must be 3')
        self.amplitude = params[0]
        self.mean = params[1]
        self.stddev = params[2]

    def get_params_as_array(self):
        return np.array([self.amplitude, self.mean, self.stddev])