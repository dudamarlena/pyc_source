# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/vinet.py
# Compiled at: 2018-03-29 19:08:50
import scipy.optimize as opt
from . import equation_of_state as eos
import warnings
from math import exp

def bulk_modulus(volume, params):
    """
    compute the bulk modulus as per the third order
    Vinet equation of state.  Returns bulk
    modulus in the same units as the reference bulk
    modulus.  Pressure must be in :math:`[Pa]`.
    """
    x = volume / params['V_0']
    eta = 3.0 / 2.0 * (params['Kprime_0'] - 1.0)
    K = params['K_0'] * pow(x, -2.0 / 3.0) * (1 + (eta * pow(x, 1.0 / 3.0) + 1.0) * (1.0 - pow(x, 1.0 / 3.0))) * exp(eta * (1.0 - pow(x, 1.0 / 3.0)))
    return K


def vinet(x, params):
    """
    equation for the third order Vinet equation of state, returns
    pressure in the same units that are supplied for the reference bulk
    modulus (params['K_0'])
    """
    eta = 3.0 / 2.0 * (params['Kprime_0'] - 1.0)
    return 3.0 * params['K_0'] * pow(x, -2.0 / 3.0) * (1.0 - pow(x, 1.0 / 3.0)) * exp(eta * (1.0 - pow(x, 1.0 / 3.0)))


def volume(pressure, params):
    """
    Get the Vinet volume at a reference temperature for a given
    pressure :math:`[Pa]`. Returns molar volume in :math:`[m^3]`
    """
    func = lambda x: vinet(x / params['V_0'], params) - pressure
    V = opt.brentq(func, 0.1 * params['V_0'], 1.5 * params['V_0'])
    return V


class Vinet(eos.EquationOfState):
    """
    Base class for the isothermal Vinet equation of state.  This is third order in strain, and
    has no temperature dependence.
    """

    def volume(self, pressure, temperature, params):
        """
        Returns volume :math:`[m^3]` as a function of pressure :math:`[Pa]`.
        """
        return volume(pressure, params)

    def pressure(self, temperature, volume, params):
        return vinet(volume / params['V_0'], params)

    def isothermal_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns isothermal bulk modulus :math:`K_T` :math:`[Pa]` as a function of pressure :math:`[Pa]`,
        temperature :math:`[K]` and volume :math:`[m^3]`.
        """
        return bulk_modulus(volume, params)

    def adiabatic_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns adiabatic bulk modulus :math:`K_s` of the mineral. :math:`[Pa]`.
        """
        return bulk_modulus(volume, params)

    def shear_modulus(self, pressure, temperature, volume, params):
        """
        Returns shear modulus :math:`G` of the mineral. :math:`[Pa]`
        Currently not included in the Vinet EOS, so omitted.
        """
        return 0.0

    def heat_capacity_v(self, pressure, temperature, volume, params):
        """
        Since this equation of state does not contain temperature effects, simply return a very large number. :math:`[J/K/mol]`
        """
        return 1e+99

    def heat_capacity_p(self, pressure, temperature, volume, params):
        """
        Since this equation of state does not contain temperature effects, simply return a very large number. :math:`[J/K/mol]`
        """
        return 1e+99

    def thermal_expansivity(self, pressure, temperature, volume, params):
        """
        Since this equation of state does not contain temperature effects, simply return zero. :math:`[1/K]`
        """
        return 0.0

    def grueneisen_parameter(self, pressure, temperature, volume, params):
        """
        Since this equation of state does not contain temperature effects, simply return zero. :math:`[unitless]`
        """
        return 0.0

    def validate_parameters(self, params):
        """
        Check for existence and validity of the parameters
        """
        if 'G_0' not in params:
            params['G_0'] = float('nan')
        if 'Gprime_0' not in params:
            params['Gprime_0'] = float('nan')
        expected_keys = [
         'V_0', 'K_0', 'Kprime_0']
        for k in expected_keys:
            if k not in params:
                raise KeyError('params object missing parameter : ' + k)

        if params['V_0'] < 1e-07 or params['V_0'] > 0.001:
            warnings.warn('Unusual value for V_0', stacklevel=2)
        if params['K_0'] < 1000000000.0 or params['K_0'] > 10000000000000.0:
            warnings.warn('Unusual value for K_0', stacklevel=2)
        if params['Kprime_0'] < -5.0 or params['Kprime_0'] > 10.0:
            warnings.warn('Unusual value for Kprime_0', stacklevel=2)