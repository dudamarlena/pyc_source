# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/modified_tait.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import warnings, numpy as np
from . import equation_of_state as eos

def tait_constants(params):
    """
    returns parameters for the modified Tait equation of state
    derived from K_T and its two first pressure derivatives
    EQ 4 from Holland and Powell, 2011
    """
    a = (1.0 + params['Kprime_0']) / (1.0 + params['Kprime_0'] + params['K_0'] * params['Kdprime_0'])
    b = params['Kprime_0'] / params['K_0'] - params['Kdprime_0'] / (1.0 + params['Kprime_0'])
    c = (1.0 + params['Kprime_0'] + params['K_0'] * params['Kdprime_0']) / (params['Kprime_0'] * params['Kprime_0'] + params['Kprime_0'] - params['K_0'] * params['Kdprime_0'])
    return (a, b, c)


def modified_tait(x, params):
    """
    equation for the modified Tait equation of state, returns
    pressure in the same units that are supplied for the reference bulk
    modulus (params['K_0'])
    EQ 2 from Holland and Powell, 2011
    """
    a, b, c = tait_constants(params)
    return (np.power((x + a - 1.0) / a, -1.0 / c) - 1.0) / b + params['P_0']


def volume(pressure, params):
    """
    Returns volume [m^3] as a function of pressure [Pa] and temperature [K]
    EQ 12
    """
    a, b, c = tait_constants(params)
    x = 1 - a * (1.0 - np.power(1.0 + b * (pressure - params['P_0']), -1.0 * c))
    return x * params['V_0']


def bulk_modulus(pressure, params):
    """
    Returns isothermal bulk modulus :math:`K_T` of the mineral. :math:`[Pa]`.
    EQ 13+2
    """
    a, b, c = tait_constants(params)
    return params['K_0'] * (1.0 + b * (pressure - params['P_0'])) * (a + (1.0 - a) * np.power(1.0 + b * (pressure - params['P_0']), c))


class MT(eos.EquationOfState):
    """
    Base class for a generic modified Tait equation of state.
    References for this can be found in Huang and Chow (1974)
    and Holland and Powell (2011; followed here).

    An instance "m" of a Mineral can be assigned this
    equation of state with the command m.set_method('mt')
    (or by initialising the class with the param
    equation_of_state = 'mt').
    """

    def volume(self, pressure, temperature, params):
        """
        Returns volume :math:`[m^3]` as a function of pressure :math:`[Pa]`.
        """
        return volume(pressure, params)

    def pressure(self, temperature, volume, params):
        """
        Returns pressure [Pa] as a function of temperature [K] and volume[m^3]
        """
        return modified_tait(params['V_0'] / volume, params)

    def isothermal_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns isothermal bulk modulus :math:`K_T` of the mineral. :math:`[Pa]`.
        """
        return bulk_modulus(pressure, params)

    def adiabatic_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Since this equation of state does not contain temperature effects, simply return a very large number. :math:`[Pa]`
        """
        return 1e+99

    def shear_modulus(self, pressure, temperature, volume, params):
        """
        Not implemented in the Modified Tait EoS. :math:`[Pa]`
        Returns 0.
        Could potentially apply a fixed Poissons ratio as a rough estimate.
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
        if 'P_0' not in params:
            params['P_0'] = 100000.0
        if 'G_0' not in params:
            params['G_0'] = float('nan')
        if 'Gprime_0' not in params:
            params['Gprime_0'] = float('nan')
        expected_keys = [
         'V_0', 'K_0', 'Kprime_0', 'Kdprime_0', 'G_0', 'Gprime_0']
        for k in expected_keys:
            if k not in params:
                raise KeyError('params object missing parameter : ' + k)

        if params['P_0'] < 0.0:
            warnings.warn('Unusual value for P_0', stacklevel=2)
        if params['V_0'] < 1e-07 or params['V_0'] > 0.01:
            warnings.warn('Unusual value for V_0', stacklevel=2)
        if params['K_0'] < 1000000000.0 or params['K_0'] > 10000000000000.0:
            warnings.warn('Unusual value for K_0', stacklevel=2)
        if params['Kprime_0'] < 0.0 or params['Kprime_0'] > 10.0:
            warnings.warn('Unusual value for Kprime_0', stacklevel=2)
        if params['G_0'] < 0.0 or params['G_0'] > 10000000000000.0:
            warnings.warn('Unusual value for G_0', stacklevel=2)
        if params['Gprime_0'] < -5.0 or params['Gprime_0'] > 10.0:
            warnings.warn('Unusual value for Gprime_0', stacklevel=2)