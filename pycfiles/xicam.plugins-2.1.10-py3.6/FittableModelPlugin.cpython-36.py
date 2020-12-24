# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\FittableModelPlugin.py
# Compiled at: 2018-05-17 15:54:05
# Size of source mod 2**32: 826 bytes
from astropy.modeling import Fittable1DModel
from yapsy.IPlugin import IPlugin

class Fittable1DModelPlugin(Fittable1DModel, IPlugin):
    __doc__ = '\n    Plugins of this base class mimic the astropy FittableModel class structure. An activated fittable model would be\n    usable for fitting 1-d spectra or 2-d images. Example: A 1-D Lorentzian model, usable for fitting SAXS spectra.\n\n    See the Astropy API for a detailed explanation of the usage.\n\n    See xicam.plugins.tests for examples.\n\n    '

    @staticmethod
    def evaluate(x, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def fit_deriv(x, *args, **kwargs):
        raise NotImplementedError

    @property
    def inverse(self):
        raise NotImplementedError