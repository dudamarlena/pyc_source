# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: signaturesimulator/sense/scatterer.py
# Compiled at: 2018-02-20 04:22:40
"""
Definition of scatter types
"""
import numpy as np

class Scatterer(object):

    def __init__(self, **kwargs):
        self.sigma_s_hh = kwargs.get('sigma_s_hh', None)
        assert self.sigma_s_hh is not None, 'Particle HH scattering cross section needs to be specified [m**-2]'
        self.sigma_s_vv = kwargs.get('sigma_s_vv', None)
        assert self.sigma_s_vv is not None, 'Particle VV scattering cross section needs to be specified [m**-2]'
        self.sigma_s_hv = kwargs.get('sigma_s_hv', None)
        assert self.sigma_s_hv is not None, 'Particle HV scattering cross section needs to be specified [m**-2]'
        return


class ScatIso(Scatterer):
    """
    Isotropic scatterer definition
    see 11.2 in Ulaby (2014)
    """

    def __init__(self, **kwargs):
        super(ScatIso, self).__init__(**kwargs)
        assert self.sigma_s_hh == self.sigma_s_vv
        assert self.sigma_s_hh == self.sigma_s_hv

    def sigma_v_back(self):
        """
        volume backscattering coefficient
        for the isotropic case this corresponds to the
        volume scattering coefficient ks

        not that this is NOT the scattering cross section of a single particle!
        """
        return {'hh': self.sigma_s_hh, 'vv': self.sigma_s_vv, 'hv': self.sigma_s_hv}

    def sigma_v_bist(self):
        return self.sigma_v_back()


class ScatRayleigh(Scatterer):
    """
    Isotropic scatterer definition
    see 11.2 in Ulaby (2014)
    """

    def __init__(self, **kwargs):
        super(ScatRayleigh, self).__init__(**kwargs)

    def sigma_v_back(self):
        return {'hh': 1.5 * self.sigma_s_hh, 'vv': 1.5 * self.sigma_s_vv, 'hv': np.nan}

    def sigma_v_bist(self):
        return self.sigma_v_back()