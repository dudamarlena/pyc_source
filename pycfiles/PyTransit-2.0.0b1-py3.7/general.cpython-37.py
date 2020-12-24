# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/models/general.py
# Compiled at: 2020-03-28 19:16:40
# Size of source mod 2**32: 9203 bytes
from typing import Union, Optional, List
from numpy import ndarray, array, squeeze, atleast_2d, atleast_1d, zeros, asarray
from numba.general_nb import init_arrays, general_model_s, general_model_v, general_model_pv
from .transitmodel import TransitModel
__all__ = [
 'GeneralModel']

class GeneralModel(TransitModel):
    __doc__ = 'Transit model with general limb darkening (Giménez, A&A 450, 1231–1237, 2006).\n\n    Transit model with general limb darkening (Giménez, A&A 450, 1231–1237, 2006) with optimizations described in\n    Parviainen (MNRAS 450, 3233–3238, 2015).\n\n    The general limb darkening law is\n\n    .. math:: I(\\mu) = I(1) (1 - \\sum_{n=1}^N u_n(1-\\mu^n) )\n\n    '

    def __init__(self, npol=50, nldc=2, mode=0):
        if npol < 1:
            raise ValueError(f"`npol` has to be positive, now {npol}")
        if nldc <= 0:
            raise ValueError(f"`nldc` cannot be negative, now {nldc}")
        if mode not in (0, 1):
            raise ValueError('`mode` has to be either 0 (normal) or 1 (transmission spectroscopy).')
        super().__init__()
        self.npol = npol
        self.nldc = nldc
        self.mode = mode
        self._anm, self._avl, self._ajd, self._aje = init_arrays(npol, nldc)

    def evaluate(self, k: Union[(float, ndarray)], ldc: Union[(ndarray, List)], t0: Union[(float, ndarray)], p: Union[(float, ndarray)], a: Union[(float, ndarray)], i: Union[(float, ndarray)], e: Optional[Union[(float, ndarray)]]=None, w: Optional[Union[(float, ndarray)]]=None, copy: bool=True) -> ndarray:
        """Evaluate the transit model for a set of scalar or vector parameters.

        Parameters
        ----------
        k
            Radius ratio(s) either as a single float, 1D vector, or 2D array.
        ldc
            Limb darkening coefficients as a 1D or 2D array.
        t0
            Transit center(s) as a float or a 1D vector.
        p
            Orbital period(s) as a float or a 1D vector.
        a
            Orbital semi-major axis (axes) divided by the stellar radius as a float or a 1D vector.
        i
            Orbital inclination(s) as a float or a 1D vector.
        e : optional
            Orbital eccentricity as a float or a 1D vector.
        w : optional
            Argument of periastron as a float or a 1D vector.

        Notes
        -----
        The model can be evaluated either for one set of parameters or for many sets of parameters simultaneously. In
        the first case, the orbital parameters should all be given as floats. In the second case, the orbital parameters
        should be given as a 1D array-like.

        Returns
        -------
        ndarray
            Modelled flux either as a 1D or 2D ndarray.
        """
        if isinstance(t0, float):
            if e is None:
                e, w = (0.0, 0.0)
            return self.evaluate_ps(k, ldc, t0, p, a, i, e, w, copy)
        ldc = atleast_2d(ldc)
        k, t0, p, a, i = (asarray(k), asarray(t0), asarray(p), asarray(a), asarray(i))
        if k.ndim == 1:
            k = k.reshape((k.size, 1))
        npv = t0.size
        if e is None:
            e, w = zeros(npv), zeros(npv)
        flux = general_model_v(self.time, k, t0, p, a, i, e, w, ldc, self.mode, self.lcids, self.pbids, self.nsamples, self.exptimes, self.npb, self.npol, self.nldc, self._es, self._ms, self._tae, self._anm, self._avl, self._ajd, self._aje)
        return squeeze(flux)

    def evaluate_ps(self, k: Union[(float, ndarray)], ldc: ndarray, t0: float, p: float, a: float, i: float, e: float=0.0, w: float=0.0, copy: bool=True) -> ndarray:
        """Evaluate the transit model for a set of scalar parameters.

        Parameters
        ----------
        k : array-like
            Radius ratio(s) either as a single float or an 1D array.
        ldc : array-like
            Limb darkening coefficients as a 1D array.
        t0 : float
            Transit center as a float.
        p : float
            Orbital period as a float.
        a : float
            Orbital semi-major axis divided by the stellar radius as a float.
        i : float
            Orbital inclination(s) as a float.
        e : float, optional
            Orbital eccentricity as a float.
        w : float, optional
            Argument of periastron as a float.

        Notes
        -----
        This version of the `evaluate` method is optimized for calculating a single transit model (such as when using a
        local optimizer). If you want to evaluate the model for a large number of parameters simultaneously, use either
        `evaluate` or `evaluate_pv`.

        Returns
        -------
        ndarray
            Modelled flux as a 1D ndarray.
        """
        ldc = asarray(ldc)
        k = asarray(k)
        if self.time is None:
            raise ValueError('Need to set the data before calling the transit model.')
        if ldc.size != self.nldc * self.npb:
            raise ValueError('The quadratic model needs two limb darkening coefficients per passband')
        flux = general_model_s(self.time, k, t0, p, a, i, e, w, ldc, self.mode, self.lcids, self.pbids, self.nsamples, self.exptimes, self.npb, self.npol, self.nldc, self._es, self._ms, self._tae, self._anm, self._avl, self._ajd, self._aje)
        return squeeze(flux)

    def evaluate_pv(self, pvp: ndarray, ldc: ndarray, copy: bool=True) -> ndarray:
        """Evaluate the transit model for a 2D parameter array.

        Parameters
        ----------
        pvp: ndarray
            Parameter array with a shape `(npv, npar)` where `npv` is the number of parameter vectors, and each row
            contains a set of parameters `[k, t0, p, a, i, e, w]`. The radius ratios can also be given per passband,
            in which case the row should be structured as `[k_0, k_1, k_2, ..., k_npb, t0, p, a, i, e, w]`.
        ldc: ndarray
            Limb darkening coefficient array with shape `(npv, 2*npb)`, where `npv` is the number of parameter vectors
            and `npb` is the number of passbands.

        Notes
        -----
        This version of the `evaluate` method is optimized for calculating several models in parallel, such as when
        using *emcee* for MCMC sampling.

        Returns
        -------
        ndarray
            Modelled flux either as a 1D or 2D ndarray.
        """
        ldc = asarray(ldc)
        pvp = asarray(pvp)
        if self.time is None:
            raise ValueError('Need to set the data before calling the transit model.')
        flux = general_model_pv(self.time, pvp, ldc, self.mode, self.lcids, self.pbids, self.nsamples, self.exptimes, self.npb, self.npol, self.nldc, self._es, self._ms, self._tae, self._anm, self._avl, self._ajd, self._aje)
        return squeeze(flux)

    def to_opencl(self):
        """Creates an OpenCL clone (`QuadraticModelCL`) of the transit model.

        Returns
        -------
        QuadraticModelCL
        """
        from .ma_quadratic_cl import QuadraticModelCL
        tm = QuadraticModelCL(klims=(self.klims))
        tm.set_data(self.time, self.lcids, self.pbids, self.nsamples, self.exptimes)
        return tm