# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/birch_murnaghan_4th.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import scipy.optimize as opt
from . import equation_of_state as eos
from ..tools import bracket
import warnings

def bulk_modulus_fourth(volume, params):
    """
    compute the bulk modulus as per the fourth order
    birch-murnaghan equation of state.  Returns bulk
    modulus in the same units as the reference bulk
    modulus.  Pressure must be in :math:`[Pa]`.
    """
    x = params['V_0'] / volume
    f = 0.5 * (pow(x, 2.0 / 3.0) - 1.0)
    Xi = 3.0 / 4.0 * (4.0 - params['Kprime_0'])
    Zeta = 3.0 / 8.0 * (params['K_0'] * params['Kprime_prime_0'] + params['Kprime_0'] * (params['Kprime_0'] - 7.0) + 143.0 / 9.0)
    K = 5.0 * f * pow(1.0 + 2.0 * f, 5.0 / 2.0) * params['K_0'] * (1.0 - 2.0 * Xi * f + 4.0 * Zeta * pow(f, 2.0)) + pow(1.0 + 2.0 * f, 7.0 / 2.0) * params['K_0'] * (1.0 - 4.0 * Xi * f + 12.0 * Zeta * pow(f, 2.0))
    return K


def volume_fourth_order(pressure, params):
    func = lambda x: birch_murnaghan_fourth(params['V_0'] / x, params) - pressure
    try:
        sol = bracket(func, params['V_0'], 0.01 * params['V_0'])
    except:
        raise ValueError('Cannot find a volume, perhaps you are outside of the range of validity for the equation of state?')

    return opt.brentq(func, sol[0], sol[1])


def birch_murnaghan_fourth(x, params):
    """
    equation for the fourth order birch-murnaghan equation of state, returns
    pressure in the same units that are supplied for the reference bulk
    modulus (params['K_0'])
    """
    f = 0.5 * (pow(x, 2.0 / 3.0) - 1.0)
    Xi = 3.0 / 4.0 * (4.0 - params['Kprime_0'])
    Zeta = 3.0 / 8.0 * (params['K_0'] * params['Kprime_prime_0'] + params['Kprime_0'] * (params['Kprime_0'] - 7.0) + 143.0 / 9.0)
    return 3.0 * f * pow(1.0 + 2.0 * f, 5.0 / 2.0) * params['K_0'] * (1.0 - 2.0 * Xi * f + 4.0 * Zeta * pow(f, 2.0))


class BM4(eos.EquationOfState):
    """
    Base class for the isothermal Birch Murnaghan equation of state.  This is fourth order in strain, and
    has no temperature dependence.
    """

    def volume(self, pressure, temperature, params):
        """
        Returns volume :math:`[m^3]` as a function of pressure :math:`[Pa]`.
        """
        return volume_fourth_order(pressure, params)

    def pressure(self, temperature, volume, params):
        return birch_murnaghan_fourth(volume / params['V_0'], params)

    def isothermal_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns isothermal bulk modulus :math:`K_T` :math:`[Pa]` as a function of pressure :math:`[Pa]`,
        temperature :math:`[K]` and volume :math:`[m^3]`.
        """
        return bulk_modulus_fourth(volume, params)

    def adiabatic_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns adiabatic bulk modulus :math:`K_s` of the mineral. :math:`[Pa]`.
        """
        return bulk_modulus_fourth(volume, params)

    def shear_modulus(self, pressure, temperature, volume, params):
        """
        Returns shear modulus :math:`G` of the mineral. :math:`[Pa]`
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
            params['P_0'] = 0.0
        if 'G_0' not in params:
            params['G_0'] = float('nan')
        if 'Gprime_0' not in params:
            params['Gprime_0'] = float('nan')
        expected_keys = [
         'V_0', 'K_0', 'Kprime_0']
        for k in expected_keys:
            if k not in params:
                raise KeyError('params object missing parameter : ' + k)

        if params['P_0'] < 0.0:
            warnings.warn('Unusual value for P_0', stacklevel=2)
        if params['V_0'] < 1e-07 or params['V_0'] > 0.001:
            warnings.warn('Unusual value for V_0', stacklevel=2)
        if params['K_0'] < 1000000000.0 or params['K_0'] > 10000000000000.0:
            warnings.warn('Unusual value for K_0', stacklevel=2)
        if params['Kprime_0'] < 0.0 or params['Kprime_0'] > 10.0:
            warnings.warn('Unusual value for Kprime_0', stacklevel=2)
        if params['Kprime_prime_0'] > 0.0 or params['Kprime_prime_0'] < -10.0:
            warnings.warn('Unusual value for Kprime_prime_0', stacklevel=2)