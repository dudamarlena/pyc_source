# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/mie_grueneisen_debye.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import numpy as np, scipy.optimize as opt, warnings
from . import equation_of_state as eos
from . import birch_murnaghan as bm
from . import debye
from .. import constants
from ..tools import bracket

class MGDBase(eos.EquationOfState):
    """
    Base class for a generic finite-strain Mie-Grueneisen-Debye
    equation of state.  References for this can be found in many
    places, such as Shim, Duffy and Kenichi (2002) and Jackson and Rigden
    (1996).  Here we mostly follow the appendices of Matas et al (2007).
    Of particular note is the thermal correction to the shear modulus, which
    was developed by Hama and Suito (1998).
    """

    def grueneisen_parameter(self, pressure, temperature, volume, params):
        """
        Returns grueneisen parameter [unitless] as a function of pressure,
        temperature, and volume (EQ B6)
        """
        return self._grueneisen_parameter(params['V_0'] / volume, params)

    def volume(self, pressure, temperature, params):
        """
        Returns volume [m^3] as a function of pressure [Pa] and temperature [K]
        EQ B7
        """
        T_0 = params['T_0']
        func = lambda x: bm.birch_murnaghan(params['V_0'] / x, params) + self._thermal_pressure(temperature, x, params) - self._thermal_pressure(T_0, x, params) - pressure
        try:
            sol = bracket(func, params['V_0'], 0.01 * params['V_0'])
        except:
            raise ValueError('Cannot find a volume, perhaps you are outside of the range of validity for the equation of state?')

        return opt.brentq(func, sol[0], sol[1])

    def isothermal_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns isothermal bulk modulus [Pa] as a function of pressure [Pa],
        temperature [K], and volume [m^3].  EQ B8
        """
        T_0 = params['T_0']
        K_T = bm.bulk_modulus(volume, params) + self._thermal_bulk_modulus(temperature, volume, params) - self._thermal_bulk_modulus(T_0, volume, params)
        return K_T

    def shear_modulus(self, pressure, temperature, volume, params):
        """
        Returns shear modulus [Pa] as a function of pressure [Pa],
        temperature [K], and volume [m^3].  EQ B11
        """
        T_0 = params['T_0']
        if self.order == 2:
            return bm.shear_modulus_second_order(volume, params) + self._thermal_shear_modulus(temperature, volume, params) - self._thermal_shear_modulus(T_0, volume, params)
        if self.order == 3:
            return bm.shear_modulus_third_order(volume, params) + self._thermal_shear_modulus(temperature, volume, params) - self._thermal_shear_modulus(T_0, volume, params)
        raise NotImplementedError('')

    def heat_capacity_v(self, pressure, temperature, volume, params):
        """
        Returns heat capacity at constant volume at the pressure, temperature, and volume [J/K/mol]
        """
        Debye_T = self._debye_temperature(params['V_0'] / volume, params)
        C_v = debye.heat_capacity_v(temperature, Debye_T, params['n'])
        return C_v

    def thermal_expansivity(self, pressure, temperature, volume, params):
        """
        Returns thermal expansivity at the pressure, temperature, and volume [1/K]
        """
        C_v = self.heat_capacity_v(pressure, temperature, volume, params)
        gr = self._grueneisen_parameter(params['V_0'] / volume, params)
        K = self.isothermal_bulk_modulus(pressure, temperature, volume, params)
        alpha = gr * C_v / K / volume
        return alpha

    def heat_capacity_p(self, pressure, temperature, volume, params):
        """
        Returns heat capacity at constant pressure at the pressure, temperature, and volume [J/K/mol]
        """
        alpha = self.thermal_expansivity(pressure, temperature, volume, params)
        gr = self._grueneisen_parameter(params['V_0'] / volume, params)
        C_v = self.heat_capacity_v(pressure, temperature, volume, params)
        C_p = C_v * (1.0 + gr * alpha * temperature)
        return C_p

    def adiabatic_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns adiabatic bulk modulus [Pa] as a function of pressure [Pa],
        temperature [K], and volume [m^3].  EQ D6
        """
        K_T = self.isothermal_bulk_modulus(pressure, temperature, volume, params)
        alpha = self.thermal_expansivity(pressure, temperature, volume, params)
        gr = self._grueneisen_parameter(params['V_0'] / volume, params)
        K_S = K_T * (1.0 + gr * alpha * temperature)
        return K_S

    def pressure(self, temperature, volume, params):
        """
        Returns pressure [Pa] as a function of temperature [K] and volume[m^3]
        EQ B7
        """
        T_0 = params['T_0']
        return bm.birch_murnaghan(params['V_0'] / volume, params) + self._thermal_pressure(temperature, volume, params) - self._thermal_pressure(T_0, volume, params)

    def _thermal_shear_modulus(self, T, V, params):
        if T > 1e-10:
            gr = self._grueneisen_parameter(params['V_0'] / V, params)
            Debye_T = self._debye_temperature(params['V_0'] / V, params)
            G_th = 3.0 / 5.0 * (self._thermal_bulk_modulus(T, V, params) - 6 * constants.gas_constant * T * params['n'] / V * gr * debye.debye_fn(Debye_T / T))
            return G_th
        else:
            return 0.0

    def _debye_temperature(self, x, params):
        return params['Debye_0'] * np.exp((params['grueneisen_0'] - self._grueneisen_parameter(x, params)) / params['q_0'])

    def _grueneisen_parameter(self, x, params):
        return params['grueneisen_0'] * pow(1.0 / x, params['q_0'])

    def _thermal_pressure(self, T, V, params):
        Debye_T = self._debye_temperature(params['V_0'] / V, params)
        gr = self._grueneisen_parameter(params['V_0'] / V, params)
        P_th = gr * debye.thermal_energy(T, Debye_T, params['n']) / V
        return P_th

    def _thermal_bulk_modulus(self, T, V, params):
        if T > 1e-10:
            gr = self._grueneisen_parameter(params['V_0'] / V, params)
            Debye_T = self._debye_temperature(params['V_0'] / V, params)
            K_th = 3.0 * params['n'] * constants.gas_constant * T / V * gr * ((1.0 - params['q_0'] - 3.0 * gr) * debye.debye_fn(Debye_T / T) + 3.0 * gr * (Debye_T / T) / (np.exp(Debye_T / T) - 1.0))
            return K_th
        else:
            return 0.0

    def validate_parameters(self, params):
        """
        Check for existence and validity of the parameters
        """
        if 'T_0' not in params:
            params['T_0'] = 300.0
        bm.BirchMurnaghanBase.validate_parameters(bm.BirchMurnaghanBase(), params)
        expected_keys = [
         'molar_mass', 'n', 'Debye_0', 'grueneisen_0', 'q_0']
        for k in expected_keys:
            if k not in params:
                raise KeyError('params object missing parameter : ' + k)

        if params['T_0'] < 0.0:
            warnings.warn('Unusual value for T_0', stacklevel=2)
        if params['molar_mass'] < 0.001 or params['molar_mass'] > 1.0:
            warnings.warn('Unusual value for molar_mass', stacklevel=2)
        if params['n'] < 1.0 or params['n'] > 1000.0:
            warnings.warn('Unusual value for n', stacklevel=2)
        if params['Debye_0'] < 1.0 or params['Debye_0'] > 10000.0:
            warnings.warn('Unusual value for Debye_0', stacklevel=2)
        if params['grueneisen_0'] < 0.0 or params['grueneisen_0'] > 10.0:
            warnings.warn('Unusual value for grueneisen_0', stacklevel=2)
        if params['q_0'] < -10.0 or params['q_0'] > 10.0:
            warnings.warn('Unusual value for q_0', stacklevel=2)


class MGD3(MGDBase):
    """
    MGD equation of state with third order finite strain expansion for the
    shear modulus (this should be preferred, as it is more thermodynamically
    consistent.
    """

    def __init__(self):
        self.order = 3


class MGD2(MGDBase):
    """
    MGD equation of state with second order finite strain expansion for the
    shear modulus.  In general, this should not be used, but sometimes
    shear modulus data is fit to a second order equation of state.  In that
    case, you should use this.  The moral is, be careful!
    """

    def __init__(self):
        self.order = 2