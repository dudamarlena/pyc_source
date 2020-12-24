# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: signaturesimulator/sense/surface/dubois95.py
# Compiled at: 2018-02-20 04:22:40
"""
implements the Dubois95 model
as described in Ulaby (2014), Chapter 10.6
"""
import numpy as np, matplotlib.pyplot as plt
from .scatter import SurfaceScatter

class Dubois95(SurfaceScatter):

    def __init__(self, eps, ks, theta, lam=None):
        """
        Parameters
        ----------
        lam : float
            wavelength in meter
        """
        super(Dubois95, self).__init__(eps, ks, theta)
        self.lam = lam
        assert self.lam is not None
        self.vv, self.hh = self._calc_sigma()
        self.hv = None
        return

    def _calc_sigma(self):
        lam = self.lam * 100.0
        ks = self.ks / 100
        return (self._vv(lam, ks), self._hh(lam, ks))

    def _hh(self, lam, ks):
        """
        lam : float
            wavelength in cm
        """
        a = 0.0017782794100389228 * np.cos(self.theta) ** 1.5 / np.sin(self.theta) ** 5.0
        c = 10.0 ** (0.028 * np.real(self.eps) * np.tan(self.theta))
        d = (ks * np.sin(self.theta)) ** 1.4 * lam ** 0.7
        return a * c * d

    def _vv(self, lam, ks):
        """ eq. 10.41b """
        b = 0.0044668359215096305 * (np.cos(self.theta) ** 3.0 / np.sin(self.theta) ** 3.0)
        c = 10.0 ** (0.046 * np.real(self.eps) * np.tan(self.theta))
        d = (ks * np.sin(self.theta)) ** 1.1 * lam ** 0.7
        return b * c * d

    def plot(self):
        f = plt.figure()
        ax = f.add_subplot(111)
        t = np.rad2deg(self.theta)
        ax.plot(t, 10.0 * np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10.0 * np.log10(self.vv), color='red', label='vv')
        ax.grid()
        ax.set_ylim(-35.0, -5.0)
        ax.set_xlim(30.0, 70.0)
        ax.legend()
        ax.set_xlabel('incidence angle [deg]')
        ax.set_ylabel('backscatter [dB]')