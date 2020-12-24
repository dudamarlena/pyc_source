# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/slb.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import numpy as np, scipy.optimize as opt, warnings
try:
    from numba import jit
except ImportError:

    def jit(fn):
        return fn


from . import birch_murnaghan as bm
from . import debye
from . import equation_of_state as eos
from ..tools import bracket

@jit
def _grueneisen_parameter_fast(V_0, volume, gruen_0, q_0):
    """global function with plain parameters so jit will work"""
    x = V_0 / volume
    f = 1.0 / 2.0 * (pow(x, 2.0 / 3.0) - 1.0)
    a1_ii = 6.0 * gruen_0
    a2_iikk = -12.0 * gruen_0 + 36.0 * gruen_0 * gruen_0 - 18.0 * q_0 * gruen_0
    nu_o_nu0_sq = 1.0 + a1_ii * f + 1.0 / 2.0 * a2_iikk * f * f
    return 1.0 / 6.0 / nu_o_nu0_sq * (2.0 * f + 1.0) * (a1_ii + a2_iikk * f)


@jit
def _delta_pressure(x, pressure, temperature, V_0, T_0, Debye_0, n, a1_ii, a2_iikk, b_iikk, b_iikkmm):
    f = 0.5 * (pow(V_0 / x, 2.0 / 3.0) - 1.0)
    debye_temperature = Debye_0 * np.sqrt(1.0 + a1_ii * f + 1.0 / 2.0 * a2_iikk * f * f)
    E_th = debye.thermal_energy(temperature, debye_temperature, n)
    E_th_ref = debye.thermal_energy(T_0, debye_temperature, n)
    nu_o_nu0_sq = 1.0 + a1_ii * f + 1.0 / 2.0 * a2_iikk * f * f
    gr = 1.0 / 6.0 / nu_o_nu0_sq * (2.0 * f + 1.0) * (a1_ii + a2_iikk * f)
    return 1.0 / 3.0 * pow(1.0 + 2.0 * f, 5.0 / 2.0) * (b_iikk * f + 0.5 * b_iikkmm * f * f) + gr * (E_th - E_th_ref) / x - pressure


class SLBBase(eos.EquationOfState):
    """
    Base class for the finite strain-Mie-Grueneiesen-Debye equation of state detailed
    in :cite:`Stixrude2005`.  For the most part the equations are
    all third order in strain, but see further the :class:`burnman.slb.SLB2` and
    :class:`burnman.slb.SLB3` classes.
    """

    def _debye_temperature(self, x, params):
        """
        Finite strain approximation for Debye Temperature [K]
        x = ref_vol/vol
        """
        f = 1.0 / 2.0 * (pow(x, 2.0 / 3.0) - 1.0)
        a1_ii = 6.0 * params['grueneisen_0']
        a2_iikk = -12.0 * params['grueneisen_0'] + 36.0 * pow(params['grueneisen_0'], 2.0) - 18.0 * params['q_0'] * params['grueneisen_0']
        return params['Debye_0'] * np.sqrt(1.0 + a1_ii * f + 1.0 / 2.0 * a2_iikk * f * f)

    def volume_dependent_q(self, x, params):
        """
        Finite strain approximation for :math:`q`, the isotropic volume strain
        derivative of the grueneisen parameter.
        """
        f = 1.0 / 2.0 * (pow(x, 2.0 / 3.0) - 1.0)
        a1_ii = 6.0 * params['grueneisen_0']
        a2_iikk = -12.0 * params['grueneisen_0'] + 36.0 * pow(params['grueneisen_0'], 2.0) - 18.0 * params['q_0'] * params['grueneisen_0']
        nu_o_nu0_sq = 1.0 + a1_ii * f + 1.0 / 2.0 * a2_iikk * f * f
        gr = 1.0 / 6.0 / nu_o_nu0_sq * (2.0 * f + 1.0) * (a1_ii + a2_iikk * f)
        if np.abs(params['grueneisen_0']) < 1e-10:
            q = 1.0 / 9.0 * (18.0 * gr - 6.0)
        else:
            q = 1.0 / 9.0 * (18.0 * gr - 6.0 - 1.0 / 2.0 / nu_o_nu0_sq * (2.0 * f + 1.0) * (2.0 * f + 1.0) * a2_iikk / gr)
        return q

    def _isotropic_eta_s(self, x, params):
        """
        Finite strain approximation for :math:`eta_{s0}`, the isotropic shear
        strain derivative of the grueneisen parameter.
        """
        f = 1.0 / 2.0 * (pow(x, 2.0 / 3.0) - 1.0)
        a2_s = -2.0 * params['grueneisen_0'] - 2.0 * params['eta_s_0']
        a1_ii = 6.0 * params['grueneisen_0']
        a2_iikk = -12.0 * params['grueneisen_0'] + 36.0 * pow(params['grueneisen_0'], 2.0) - 18.0 * params['q_0'] * params['grueneisen_0']
        nu_o_nu0_sq = 1.0 + a1_ii * f + 1.0 / 2.0 * a2_iikk * pow(f, 2.0)
        gr = 1.0 / 6.0 / nu_o_nu0_sq * (2.0 * f + 1.0) * (a1_ii + a2_iikk * f)
        eta_s = -gr - 1.0 / 2.0 * pow(nu_o_nu0_sq, -1.0) * pow(2.0 * f + 1.0, 2.0) * a2_s
        return eta_s

    def _thermal_pressure(self, T, V, params):
        Debye_T = self._debye_temperature(params['V_0'] / V, params)
        gr = self.grueneisen_parameter(0.0, T, V, params)
        P_th = gr * debye.thermal_energy(T, Debye_T, params['n']) / V
        return P_th

    def volume(self, pressure, temperature, params):
        """
        Returns molar volume. :math:`[m^3]`
        """
        T_0 = params['T_0']
        Debye_0 = params['Debye_0']
        V_0 = params['V_0']
        n = params['n']
        a1_ii = 6.0 * params['grueneisen_0']
        a2_iikk = -12.0 * params['grueneisen_0'] + 36.0 * pow(params['grueneisen_0'], 2.0) - 18.0 * params['q_0'] * params['grueneisen_0']
        b_iikk = 9.0 * params['K_0']
        b_iikkmm = 27.0 * params['K_0'] * (params['Kprime_0'] - 4.0)
        args = (
         pressure, temperature, V_0, T_0,
         Debye_0, n, a1_ii, a2_iikk, b_iikk, b_iikkmm)
        try:
            sol = bracket(_delta_pressure, params['V_0'], 0.01 * params['V_0'], args)
        except ValueError:
            raise Exception('Cannot find a volume, perhaps you are outside of the range of validity for the equation of state?')

        return opt.brentq(_delta_pressure, sol[0], sol[1], args=args)

    def pressure(self, temperature, volume, params):
        """
        Returns the pressure of the mineral at a given temperature and volume [Pa]
        """
        debye_T = self._debye_temperature(params['V_0'] / volume, params)
        gr = self.grueneisen_parameter(0.0, temperature, volume, params)
        E_th = debye.thermal_energy(temperature, debye_T, params['n'])
        E_th_ref = debye.thermal_energy(params['T_0'], debye_T, params['n'])
        b_iikk = 9.0 * params['K_0']
        b_iikkmm = 27.0 * params['K_0'] * (params['Kprime_0'] - 4.0)
        f = 0.5 * (pow(params['V_0'] / volume, 2.0 / 3.0) - 1.0)
        P = 1.0 / 3.0 * pow(1.0 + 2.0 * f, 5.0 / 2.0) * (b_iikk * f + 0.5 * b_iikkmm * pow(f, 2.0)) + gr * (E_th - E_th_ref) / volume
        return P

    def grueneisen_parameter(self, pressure, temperature, volume, params):
        """
        Returns grueneisen parameter :math:`[unitless]`
        """
        return _grueneisen_parameter_fast(params['V_0'], volume, params['grueneisen_0'], params['q_0'])

    def isothermal_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns isothermal bulk modulus :math:`[Pa]`
        """
        T_0 = params['T_0']
        debye_T = self._debye_temperature(params['V_0'] / volume, params)
        gr = self.grueneisen_parameter(pressure, temperature, volume, params)
        E_th = debye.thermal_energy(temperature, debye_T, params['n'])
        E_th_ref = debye.thermal_energy(T_0, debye_T, params['n'])
        C_v = debye.heat_capacity_v(temperature, debye_T, params['n'])
        C_v_ref = debye.heat_capacity_v(T_0, debye_T, params['n'])
        q = self.volume_dependent_q(params['V_0'] / volume, params)
        K = bm.bulk_modulus(volume, params) + (gr + 1.0 - q) * (gr / volume) * (E_th - E_th_ref) - pow(gr, 2.0) / volume * (C_v * temperature - C_v_ref * T_0)
        return K

    def adiabatic_bulk_modulus(self, pressure, temperature, volume, params):
        """
        Returns adiabatic bulk modulus. :math:`[Pa]`
        """
        K_T = self.isothermal_bulk_modulus(pressure, temperature, volume, params)
        alpha = self.thermal_expansivity(pressure, temperature, volume, params)
        gr = self.grueneisen_parameter(pressure, temperature, volume, params)
        K_S = K_T * (1.0 + gr * alpha * temperature)
        return K_S

    def shear_modulus(self, pressure, temperature, volume, params):
        """
        Returns shear modulus. :math:`[Pa]`
        """
        T_0 = params['T_0']
        debye_T = self._debye_temperature(params['V_0'] / volume, params)
        eta_s = self._isotropic_eta_s(params['V_0'] / volume, params)
        E_th = debye.thermal_energy(temperature, debye_T, params['n'])
        E_th_ref = debye.thermal_energy(T_0, debye_T, params['n'])
        if self.order == 2:
            return bm.shear_modulus_second_order(volume, params) - eta_s * (E_th - E_th_ref) / volume
        if self.order == 3:
            return bm.shear_modulus_third_order(volume, params) - eta_s * (E_th - E_th_ref) / volume
        raise NotImplementedError('')

    def heat_capacity_v(self, pressure, temperature, volume, params):
        """
        Returns heat capacity at constant volume. :math:`[J/K/mol]`
        """
        debye_T = self._debye_temperature(params['V_0'] / volume, params)
        return debye.heat_capacity_v(temperature, debye_T, params['n'])

    def heat_capacity_p(self, pressure, temperature, volume, params):
        """
        Returns heat capacity at constant pressure. :math:`[J/K/mol]`
        """
        alpha = self.thermal_expansivity(pressure, temperature, volume, params)
        gr = self.grueneisen_parameter(pressure, temperature, volume, params)
        C_v = self.heat_capacity_v(pressure, temperature, volume, params)
        C_p = C_v * (1.0 + gr * alpha * temperature)
        return C_p

    def thermal_expansivity(self, pressure, temperature, volume, params):
        """
        Returns thermal expansivity. :math:`[1/K]`
        """
        C_v = self.heat_capacity_v(pressure, temperature, volume, params)
        gr = self.grueneisen_parameter(pressure, temperature, volume, params)
        K = self.isothermal_bulk_modulus(pressure, temperature, volume, params)
        alpha = gr * C_v / K / volume
        return alpha

    def gibbs_free_energy(self, pressure, temperature, volume, params):
        """
        Returns the Gibbs free energy at the pressure and temperature of the mineral [J/mol]
        """
        G = self.helmholtz_free_energy(pressure, temperature, volume, params) + pressure * volume
        return G

    def internal_energy(self, pressure, temperature, volume, params):
        """
        Returns the internal energy at the pressure and temperature of the mineral [J/mol]
        """
        return self.helmholtz_free_energy(pressure, temperature, volume, params) + temperature * self.entropy(pressure, temperature, volume, params)

    def entropy(self, pressure, temperature, volume, params):
        """
        Returns the entropy at the pressure and temperature of the mineral [J/K/mol]
        """
        Debye_T = self._debye_temperature(params['V_0'] / volume, params)
        S = debye.entropy(temperature, Debye_T, params['n'])
        return S

    def enthalpy(self, pressure, temperature, volume, params):
        """
        Returns the enthalpy at the pressure and temperature of the mineral [J/mol]
        """
        return self.helmholtz_free_energy(pressure, temperature, volume, params) + temperature * self.entropy(pressure, temperature, volume, params) + pressure * volume

    def helmholtz_free_energy(self, pressure, temperature, volume, params):
        """
        Returns the Helmholtz free energy at the pressure and temperature of the mineral [J/mol]
        """
        x = params['V_0'] / volume
        f = 1.0 / 2.0 * (pow(x, 2.0 / 3.0) - 1.0)
        Debye_T = self._debye_temperature(params['V_0'] / volume, params)
        F_quasiharmonic = debye.helmholtz_free_energy(temperature, Debye_T, params['n']) - debye.helmholtz_free_energy(params['T_0'], Debye_T, params['n'])
        b_iikk = 9.0 * params['K_0']
        b_iikkmm = 27.0 * params['K_0'] * (params['Kprime_0'] - 4.0)
        F = params['F_0'] + 0.5 * b_iikk * f * f * params['V_0'] + 1.0 / 6.0 * params['V_0'] * b_iikkmm * f * f * f + F_quasiharmonic
        return F

    def validate_parameters(self, params):
        """
        Check for existence and validity of the parameters
        """
        if 'T_0' not in params:
            params['T_0'] = 300.0
        if 'eta_s_0' not in params:
            params['eta_s_0'] = float('nan')
        if 'F_0' not in params:
            params['F_0'] = float('nan')
        bm.BirchMurnaghanBase.validate_parameters(bm.BirchMurnaghanBase(), params)
        expected_keys = [
         'molar_mass', 'n', 'Debye_0', 'grueneisen_0', 'q_0', 'eta_s_0']
        for k in expected_keys:
            if k not in params:
                raise KeyError('params object missing parameter : ' + k)

        if params['T_0'] < 0.0:
            warnings.warn('Unusual value for T_0', stacklevel=2)
        if params['molar_mass'] < 0.001 or params['molar_mass'] > 10.0:
            warnings.warn('Unusual value for molar_mass', stacklevel=2)
        if params['n'] < 1.0 or params['n'] > 1000.0:
            warnings.warn('Unusual value for n', stacklevel=2)
        if params['Debye_0'] < 1.0 or params['Debye_0'] > 10000.0:
            warnings.warn('Unusual value for Debye_0', stacklevel=2)
        if params['grueneisen_0'] < -0.005 or params['grueneisen_0'] > 10.0:
            warnings.warn('Unusual value for grueneisen_0', stacklevel=2)
        if params['q_0'] < -10.0 or params['q_0'] > 10.0:
            warnings.warn('Unusual value for q_0', stacklevel=2)
        if params['eta_s_0'] < -10.0 or params['eta_s_0'] > 10.0:
            warnings.warn('Unusual value for eta_s_0', stacklevel=2)


class SLB3(SLBBase):
    """
    SLB equation of state with third order finite strain expansion for the
    shear modulus (this should be preferred, as it is more thermodynamically
    consistent.)
    """

    def __init__(self):
        self.order = 3


class SLB2(SLBBase):
    """
    SLB equation of state with second order finite strain expansion for the
    shear modulus.  In general, this should not be used, but sometimes
    shear modulus data is fit to a second order equation of state.  In that
    case, you should use this.  The moral is, be careful!
    """

    def __init__(self):
        self.order = 2