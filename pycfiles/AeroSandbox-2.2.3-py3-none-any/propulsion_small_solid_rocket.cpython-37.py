# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\projects\github\aerosandbox\aerosandbox\library\propulsion_small_solid_rocket.py
# Compiled at: 2020-02-21 18:38:54
# Size of source mod 2**32: 7429 bytes
import casadi as cas, numpy as np
n = 0.402
lamb = 6.2
a_0 = 3.9444999999999997 * 1000000.0 ** (-n) * 0.001
strand_reduction_factor = 0.8695652173913044
zeta_c_star = 0.9
chamber_pressure_max = 2000000.0
W_OM_VALID_RANGE = (0, 0.22)
OUT_OF_RANGE_ERROR_STRING = '{:.3f} is outside the model valid range of {:.3f} <= w_om <= {:.3f}'

def burn_rate_coefficient(oxamide_fraction):
    """Burn rate vs oxamide content model.
    Valid from 0% to 15% oxamide. # TODO IMPLEMENT THIS

    Returns:
        a: propellant burn rate coefficient
            [units: pascal**(-n) meter second**-1].
    """
    oxamide_fraction = cas.fmax(oxamide_fraction, 0)
    return a_0 * (1 - oxamide_fraction) / (1 + lamb * oxamide_fraction)


def c_star(oxamide_fraction):
    """Characteristic velocity vs. oxamide content model.
    Valid from 0% to 15% oxamide. # TODO IMPLEMENT THIS

    Returns:
        c_star: ideal characteristic velocity [units: meter second**-1].
    """
    coefs = [
     1380.28, -989.19, -657.7]
    return coefs[0] + coefs[1] * oxamide_fraction + coefs[2] * oxamide_fraction ** 2


def dubious_min_combustion_pressure(oxamide_fraction):
    """Minimum pressure for stable combustion vs. oxamide content model.

    Note: this model is of DUBIOUS accuracy. Don't trust it.
    """
    coefs = [
     7.73179444, 0.36088697, 0.00764587936]
    p_min_MPa = coefs[0] * oxamide_fraction ** 2 + coefs[1] * oxamide_fraction + coefs[2]
    p_min = 1000000.0 * p_min_MPa
    return p_min


def gamma(oxamide_fraction):
    """Ratio of specific heats vs. oxamide content model.

    Returns:
        gamma: Exhaust gas ratio of specific heats [units: dimensionless].
    """
    coefs = [
     1.23767512, 0.21940021, -0.37727591]
    return coefs[0] + coefs[1] * oxamide_fraction + coefs[2] * oxamide_fraction ** 2


def expansion_ratio_from_pressure(chamber_pressure, exit_pressure, gamma, oxamide_fraction):
    r"""Find the nozzle expansion ratio from the chamber and exit pressures.

    See :ref:`expansion-ratio-tutorial-label` for a physical description of the
    expansion ratio.

    Reference: Rocket Propulsion Elements, 8th Edition, Equation 3-25

    Arguments:
        chamber_pressure (scalar): Nozzle stagnation chamber pressure [units: pascal].
        exit_pressure (scalar): Nozzle exit static pressure [units: pascal].
        gamma (scalar): Exhaust gas ratio of specific heats [units: dimensionless].

    Returns:
        scalar: Expansion ratio :math:`\epsilon = A_e / A_t` [units: dimensionless]
    """
    chamber_pressure = cas.fmax(chamber_pressure, dubious_min_combustion_pressure(oxamide_fraction))
    chamber_pressure = cas.fmax(chamber_pressure, exit_pressure * 1.5)
    AtAe = ((gamma + 1) / 2) ** (1 / (gamma - 1)) * (exit_pressure / chamber_pressure) ** (1 / gamma) * cas.sqrt((gamma + 1) / (gamma - 1) * (1 - (exit_pressure / chamber_pressure) ** ((gamma - 1) / gamma)))
    er = 1 / AtAe
    return er


def thrust_coefficient(chamber_pressure, exit_pressure, gamma, p_a=None, er=None):
    """Nozzle thrust coefficient, :math:`C_F`.

    The thrust coefficient is a figure of merit for the nozzle expansion process.
    See :ref:`thrust-coefficient-label` for a description of the physical meaning of the
    thrust coefficient.

    Reference: Equation 1-33a in Huzel and Huang.

    Arguments:
        chamber_pressure (scalar): Nozzle stagnation chamber pressure [units: pascal].
        exit_pressure (scalar): Nozzle exit static pressure [units: pascal].
        gamma (scalar): Exhaust gas ratio of specific heats [units: dimensionless].
        p_a (scalar, optional): Ambient pressure [units: pascal]. If None,
            then p_a = exit_pressure.
        er (scalar, optional): Nozzle area expansion ratio [units: dimensionless]. If None,
            then p_a = exit_pressure.

    Returns:
        scalar: The thrust coefficient, :math:`C_F` [units: dimensionless].
    """
    C_F = (2 * gamma ** 2 / (gamma - 1) * (2 / (gamma + 1)) ** ((gamma + 1) / (gamma - 1)) * (1 - (exit_pressure / chamber_pressure) ** ((gamma - 1) / gamma))) ** 0.5
    C_F += er * (exit_pressure - p_a) / chamber_pressure
    return C_F


if __name__ == '__main__':
    import plotly.express as px
    import pandas as pd
    chamber_pressure_inputs = np.logspace(5, 6, 200)
    exit_pressure_inputs = np.logspace(4, 5, 200)
    ox_for_test = 0
    chamber_pressures = []
    exit_pressures = []
    ers = []
    for chamber_pressure in chamber_pressure_inputs:
        for exit_pressure in exit_pressure_inputs:
            chamber_pressures.append(chamber_pressure)
            exit_pressures.append(exit_pressure)
            ers.append(expansion_ratio_from_pressure(chamber_pressure, exit_pressure, gamma(ox_for_test), ox_for_test))

    data = pd.DataFrame({'chamber_pressure':chamber_pressures, 
     'exit_pressure':exit_pressures, 
     'ers':ers})
    px.scatter_3d(data, x='chamber_pressure', y='exit_pressure', z='ers', color='ers', log_x=True, log_y=True, log_z=True).show()