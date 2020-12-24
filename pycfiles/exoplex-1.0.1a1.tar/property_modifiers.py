# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/property_modifiers.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import numpy as np, scipy.optimize as opt
from ..constants import gas_constant

def _landau_excesses(pressure, temperature, params):
    """
    Applies a tricritical Landau correction to the properties
    of an endmember which undergoes a displacive phase transition.
    This correction follows Putnis (1992), and is done relative to
    the completely *ordered* state (at 0 K).
    It therefore differs in implementation from both
    Stixrude and Lithgow-Bertelloni (2011) and
    Holland and Powell (2011), who compute properties relative to
    the completely disordered state and standard states respectively.

    The current implementation is preferred, as the excess
    entropy (and heat capacity) terms are equal to zero at 0 K.

    N.B. The excesses are for a *completely relaxed* mineral;
    for example, seismic wave propagation is *slow* compared to the
    rate of reaction.
    """
    Tc = params['Tc_0'] + params['V_D'] * pressure / params['S_D']
    G_disordered = -params['S_D'] * (temperature - Tc + params['Tc_0'] / 3.0)
    dGdT_disordered = -params['S_D']
    dGdP_disordered = params['V_D']
    if temperature < Tc:
        Q2 = np.sqrt(1.0 - temperature / Tc)
        G = params['S_D'] * ((temperature - Tc) * Q2 + params['Tc_0'] * Q2 * Q2 * Q2 / 3.0) + G_disordered
        dGdP = -params['V_D'] * Q2 * (1.0 + 0.5 * temperature / Tc * (1.0 - params['Tc_0'] / Tc)) + dGdP_disordered
        dGdT = params['S_D'] * Q2 * (1.5 - 0.5 * params['Tc_0'] / Tc) + dGdT_disordered
        d2GdP2 = params['V_D'] * params['V_D'] * temperature / (params['S_D'] * Tc * Tc * Q2) * (temperature * (1.0 + params['Tc_0'] / Tc) / (4.0 * Tc) + Q2 * Q2 * (1.0 - params['Tc_0'] / Tc) - 1.0)
        d2GdT2 = -params['S_D'] / (Tc * Q2) * (0.75 - 0.25 * params['Tc_0'] / Tc)
        d2GdPdT = params['V_D'] / (2.0 * Tc * Q2) * (1.0 + (temperature / (2.0 * Tc) - Q2 * Q2) * (1.0 - params['Tc_0'] / Tc))
    else:
        G = G_disordered
        dGdT = dGdT_disordered
        dGdP = dGdP_disordered
        d2GdT2 = 0.0
        d2GdP2 = 0.0
        d2GdPdT = 0.0
    excesses = {'G': G, 'dGdT': dGdT, 'dGdP': dGdP, 'd2GdT2': d2GdT2, 
       'd2GdP2': d2GdP2, 'd2GdPdT': d2GdPdT}
    return excesses


def _landau_hp_excesses(pressure, temperature, params):
    """
    Applies a tricritical Landau correction to the properties
    of an endmember which undergoes a displacive phase transition.
    This correction is done relative to the standard state, as per
    Holland and Powell (1998).

    Includes the correction published within landaunote.pdf
    (Holland, pers. comm), which 'corrects' the terms involving
    the critical temperature Tc / Tc*

    Note that this formalism is still inconsistent, as it predicts that
    the order parameter can be greater than one. For this reason
    _landau_excesses is preferred.

    N.B. The excesses are for a *completely relaxed* mineral;
    i.e. the seismic wave propagation is *slow* compared to the
    rate of reaction.
    """
    P = pressure
    T = temperature
    if params['T_0'] < params['Tc_0']:
        Q_0 = np.power((params['Tc_0'] - params['T_0']) / params['Tc_0'], 0.25)
    else:
        Q_0 = 0.0
    Tc = params['Tc_0'] + params['V_D'] * (P - params['P_0']) / params['S_D']
    if T < Tc:
        Q = np.power((Tc - T) / params['Tc_0'], 0.25)
    else:
        Q = 0.0
    G = params['Tc_0'] * params['S_D'] * (Q_0 * Q_0 - np.power(Q_0, 6.0) / 3.0) - params['S_D'] * (Tc * Q * Q - params['Tc_0'] * np.power(Q, 6.0) / 3.0) - T * params['S_D'] * (Q_0 * Q_0 - Q * Q) + (P - params['P_0']) * params['V_D'] * Q_0 * Q_0
    dGdT = params['S_D'] * (Q * Q - Q_0 * Q_0)
    dGdP = -params['V_D'] * (Q * Q - Q_0 * Q_0)
    if Q > 1e-12:
        d2GdT2 = -params['S_D'] / (2.0 * params['Tc_0'] * Q * Q)
        d2GdP2 = -params['V_D'] * params['V_D'] / (2.0 * params['S_D'] * params['Tc_0'] * Q * Q)
        d2GdPdT = params['V_D'] / (2.0 * params['Tc_0'] * Q * Q)
    else:
        d2GdT2 = 0.0
        d2GdP2 = 0.0
        d2GdPdT = 0.0
    excesses = {'G': G, 'dGdT': dGdT, 'dGdP': dGdP, 'd2GdT2': d2GdT2, 
       'd2GdP2': d2GdP2, 'd2GdPdT': d2GdPdT}
    return excesses


def _linear_excesses(pressure, temperature, params):
    """
    Applies a 'Darken's quadratic formalism' correction (Powell, 1987)
    to the thermodynamic properties of a mineral endmember.
    This correction is relative to P = 0 and T = 0 and linear in P and T
    and therefore corresponds to a constant volume and entropy correction.

    Applying either a volume or entropy term will generally break
    equations of state (i.e. the properties of the mineral will
    no longer obey the equation of state defined in the
    params dictionary. However, this form of excess is extremely
    useful as a first order tweak to free energies
    (especially in solid solution calculations)
    """
    G = params['delta_E'] - temperature * params['delta_S'] + pressure * params['delta_V']
    dGdT = -params['delta_S']
    dGdP = params['delta_V']
    d2GdT2 = 0.0
    d2GdP2 = 0.0
    d2GdPdT = 0.0
    excesses = {'G': G, 'dGdT': dGdT, 'dGdP': dGdP, 'd2GdT2': d2GdT2, 
       'd2GdP2': d2GdP2, 'd2GdPdT': d2GdPdT}
    return excesses


def _bragg_williams_excesses(pressure, temperature, params):
    """
    Applies a Bragg-Williams type correction to the thermodynamic
    properties of a mineral endmember. Used for modelling
    order-disorder processes.
    Expressions are from Holland and Powell (1996).

    N.B. The excesses are for a *completely relaxed* mineral;
    i.e. the seismic wave propagation is *slow* compared to the
    rate of reaction.

    This may not be reasonable for order-disorder, especially
    for slow or coupled diffusers (Si-Al, for example).
    The completely *unrelaxed* mineral (in terms of order-disorder)
    can be calculated with a solid solution model.
    """
    R = gas_constant
    n = params['n']
    f = params['factor']
    deltaS = gas_constant * ((1.0 + n) * np.log(1.0 + n) - n * np.log(n))
    lnxord = lambda n, Q: np.log(1.0 + n * Q) + n * np.log(n + Q) - (1.0 + n) * np.log(1.0 + n)
    lnxdisord = lambda n, Q: 1.0 / (1.0 + n) * np.log(1.0 + n * Q) + n / (1.0 + n) * np.log(1.0 - Q) + n / (1.0 + n) * np.log(n * (1.0 - Q)) + n * n / (1.0 + n) * np.log(n + Q) - n * np.log(n)

    def reaction_bragg_williams(Q, gibbs_disorder, temperature, n, f, W):
        if Q > 1.0:
            Q = 0.9
        return gibbs_disorder + (2.0 * Q - 1.0) * W + f * R * temperature * (lnxdisord(n, Q) - lnxord(n, Q))

    def order_gibbs(pressure, temperature, params):
        W = params['Wh'] + pressure * params['Wv']
        gibbs_disorder = params['deltaH'] - f * temperature * deltaS + pressure * params['deltaV']
        Q = opt.fsolve(reaction_bragg_williams, 0.999995, args=(
         gibbs_disorder, temperature, n, f, W))[0]
        G = (1.0 - Q) * (gibbs_disorder + f * R * temperature * lnxdisord(n, Q)) + f * Q * (R * temperature * lnxord(n, Q)) + (1.0 - Q) * Q * W
        return (Q, G)

    dT = 1.0
    dP = 1000.0
    Q, G = order_gibbs(pressure, temperature, params)
    Q, GsubPsubT = order_gibbs(pressure - dP, temperature - dT, params)
    Q, GsubPaddT = order_gibbs(pressure - dP, temperature + dT, params)
    Q, GaddPsubT = order_gibbs(pressure + dP, temperature - dT, params)
    Q, GaddPaddT = order_gibbs(pressure + dP, temperature + dT, params)
    Q, GsubP = order_gibbs(pressure - dP, temperature, params)
    Q, GaddP = order_gibbs(pressure + dP, temperature, params)
    Q, GsubT = order_gibbs(pressure, temperature - dT, params)
    Q, GaddT = order_gibbs(pressure, temperature + dT, params)
    dGdT = (GaddT - GsubT) / (2.0 * dT)
    dGdP = (GaddP - GsubP) / (2.0 * dP)
    d2GdT2 = (GaddT + GsubT - 2.0 * G) / (dT * dT)
    d2GdP2 = (GaddP + GsubP - 2.0 * G) / (dP * dP)
    d2GdPdT = (GaddPaddT - GsubPaddT - GaddPsubT + GsubPsubT) / (4.0 * dT * dP)
    excesses = {'G': G, 'dGdT': dGdT, 'dGdP': dGdP, 'd2GdT2': d2GdT2, 
       'd2GdP2': d2GdP2, 'd2GdPdT': d2GdPdT}
    return excesses


def _magnetic_excesses_chs(pressure, temperature, params):
    """
    Applies a magnetic contribution to the thermodynamic
    properties of a mineral endmember.
    The expression for the gibbs energy contribution is that
    used by Chin, Hertzman and Sundman (1987) as reported
    in the Journal of Phase Equilibria (Sundman, 1991).
    """
    structural_parameter = params['structural_parameter']
    curie_temperature = params['curie_temperature'][0] + pressure * params['curie_temperature'][1]
    tau = temperature / curie_temperature
    dtaudT = 1.0 / curie_temperature
    dtaudP = -(temperature * params['curie_temperature'][1]) / (curie_temperature * curie_temperature)
    d2taudPdT = params['curie_temperature'][1] / (curie_temperature * curie_temperature)
    d2taudP2 = 2.0 * temperature * params['curie_temperature'][1] * params['curie_temperature'][1] / (curie_temperature * curie_temperature * curie_temperature)
    magnetic_moment = params['magnetic_moment'][0] + pressure * params['magnetic_moment'][1]
    dmagnetic_momentdP = params['magnetic_moment'][1]
    A = 518.0 / 1125.0 + 11692.0 / 15975.0 * (1.0 / structural_parameter - 1.0)
    if tau < 1:
        f = 1.0 - 1.0 / A * (79.0 / (140.0 * structural_parameter * tau) + 474.0 / 497.0 * (1.0 / structural_parameter - 1.0) * (np.power(tau, 3.0) / 6.0 + np.power(tau, 9.0) / 135.0 + np.power(tau, 15.0) / 600.0))
        dfdtau = -(1.0 / A) * (-79.0 / (140.0 * structural_parameter * tau * tau) + 474.0 / 497.0 * (1.0 / structural_parameter - 1.0) * (tau * tau / 2.0 + np.power(tau, 8.0) / 15.0 + np.power(tau, 14.0) / 40.0))
        d2fdtau2 = -(1.0 / A) * (158.0 / (140.0 * structural_parameter * np.power(tau, 3.0)) + 474.0 / 497.0 * (1.0 / structural_parameter - 1.0) * (tau + 8.0 * np.power(tau, 7.0) / 15.0 + 14.0 * np.power(tau, 13.0) / 40.0))
    else:
        f = -(1.0 / A) * (np.power(tau, -5.0) / 10.0 + np.power(tau, -15.0) / 315.0 + np.power(tau, -25.0) / 1500.0)
        dfdtau = 1.0 / A * (np.power(tau, -6.0) / 2.0 + np.power(tau, -16.0) / 21.0 + np.power(tau, -26.0) / 60.0)
        d2fdtau2 = -(1.0 / A) * (6.0 * np.power(tau, -7.0) / 2.0 + 16.0 * np.power(tau, -17.0) / 21.0 + 26.0 * np.power(tau, -27.0) / 60.0)
    dfdT = dfdtau * dtaudT
    d2fdT2 = d2fdtau2 * dtaudT * dtaudT
    dfdP = dfdtau * dtaudP
    d2fdP2 = d2fdtau2 * dtaudP * dtaudP + dfdtau * d2taudP2
    d2fdPdT = d2fdtau2 * dtaudT * dtaudP - dfdtau * d2taudPdT
    G = gas_constant * temperature * np.log(magnetic_moment + 1.0) * f
    dGdT = gas_constant * np.log(magnetic_moment + 1.0) * (f + temperature * dfdT)
    d2GdT2 = gas_constant * np.log(magnetic_moment + 1.0) * (2.0 * dfdT + temperature * d2fdT2)
    dGdP = gas_constant * temperature * (f * dmagnetic_momentdP / (magnetic_moment + 1.0) + dfdP * np.log(magnetic_moment + 1.0))
    d2GdP2 = gas_constant * temperature * (-f * np.power(dmagnetic_momentdP / (magnetic_moment + 1.0), 2.0) + 2 * dfdP * dmagnetic_momentdP / (magnetic_moment + 1.0) + d2fdP2 * np.log(magnetic_moment + 1.0))
    d2GdPdT = dGdP / temperature + gas_constant * temperature * np.log(magnetic_moment + 1.0) * d2fdPdT + gas_constant * temperature * dmagnetic_momentdP / (magnetic_moment + 1.0) * dfdT
    excesses = {'G': G, 'dGdT': dGdT, 'dGdP': dGdP, 'd2GdT2': d2GdT2, 
       'd2GdP2': d2GdP2, 'd2GdPdT': d2GdPdT}
    return excesses


def calculate_property_modifications(mineral):
    """
    Sums the excesses from all the modifiers.

    To calculate thermodynamic properties from the outputs,
    the following functions should be used
    (the _o suffix stands for original value):

    gibbs = gibbs_o + excesses['G']
    S = S_o - excesses['dGdT']
    V = V_o + excesses['dGdP']
    K_T = V / ((V_o / K_T_o) - excesses['d2GdP2'])
    C_p = C_p_o - temperature*excesses['d2GdT2']
    alpha = ((alpha_o*V_o) + excesses['d2GdPdT']) / V

    H = gibbs + temperature*S
    helmholtz = gibbs - pressure*V
    C_v = C_p - V*temperature*alpha*alpha*K_T
    gr = alpha*K_T*V/C_v
    K_S = K_T*C_p/C_v
    """
    excesses = {'G': 0.0, 'dGdT': 0.0, 'dGdP': 0.0, 'd2GdT2': 0.0, 
       'd2GdP2': 0.0, 'd2GdPdT': 0.0}
    for modifier in mineral.property_modifiers:
        if modifier[0] == 'landau':
            xs_function = _landau_excesses
        if modifier[0] == 'landau_hp':
            xs_function = _landau_hp_excesses
        if modifier[0] == 'linear':
            xs_function = _linear_excesses
        if modifier[0] == 'bragg_williams':
            xs_function = _bragg_williams_excesses
        if modifier[0] == 'magnetic_chs':
            xs_function = _magnetic_excesses_chs
        xs_component = xs_function(mineral.pressure, mineral.temperature, modifier[1])
        for key in xs_component:
            excesses[key] += xs_component[key]

    return excesses