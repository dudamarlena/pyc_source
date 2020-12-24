# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/models/gimenez.py
# Compiled at: 2020-01-13 18:32:58
# Size of source mod 2**32: 3346 bytes
import numpy as np
from .transitmodel import TransitModel

class Gimenez(TransitModel):
    __doc__ = 'Exoplanet transit light curve model by A. Gimenez (A&A 450, 1231--1237, 2006).\n\n    This class aims to offer an easy access to the Fortran implementation of the\n    transit model by A. Gimenez (A&A 450, 1231--1237, 2006). The Fortran code is\n    adapted from the original implementation at http://thor.ieec.uab.es/LRVCode,\n    and includes several optimisations that make it several orders faster for\n    light curves with thousands to millions of datapoints.\n    '

    def __init__(self, method='pars', is_secondary=False):
        """Initialise the model.

        Args:
            npol:
            nldc: Number of limb darkening coefficients.
            nthr: Number of threads (default = 0).
            interpolate: If True, evaluates the model using interpolation (default = False).
            supersampling: Number of subsamples to calculate for each light curve point (default=0).
            exptime: Integration time for a single exposure, used in supersampling default=(0.02).
            is_secondary: If True, evaluates the model for eclipses. If false, eclipses are filtered out (default = False).
        """
        raise NotImplementedError
        super(Gimenez, self).__init__(is_secondary, exptime)
        self._eval = self._eval_interpolate if (interpolate or kwargs.get('lerp', False)) else (self._eval_nointerpolate)
        self._coeff_arr = g.init_arrays(npol, nldc)
        self.npol = npol

    def __call__(self, z, k, u, c=0.0, b=1e-08, update=True):
        """Evaluates the model for the given z, k, and u. 

        Evaluates the transit model given an array of normalised distances, a radius ratio, and
        a set of limb darkening coefficients.

        Args:
            z: Array of normalised projected distances.
            k: Planet to star radius ratio.
            u: Array of limb darkening coefficients.
            c: Contamination factor (fraction of third light), optional.
           
        Returns:
            An array of model flux values for each z.
        """
        u = np.reshape(u, [-1, self.nldc]).T
        c = np.ones(u.shape[1]) * c
        flux = self._eval(z, k, u, c, b, update)
        if u.shape[1] > 1:
            return flux
        return flux.ravel()

    def _eval_nointerpolate(self, z, k, u, c, b, update):
        return (g.eval)(z, k, u, c, self.nthr, *self._coeff_arr)

    def _eval_interpolate(self, z, k, u, c, b, update):
        return (g.eval_lerp)(z, k, u, b, c, self.nthr, update, *self._coeff_arr)