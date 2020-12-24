# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: signaturesimulator/sense/core.py
# Compiled at: 2018-02-20 04:22:40
import numpy as np, matplotlib.pyplot as plt

class Fresnel0(object):

    def __init__(self, e):
        """
        calculate the Nadir Fresnel reflectivity
        e.g. Ulaby (2014), eq. 10.36

        Parameters
        ----------
        e : complex
            complex relative dielectric permitivity
        """
        self.x = self._calc(e)

    def _calc(self, e):
        return np.abs((1.0 - np.sqrt(e)) / (1.0 + np.sqrt(e))) ** 2.0


class Reflectivity(object):
    """
    calculate the reflectivity for H and V polarization
    """

    def __init__(self, eps, theta):
        """
        table 2.5 Ulaby (2014)
        assumes specular surface
        Parameters
        ----------
        eps : complex
            relative dielectric permitivity
        theta : float, ndarray
            incidence angle [rad]
            can be specified
        """
        self.eps = eps
        self.theta = theta
        self._calc_reflection_coefficients()
        self.v = np.abs(self.rho_v) ** 2.0
        self.h = np.abs(self.rho_h) ** 2.0

    def _calc_reflection_coefficients(self):
        """
        calculate reflection coefficients
        Woodhouse, 2006; Eq. 5.54, 5.55
        """
        co = np.cos(self.theta)
        si2 = np.sin(self.theta) ** 2.0
        self.rho_v = (self.eps * co - np.sqrt(self.eps - si2)) / (self.eps * co + np.sqrt(self.eps - si2))
        self.rho_h = (co - np.sqrt(self.eps - si2)) / (co + np.sqrt(self.eps - si2))

    def plot(self):
        f = plt.figure()
        ax = f.add_subplot(111)
        ax.plot(np.rad2deg(self.theta), self.v, color='red', linestyle='-', label='V')
        ax.plot(np.rad2deg(self.theta), self.h, color='blue', linestyle='--', label='H')
        ax.grid()
        ax.legend()