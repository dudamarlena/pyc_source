# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: signaturesimulator/sense/surface/oh1992.py
# Compiled at: 2018-02-20 04:22:40
"""
This module implements the Oh et al. (1992)
empirical surface backscattering model as documented
in Ulaby et al (2014), chapter 10.5

References
----------
Oh et al. (1992): An empirical model and an inversion technique for radar scattering from bare soil surfaces. IEEE TGRS 30(2). 370-381.
"""
import numpy as np, matplotlib.pyplot as plt
from .scatter import SurfaceScatter
from ..core import Fresnel0
from ..core import Reflectivity

class Oh92(SurfaceScatter):

    def __init__(self, eps, ks, theta):
        """
        Parameters
        ----------
        eps : complex
            relative dielectric permitivity
        ks : float
            product of wavenumber and rms height
            be aware that both need to have the same units
        theta : float, ndarray
            incidence angle [rad]
        """
        super(Oh92, self).__init__(eps, ks, theta)
        self.G0 = Fresnel0(self.eps)
        self.G = Reflectivity(self.eps, self.theta)
        self._calc_p()
        self._calc_q()
        self._vv0 = self._calc_vv()
        self.vv = self._vv0
        self.hh = self.p * self._vv0
        self.hv = self.q * self._vv0

    def _calc_p(self):
        a = 1.0 / (3.0 * self.G0.x)
        self.p = (1.0 - (2.0 * self.theta / np.pi) ** a * np.exp(-self.ks)) ** 2.0

    def _calc_q(self):
        self.q = 0.23 * self.G0.x ** 0.5 * (1.0 - np.exp(-self.ks))

    def _calc_vv(self):
        a = 0.7 * (1.0 - np.exp(-0.65 * self.ks ** 1.8))
        b = np.cos(self.theta) ** 3.0 * (self.G.v + self.G.h) / np.sqrt(self.p)
        return a * b

    def plot(self):
        f = plt.figure()
        ax = f.add_subplot(111)
        t = np.rad2deg(self.theta)
        ax.plot(t, 10 * np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10 * np.log10(self.vv), color='red', label='vv')
        ax.plot(t, 10 * np.log10(self.hv), color='green', label='hv')
        ax.grid()
        ax.set_ylim(-25.0, 0.0)
        ax.set_xlim(0.0, 70.0)
        ax.legend()
        ax.set_xlabel('incidence angle [deg]')
        ax.set_ylabel('backscatter [dB]')