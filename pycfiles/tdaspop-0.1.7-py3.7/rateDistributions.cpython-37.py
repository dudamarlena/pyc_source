# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tdaspop/rateDistributions.py
# Compiled at: 2019-04-30 16:41:20
# Size of source mod 2**32: 9769 bytes
"""
"""
from __future__ import absolute_import, print_function, division
__all__ = [
 'PowerLawRates']
import numpy as np
from astropy.cosmology import Planck15
from . import BaseRateDistributions

class PowerLawRates(BaseRateDistributions):
    __doc__ = '\n    Concrete implementation of `RateDistributions` providing rates and TDO\n    numbers and samples as a function of redshift when the volumetric rate can\n    be expressed as a power law in redshift. This is instantiated by the following\n    parameters and has the attributes and methods listed\n\n\n    Parameters\n    ----------\n    rng : `np.random.RandomState`\n        random state needed for generation\n    cosmo : `astropy.cosmology` instance, defaults to Planck15\n        Cosmology used in the calculation of volumes etc. \n    alpha_rate :`np.float` defaults to 2.6e-5\n    beta_rate : `np.float` defaults to 1.5\n    zbin_edges : sequence of floats, defaults to `None`\n        Available method of having non-uniform redshift bins by specifying\n        the edgees of the bins. To specify `n` bins, this sequence must have a\n        length of `n + 1`. Has higher preference compared to setting values for\n        `zlower`, `zhigher` and `numBins` which necessarily require uniformly\n        spaced bin, and must be set to `None` for other methods to be used.\n    zlower : `np.float`, defaults to 1.0e-8 \n        Lower end of the redshift distribution, which is used in one of the\n        available methods to set the redshift bins. Must be used in concert\n        with `zhigher`, and `numBins` with `zbin_edges` set to `None` for this\n        to work.\n    zhigher : `np.float`, defaults to 1.4,\n        Higher end of the redshift distribution, which is used in one of the\n        available methods to set the redshift bins. Must be used in concert\n        with `zlower`, and `numBins` with `zbin_edges` set to `None` for this\n        to work.\n    num_bins : `int`, defaults to 28,\n        number of bins, assuming uniform redshift bins as one of the variables\n        for use in setting the redshift bins. Must be used in concert\n        with `zlower`, and `zhigher` with `zbin_edges` set to `None` for this\n        to work.\n    survey_duration :`np.float`, unit of years, defaults to 10.0\n        number of years of survey\n    sky_area : `np.float`, unit of sq deg,  defaults to 10.0 \n        Used if `skyFraction` is set to `None`. The area of the sky over which\n        the samples are calculated. Exactly one of `sky_area` and `skyFraction`\n        must be provided.\n    sky_fraction : `np.float`, defaults to `None`\n        if not `None` the fraction of the sky over which samples are studied.\n        if `None`, this is set by `sky_area`. Exactly one of `sky_area` and\n        `skyFraction` must be provided.\n\n    Attributes\n    ----------\n    - rate: The variable rate is a single power law with numerical\n        coefficients (alpha, beta)  passed into the instantiation. The rate is\n        the number of variables at redshift z per comoving volume per unit\n        observer time over the entire sky expressed in units of \n        numbers/Mpc^3/year \n    - A binning in redshift is used to perform the calculation of the expected\n        number of variables.\n    - It is assumed that the change of rates and volume within a redshift bin\n        is negligible enough that samples to the true distribution may be drawn\n        by obtaining number of variable samples of z from a uniform distribution\n        within the z bin.\n    - The expected number of variables in each of these redshift bins is\n        computed using the rate above at the midpoint of the redshift bin, using\n        a cosmology to compute the comoving volume for the redshift bin\n    - The actual numbers of variables are determined by a Poisson Distribution\n        using the expected number of variables in each redshift bin,\n        determined with a random state passed in as an argument.\n        This number must be integral.\n\n    '

    def __init__(self, rng, cosmo=Planck15, alpha_rate=2.6e-05, beta_rate=1.5, zbin_edges=None, zlower=1e-08, zhigher=1.4, num_bins=20, survey_duration=10.0, sky_area=10.0, sky_fraction=None):
        """
        Basic constructor for class. Parameters are in the class definition.
        """
        self._rng = rng
        self._cosmo = cosmo
        self.alpha_rate = alpha_rate
        self.beta_rate = beta_rate
        self.DeltaT = survey_duration
        self._zsamples = None
        self._set_zbins(zbin_edges, zlower, zhigher, num_bins)
        self._set_skyfraction(sky_area, sky_fraction)
        self._num_sources = None
        _ = self.num_sources_realized

    @property
    def randomState(self):
        if self._rng is None:
            raise ValueError('rng must be provided')
        return self._rng

    @property
    def cosmology(self):
        return self._cosmo

    def _set_skyfraction(self, sky_area, sky_fraction):
        """
        Private helper function to handle the sky_area and sky_fraction
        """
        if bool(sky_fraction and sky_area):
            raise AssertionError('Both `sky_fraction` and `sky_area` cannot be specified')
        assert bool(sky_fraction or sky_area), 'At least one of `sky_fraction` and `sky_area` have to be specified'
        if sky_fraction is None:
            self._sky_area = sky_area
            self._sky_fraction = self.sky_area * np.radians(1.0) ** 2.0 / 4.0 / np.pi
        if sky_area is None:
            self._sky_fraction = sky_fraction
            self._sky_area = self.sky_fraction / (np.radians(1.0) ** 2.0 / 4.0 / np.pi)

    @property
    def sky_fraction(self):
        return self._sky_fraction

    @property
    def sky_area(self):
        """
        fraction of the sky
        """
        return self._sky_area

    def _set_zbins(self, zbin_edges, zlower, zhigher, num_bins):
        """
        """
        if zbin_edges is None:
            zbin_edges = np.linspace(zlower, zhigher, num_bins)
        assert len(zbin_edges) > 0
        self.zlower = zbin_edges.min()
        self.zhigher = zbin_edges.max()
        self.num_bins = len(zbin_edges) - 1
        self._zbin_edges = zbin_edges

    @property
    def zbin_edges(self):
        return self._zbin_edges

    def volumetric_rate(self, z):
        """
        The volumetric rate at a redshift z in units of number of TDOs/ comoving
        volume in Mpc^3/yr in rest frame years according to the commonly used
        power-law expression 

        .. math:: rate(z) = \x07lpha (h/0.7)^3 (1.0 + z)^\x08eta
        
        Parameters
        ----------
        z : array-like, mandatory 
            redshifts at which the rate is evaluated

        Examples
        --------
        """
        res = self.alpha_rate * (1.0 + z) ** self.beta_rate
        res *= (self.cosmology.h / 0.7) ** 3.0
        return res

    @staticmethod
    def volume_in_zshell(zbin_edges, cosmo, skyfrac):
        """returns the comoving volume for the redshift shells
        specified by `zbin_edges` for the cosmology `cosmo`
        and sky fraction `skyfrac`

        Paramters
        ---------
        zbin_edges : `np.ndarray` of floats
            edges of the redshift bins/shells.
        cosmo : `astropy.cosmology.cosmology` instance
            cosmology for which the comoving volumes will be
            calculated.
        skyfrac : `np.float`
            The sky fraction (area / total sky area) covered by
            this sample.
        """
        vols = cosmo.comoving_volume(zbin_edges)
        vol = np.diff(vols)
        vol *= skyfrac
        return vol

    @property
    def z_sample_sizes(self):
        """Number of TDO in each redshift bin with the bins being
        defined by the class parameters

        Returns
        -------
        num_in_volshells : `np.ndaray` of floats
            Expected number of objects in volume shells
            defined by the redshift bin edges.
        """
        DeltaT = self.DeltaT
        skyFraction = self.sky_fraction
        zbinEdges = self.zbin_edges
        z_mids = 0.5 * (zbinEdges[1:] + zbinEdges[:-1])
        vol = self.volume_in_zshell(zbinEdges, self.cosmology, self.sky_fraction)
        num_in_vol_shells = vol * self.volumetric_rate(z_mids)
        num_in_vol_shells *= DeltaT / (1.0 + z_mids)
        return num_in_vol_shells.value

    @property
    def num_sources_realized(self):
        """The number of TDO sources realized in each redshift bin set
        through a Poisson sampling of the expected number of sources.
        """
        if self._num_sources is None:
            self._num_sources = self.randomState.poisson(lam=(self.z_sample_sizes))
        return self._num_sources

    @property
    def z_samples(self):
        if self._zsamples is None:
            zbinEdges = self.zbin_edges
            num_sources = self.num_sources_realized
            x = zbinEdges[:-1]
            y = zbinEdges[1:]
            arr = (self.randomState.uniform(low=xx, high=yy, size=zz).tolist() for xx, yy, zz in zip(x, y, num_sources))
            self._zsamples = np.asarray(list((_x for _lst in arr for _x in _lst)))
        return self._zsamples