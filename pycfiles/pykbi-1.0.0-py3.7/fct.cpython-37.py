# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pykbi/fct.py
# Compiled at: 2018-09-02 04:17:57
# Size of source mod 2**32: 9157 bytes
"""
Fluctuation correlation theory.

This module allow us to work with KBI values. The module currently supports two
cases: 2 and 3 component mixtures.  In both cases, it will calculate the
partial molar volume, isosteric heat, and derivative of the chemical potential.

"""
import numpy as _np
__all__ = [
 'KBdata2comp', 'KBdata3comp']

class KBdata2comp:
    __doc__ = '\n    Using fluctuation correlation theory to calculate properties of a 2 component system.\n\n    param: G11: G11 parameter\n    param: G22: G22 parameter\n    param: G12: G12 parameter\n    param: c1: concentation of component 1\n    param: c2: concentration of component 2\n\n    '

    def __init__(self, G11, G22, G12, c1, c2):
        self.G11 = G11
        self.G22 = G22
        self.G12 = G12
        self.c1 = c1
        self.c2 = c2
        self.x1 = c1 / (c1 + c2)
        self.x2 = c2 / (c1 + c2)
        self.gamma = None
        self.pmv1 = None
        self.pmv2 = None
        self.dmu2dx2 = None
        self.dmudc1 = None
        self.dmudc2 = None
        self.isothermal_compress = None

    def CalculateProperties(self):
        """
        Calculate properties using KB coeffs
        """
        D12 = self.G11 + self.G22 - 2.0 * self.G12
        F12 = self.G11 * self.G22 - self.G12 ** 2
        denum = self.c1 + self.c2 + self.c1 * self.c2 * D12
        self.gamma = 1.0 - self.x1 * self.c2 * D12 / (1.0 + self.c2 * self.x1 * D12)
        self.pmv1 = ((self.G22 - self.G12) * self.c2 + 1.0) / denum
        self.pmv2 = ((self.G11 - self.G12) * self.c1 + 1.0) / denum
        self.dmu2dx2 = 1.0 / (self.x2 * (1.0 + self.x2 * self.c1 * D12))
        self.dmudc1 = 1.0 / (self.c1 * (1.0 + self.c1 * (self.G11 - self.G12)))
        self.dmudc2 = 1.0 / (self.c2 * (1.0 + self.c2 * (self.G22 - self.G12)))
        self.isothermal_compress = (1.0 + self.c1 * self.G11 + self.c2 * self.G22 + self.c1 * self.c2 * F12) / denum

    def PrintProperties(self):
        """
        Print properties to screen
        """
        print('Thermodynamic factor: {}'.format(self.gamma))
        print('Partial molar volume (Comp. 1): {}'.format(self.pmv1))
        print('Partial molar volume (Comp. 2): {}'.format(self.pmv2))
        print(' Isothermal compressibility (k.T.k_T=): {}'.format(self.isothermal_compress))
        print(' Derivative of chemical potential: dmu_2 / dx2)/(k.T)    : {}'.format(self.dmu2dx2))
        print(' (dmu_1/dc_1)/k.T: {}'.format(self.dmudc1))
        print(' (dmu_2/dc_2)/k.T: {}'.format(self.dmudc2))


class KBdata3comp:
    __doc__ = '\n    param: G11: G11 parameter\n    param: G22: G22 parameter\n    param: G33: G33 parameter\n    param: G12: G12 parameter\n    param: G13: G13 parameter\n    param: G23: G23 parameter\n    param: c1: concentation of component 1\n    param: c2: concentation of component 2\n    param: c3: concentation of component 3\n    '

    def __init__(self, G11, G22, G33, G12, G13, G23, c1, c2, c3):
        self.G11 = G11
        self.G22 = G22
        self.G33 = G33
        self.G12 = G12
        self.G13 = G13
        self.G23 = G23
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.x1 = c1 / (c1 + c2 + c3)
        self.x2 = c2 / (c1 + c2 + c3)
        self.x3 = c3 / (c1 + c2 + c3)
        self.gamma0 = None
        self.gamma1 = None
        self.gamma2 = None
        self.gamma3 = None
        self.pmv0 = None
        self.pmv1 = None
        self.pmv2 = None
        self.isothermal_compress = None
        self.B = None

    def CalculateProperties(self):
        """
        Calculate the properties using the KB coeffs
        """
        D12 = self.G11 * self.G22 - 2.0 * self.G12
        D13 = self.G11 * self.G33 - 2.0 * self.G13
        D23 = self.G22 * self.G33 - 2.0 * self.G23
        D123 = self.G11 * self.G22 + self.G11 * self.G33 + self.G22 * self.G33 + 2.0 * self.G12 * self.G13 + 2.0 * self.G12 * self.G23 + 2.0 * self.G13 * self.G23 - self.G12 ** 2 - self.G13 ** 2 - self.G23 ** 2 - 2.0 * self.G11 * self.G23 - 2.0 * self.G22 * self.G13 - 2.0 * self.G33 * self.G12
        F12 = self.G11 * self.G22 - self.G12 ** 2
        F13 = self.G11 * self.G33 - self.G13 ** 2
        F23 = self.G22 * self.G33 - self.G23 ** 2
        F123 = self.G11 * self.G22 * self.G33 + 2.0 * self.G12 * self.G13 * self.G23 - self.G13 ** 2 * self.G22 - self.G12 ** 2 * self.G33 - self.G23 ** 2 * self.G11
        denum = self.c1 + self.c2 + self.c3 + self.c1 * self.c2 * D12 + self.c1 * self.c3 * D13 + self.c2 * self.c3 * D23 + self.c1 * self.c2 * self.c3 * D123
        eta = self.c1 + self.c2 + self.c3 + self.c1 * self.c2 * D12 + self.c1 * self.c3 * D13 + self.c2 * self.c3 * D23 - 0.25 * self.c1 * self.c2 * self.c3 * (D12 ** 2 + D13 ** 2 + D23 ** 2 - 2.0 * D13 * D23 - 2.0 * D12 * D13 - 2.0 * D12 * D23)
        self.gamma0 = -1.0 * (-self.c2 * self.c3 * self.G22 - self.c2 + 2.0 * self.c2 * self.c3 * self.G23 - self.c2 * self.c3 * self.G33 - self.c3 + (self.c2 * self.G12 - self.c2 * self.G22 - 1.0 + self.c2 * self.G23 - self.c2 * self.G13) * self.c1) / eta
        self.gamma1 = -self.c1 * (self.c2 * self.G12 + self.c3 * self.G12 - self.c2 * self.G13 - self.c3 * self.G13 - self.c2 * self.G22 + self.c2 * self.G23 - self.c3 * self.G23 + self.c3 * self.G33) / eta
        self.gamma2 = self.c2 * (self.c1 * self.G11 - self.c1 * self.G12 - self.c3 * self.G12 - self.c1 * self.G13 + self.c3 * self.G13 + self.c1 * self.G23 + self.c3 * self.G23 - self.c3 * self.G33) / eta
        self.gamma3 = (self.c1 * self.c3 * self.G11 + self.c1 - 2.0 * self.c1 * self.c3 * self.G13 + self.c1 * self.c3 * self.G33 + self.c3 + (self.c1 * self.G11 - self.c1 * self.G12 - self.c1 * self.G13 + 1.0 + self.c1 * self.G23) * self.c2) / eta
        self.pmv0 = (1.0 + self.c2 * (self.G22 - self.G12) + self.c3 * (self.G33 - self.G13) + self.c2 * self.c3 * (-self.G13 * self.G22 + self.G13 * self.G23 - self.G23 ** 2 + self.G22 * self.G33 + self.G12 * self.G23 - self.G12 * self.G33)) / denum
        self.pmv1 = (1.0 + self.c1 * (self.G11 - self.G12) + self.c3 * (self.G33 - self.G23) + self.c1 * self.c3 * (-self.G12 * self.G33 + self.G12 * self.G13 - self.G13 ** 2 + self.G13 * self.G23 + self.G11 * self.G33 - self.G11 * self.G23)) / denum
        self.pmv2 = (1.0 + self.c1 * (self.G11 - self.G13) + self.c2 * (self.G22 - self.G23) + self.c1 * self.c2 * (-self.G13 * self.G22 + self.G12 * self.G13 - self.G12 ** 2 + self.G12 * self.G23 + self.G11 * self.G22 - self.G11 * self.G23)) / denum
        self.isothermal_compress = (1.0 + self.c1 * self.G11 + self.c2 * self.G22 + self.c3 * self.G33 + self.c1 * self.c2 * F12 + self.c1 * self.c3 * F13 + self.c2 * self.c3 * F23 + self.c1 * self.c2 * self.c3 * F123) / denum
        self.B = _np.zeros((3, 3))
        self.B[(0, 0)] = self.c1 + self.c1 ** 2 * self.G11
        self.B[(1, 1)] = self.c2 + self.c2 ** 2 * self.G22
        self.B[(2, 2)] = self.c3 + self.c3 ** 2 * self.G33
        self.B[(0, 1)] = self.c1 * self.c2 * self.G12
        self.B[(0, 2)] = self.c1 * self.c3 * self.G13
        self.B[(1, 0)] = self.c1 * self.c2 * self.G12
        self.B[(1, 2)] = self.c2 * self.c3 * self.G23
        self.B[(2, 0)] = self.c1 * self.c3 * self.G13
        self.B[(2, 1)] = self.c2 * self.c3 * self.G23

    def PrintProperties(self):
        """
        Print properties
        """
        print('Thermodynamic factor:')
        print(' Thermodynamic factor 1: {}'.format(self.gamma0))
        print(' Thermodynamic factor 2: {}'.format(self.gamma1))
        print(' Thermodynamic factor 3: {}'.format(self.gamma2))
        print(' Thermodynamic factor 4: {}'.format(self.gamma3))
        print(' Partial molar volume: ')
        print(' Component 1: {}'.format(self.pmv0))
        print(' Component 2: {}'.format(self.pmv1))
        print(' Component 3: {}'.format(self.pmv2))
        print(' Isothermal compressibility: {}'.format(self.isothermal_compress))
        print(' B-matrix')
        print(_np.array2string((self.B), precision=4, separator=',', suppress_small=True))
        print(' Determinant: %f' % _np.linalg.det(self.B))