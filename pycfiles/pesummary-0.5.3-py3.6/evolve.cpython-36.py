# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/file/evolve.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 7633 bytes
import numpy as np
from lal import MTSUN_SI, MSUN_SI
import lalsimulation
from lalsimulation import SimInspiralGetSpinFreqFromApproximant, SIM_INSPIRAL_SPINS_CASEBYCASE, SIM_INSPIRAL_SPINS_FLOW, SimInspiralSpinTaylorPNEvolveOrbit
from pesummary.gw.file.conversions import tilt_angles_and_phi_12_from_spin_vectors_and_L
from pesummary.utils.utils import iterator, logger

def evolve_spins(mass_1, mass_2, a_1, a_2, tilt_1, tilt_2, phi_12, f_low, f_ref, approximant, final_velocity='ISCO', tolerance=0.001, dt=0.1):
    """Evolve the BBH spins up to a specified value. By default this is the
    Schwarzchild ISCO velocity.

    Parameters
    ----------
    mass_1: float/np.ndarray
        float/array of primary mass samples of the binary
    mass_2: float/np.ndarray
        float/array of secondary mass samples of the binary
    a_1: float/np.ndarray
        float/array of primary spin magnitudes
    a_2: float/np.ndarray
        float/array of secondary spin magnitudes
    tilt_1: float/np.ndarray
        float/array of primary spin tilt angle from the orbital angular momentum
    tilt_2: float/np.ndarray
        float/array of secondary spin tilt angle from the orbital angular
    phi_12: float/np.ndarray
        float/array of samples for the angle between the in-plane spin
        components
    f_low: float
        low frequency cutoff used in the analysis
    f_ref: float
        reference frequency where spins are defined
    approximant: str
        Approximant used to generate the posterior samples
    final_velocity: str, float
        final orbital velocity for the evolution. This can either be the
        Schwarzschild ISCO velocity 6**-0.5 ~= 0.408 ('ISCO') or a
        fraction of the speed of light
    tolerance: float
        Only evolve spins if at least one spin's magnitude is greater than
        tolerance
    dt: float
        steps in time for the integration, in terms of the mass of the binary
    """
    if isinstance(final_velocity, str):
        if final_velocity.lower() == 'isco':
            final_velocity = 0.408248290463863
    else:
        final_velocity = float(final_velocity)
    spinfreq_enum = SimInspiralGetSpinFreqFromApproximant(getattr(lalsimulation, approximant))
    if spinfreq_enum == SIM_INSPIRAL_SPINS_CASEBYCASE:
        raise ValueError("Unable to evolve spins as '{}' does not have a set frequency at which the spins are defined".format(approximant))
    f_start = float(np.where(np.array(spinfreq_enum == SIM_INSPIRAL_SPINS_FLOW), f_low, f_ref))
    tilt_1_evol, tilt_2_evol, phi_12_evol = _evolve_spins(mass_1,
      mass_2, a_1, a_2, tilt_1, tilt_2, phi_12, f_start, final_velocity,
      tolerance=tolerance, dt=dt)
    return (
     tilt_1_evol, tilt_2_evol, phi_12_evol)


def _evolve_spins(mass_1, mass_2, a_1, a_2, tilt_1, tilt_2, phi_12, f_start, final_velocity, tolerance=0.001, dt=0.1, evolution_approximant='SpinTaylorT5'):
    """Wrapper function for the SimInspiralSpinTaylorPNEvolveOrbit function

    Parameters
    ----------
    mass_1: float/np.ndarray
        float/array of primary mass samples of the binary
    mass_2: float/np.ndarray
        float/array of secondary mass samples of the binary
    a_1: float/np.ndarray
        float/array of primary spin magnitudes
    a_2: float/np.ndarray
        float/array of secondary spin magnitudes
    tilt_1: float/np.ndarray
        float/array of primary spin tilt angle from the orbital angular momentum
    tilt_2: float/np.ndarray
        float/array of secondary spin tilt angle from the orbital angular
    phi_12: float/np.ndarray
        float/array of samples for the angle between the in-plane spin
        components
    f_start: float
        frequency to start the evolution from
    final_velocity: float
        Final velocity to evolve the spins up to
    tolerance: float
        Only evolve spins if at least one spins magnitude is greater than
        tolerance
    dt: float
        steps in time for the integration, in terms of the mass of the binary
    evolve_approximant: str
        name of the approximant you wish to use to evolve the spins. Default
        is SpinTaylorT5
    """
    if isinstance(mass_1, (float, int)):
        mass_1, mass_2 = [
         mass_1], [mass_2]
        a_1, a_2, tilt_1, tilt_2 = ([a_1], [a_2], [tilt_1], [tilt_2])
        phi_12 = [phi_12]
    tilt_1_evol = np.zeros_like(mass_1)
    tilt_2_evol = np.zeros_like(mass_1)
    phi_12_evol = np.zeros_like(mass_1)
    for i in iterator((range(len(mass_1))), desc='Evolving spins', tqdm=True):
        if np.logical_or(a_1[i] > tolerance, a_2[i] > tolerance):
            total_mass = (mass_1[i] + mass_2[i]) * MTSUN_SI
            f_final = final_velocity ** 3 / (total_mass * np.pi)
            data = SimInspiralSpinTaylorPNEvolveOrbit(deltaT=(dt * total_mass),
              m1=(mass_1[i] * MSUN_SI),
              m2=(mass_2[i] * MSUN_SI),
              fStart=f_start,
              fEnd=f_final,
              s1x=(a_1[i] * np.sin(tilt_1[i])),
              s1y=0.0,
              s1z=(a_1[i] * np.cos(tilt_1[i])),
              s2x=(a_2[i] * np.sin(tilt_2[i]) * np.cos(phi_12[i])),
              s2y=(a_2[i] * np.sin(tilt_2[i]) * np.sin(phi_12[i])),
              s2z=(a_2[i] * np.cos(tilt_2[i])),
              lnhatx=0.0,
              lnhaty=0.0,
              lnhatz=1.0,
              e1x=1.0,
              e1y=0.0,
              e1z=0.0,
              lambda1=0.0,
              lambda2=0.0,
              quadparam1=1.0,
              quadparam2=1.0,
              spinO=7,
              tideO=0,
              phaseO=7,
              lscorr=0,
              approx=(getattr(lalsimulation, evolution_approximant)))
            if f_start <= f_final:
                idx_use = -1
            else:
                idx_use = 0
            a_1_evolve = np.array([
             data[2].data.data[idx_use], data[3].data.data[idx_use],
             data[4].data.data[idx_use]])
            a_2_evolve = np.array([
             data[5].data.data[idx_use], data[6].data.data[idx_use],
             data[7].data.data[idx_use]])
            Ln_evolve = np.array([
             data[8].data.data[idx_use], data[9].data.data[idx_use],
             data[10].data.data[idx_use]])
            tilt_1_evol[i], tilt_2_evol[i], phi_12_evol[i] = tilt_angles_and_phi_12_from_spin_vectors_and_L(a_1_evolve, a_2_evolve, Ln_evolve)
        else:
            tilt_1_evol[i], tilt_2_evol[i], phi_12_evol[i] = tilt_1[i], tilt_2[i], phi_12[i]

    return (
     tilt_1_evol, tilt_2_evol, phi_12_evol)