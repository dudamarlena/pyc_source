# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-6.5-amd64/egg/xps/xps.py
# Compiled at: 2019-06-04 13:19:27
# Size of source mod 2**32: 6830 bytes
"""
xps.py

X-Ray photoelectron spectroscopy (XPS) helper functions to adjust the
machine dependent intensities to Wagner intensities
"""
__author__ = 'David Kalliecharan'
__license__ = 'ISC License'
__status__ = 'Development'
from numpy import log10 as _log10
from numpy import poly1d as _poly1d
from pandas import DataFrame as _DataFrame
photon_energy = {'Mg':1253.6, 
 'Al':1486.6}
mach_param = {'Dalhousie': {'coef':[
                0.9033, -4.0724, 5.0677, 1.1066], 
               'scale':0.01, 
               'work_func':4.6}}

def kinetic_energy(be, hv, psi):
    """Calculates the kinetic energy (KE) with a Mg source (Dalhousie default):

    be  : binding energy (BE [eV])
    psi : Work function (Psi [eV])
    hv  : Phonton energy (h*nu [eV])
    """
    return hv - be - psi


def transmission(ke, pe, a, scale):
    """Dalhousie standard for the Transmission function

    ke    : Kinetic energy (KE [eV])
    pe    : Pass Energy (PE [eV])
    a     : List of coefficients for series expansion, _NOTE_ coefficents are
            reversed such that (aN, ..., a0) -> aN*x**N + ... + a0
            See documentation on numpy.poly1d
    scale : required scaling factor according to Avantage software
    """
    f = _poly1d(a)
    x = _log10(ke / pe)
    y = f(x)
    return scale * pe * 10 ** y


def sf_machine(sf_wagner, transmission_mach, transmission_wagner):
    """Sensitivity factor for XPS machine correction from the Wagner XPS machine

    sf_wagner              : Wagner sensitivity factor
    transmission_mach      : Transmission function for the selected element
    transmission_wagner    : Wagner transmission function for the selected
                             element.
                             Proportional to 1/(kinetic_energy) [1/eV]
    """
    return sf_wagner * transmission_mach / transmission_wagner


def peak_correction(peak_area, sf_machine):
    """Corrected intensity of peak fitting by scaling to the sensitivity
    factor of the machine.

    peak_area   : peak area [CPS*eV]
    sf_machine  : sensitivity factor of xps machine
    """
    return peak_area / sf_machine


def matrix_factor(mfp_a, mfp_b, mfp_matrix_a, mfp_matrix_b, rho_a, rho_b):
    """Determines the matrix multiplicity factor. Mean free path values can be
found using an external program QUASES-IMFP-TPP2M.

    mfp_a        : Mean free path (mfp) of a in bulk, eg. mfp_a(KE_{Mn 2p3/2})
    mfp_b        : Mean free path (mfp) of b in bulk, eg. mfp_b(KE_{Co 2p3/2})
    mfp_matrix_a : Mean free path of matrix with kinetic energy of a
                   mfp_matirx(KE_{Mn 2p3/2})
    mfp_matrix_b : Mean free path of matrix with kinetic energy of b
                   mfp_matirx(KE_{Co 2p3/2})
    rho_a        : Density of species a
    rho_b        : Density of species b
    """
    a = mfp_matrix_a / mfp_a / rho_a
    b = mfp_matrix_b / mfp_b / rho_b
    return a / b


class XPSPeak:
    __doc__ = 'XPSPeakBase class that conveniently wraps the base functions into an object\n    peak_id    : Peak ID label\n    be         : Binding energy [eV]\n    peak_area  : Area of peak [CPS*eV]\n    sf_wag     : Wagner sensitivity factor\n    hv         : Photon energy\n    pe         : Pass energy\n    mach_param : Dictionary of XPS machine parameters:\n                 coef      : [aN, aN-1, ..., a1, a0]\n                 work_func : float [eV]\n                 scale     : float\n    '

    def __init__(self, peak_id, be, peak_area, sf_wagner, hv, pe, mach_param, *args, **kws):
        self._XPSPeak__peak_id = peak_id
        self._XPSPeak__be = be
        self._XPSPeak__peak_area = peak_area
        self._XPSPeak__sf_wagner = sf_wagner
        self._XPSPeak__hv = hv
        self._XPSPeak__pe = pe
        self._XPSPeak__a = mach_param['coef']
        self._XPSPeak__psi = mach_param['work_func']
        self._XPSPeak__scale = mach_param['scale']
        self._XPSPeak__args = args
        self._XPSPeak__kws = kws

    def get_kinetic_energy(self):
        return kinetic_energy(self._XPSPeak__be, self._XPSPeak__hv, self._XPSPeak__psi)

    def get_transmission(self):
        ke = self.get_kinetic_energy()
        return transmission(ke, self._XPSPeak__pe, self._XPSPeak__a, self._XPSPeak__scale)

    def get_sf_machine(self):
        ke = self.get_kinetic_energy()
        transmission_wagner = 1 / ke
        if 'transmission_wagner' in self._XPSPeak__kws:
            self.transmission_wagner = self._XPSPeak__kws['transmission_wagner']
        tx_xps = self.get_transmission()
        return sf_machine(self._XPSPeak__sf_wagner, tx_xps, transmission_wagner)

    def get_peak_correction(self):
        sf_mach = self.get_sf_machine()
        return peak_correction(self._XPSPeak__peak_area, sf_mach)

    def get_mach_params(self):
        params = {'photon_energy':self._XPSPeak__hv, 
         'pass_energy':self._XPSPeak__pe, 
         'coefficients':self._XPSPeak__a, 
         'scale':self._XPSPeak__scale, 
         'work_func':self._XPSPeak__psi}
        return params

    def set_matrix_component(self, mfp, mfp_matrix, rho):
        """
    mfp        : Mean free path (mfp) in bulk, eg. mfp_a(KE_{Mn 2p3/2})
    mfp_matrix : Mean free path of matrix with kinetic energy of a
                   mfp_matirx(KE_{Mn 2p3/2})
    rho        : Density of material
        """
        self._XPSPeak__matrix_component = mfp_matrix / mfp / rho

    def df(self, return_dict=False):
        data_dict = {'peak_id':[
          self._XPSPeak__peak_id], 
         'binding_energy':[
          self._XPSPeak__be], 
         'kinetic_energy':[
          self.get_kinetic_energy()], 
         'transmission_func':[
          self.get_transmission()], 
         'sf_wagner':[
          self._XPSPeak__sf_wagner], 
         'sf_machine':[
          self.get_sf_machine()], 
         'peak':[
          self._XPSPeak__peak_area], 
         'peak_corrected':[
          self.get_peak_correction()]}
        if hasattr(self, '_XPSPeak__matrix_component'):
            data_dict['matrix_component'] = [
             self._XPSPeak__matrix_component]
        if return_dict == True:
            return data_dict
        else:
            return _DataFrame(data=data_dict)


if __name__ == '__main__':
    pass