# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/calculations/phases.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 5947 bytes
import logging
logger = logging.getLogger(__name__)
import numpy as np
from scipy.interpolate import interp1d
from .math_tools import mmult
from .CSDS import calculate_distribution
from .goniometer import get_lorentz_polarisation_factor
from .components import get_factors

def get_structure_factors(range_stl, G, comp_list):
    """
        Calculates the structure factor and phase factor for:
        
            - range_stl: numpy array of 2*sin(θ) / λ values
            - G: the number of components (layer types)
            - comp_list: list of 
              :class:`~pyxrd.calculations.data_objects.ComponentData` instances
               
        This function calls :meth:`~pyxrd.calculations.components.get_factors`
        for each component in `comp_list` and stores the returned structure 
        factors and phase difference factors in a numpy array (of type complex)
        with shape (X, G) where X is expanded to fit the shape of `range_stl`.
    """
    shape = range_stl.shape + (G,)
    SF = np.zeros(shape, dtype=(np.complex_))
    PF = np.zeros(shape, dtype=(np.complex_))
    for i, comp in enumerate(comp_list):
        SF[:, i], PF[:, i] = get_factors(range_stl, comp)

    return (
     SF, PF)


def get_Q_matrices(Q, CSDS_max):
    Qn = np.zeros(((CSDS_max + 1,) + Q.shape), dtype=complex)
    Qn[(0, Ellipsis)] = np.copy(Q)
    for n in range(1, CSDS_max + 1):
        Qn[(n, ...)] = mmult(Qn[(n - 1, ...)], Q)

    return Qn


def get_absolute_scale(components, CSDS_real_mean, W):
    W = np.diag(W)
    mean_volume = 0.0
    mean_d001 = 0.0
    mean_density = 0.0
    for i, comp in enumerate(components):
        if comp != None:
            mean_volume += comp.volume * W[i]
            mean_d001 += comp.d001 * W[i]
            mean_density += comp.weight * W[i] / comp.volume
        else:
            logger.debug("- calc: get_absolute_scale reports: 'Zero observations found!'")

    mean_mass = CSDS_real_mean * mean_volume ** 2 * mean_density
    if mean_mass != 0.0:
        return mean_d001 / mean_mass
    else:
        return 0.0


def get_diffracted_intensity(range_theta, range_stl, phase):
    """
        Gets intensity for a single phase without taking the
        lorentz polarization factor into account.
    """
    if phase.type == 'AbtractPhase':
        raise NotImplementedError
    else:
        if phase.type == 'RawPatternPhase':
            return _get_raw_intensity(range_theta, range_stl, phase)
        else:
            return _get_diffracted_intensity(range_theta, range_stl, phase)


def get_intensity(range_theta, range_stl, soller1, soller2, mcr_2theta, phase):
    """
        Gets intensity for a single phase taking the
        lorentz polarization factor into account.
    """
    intensity = get_diffracted_intensity(range_theta, range_stl, phase)
    if phase.apply_lpf:
        return intensity * get_lorentz_polarisation_factor(range_theta, phase.sigma_star, soller1, soller2, mcr_2theta)
    else:
        return intensity


def _get_raw_intensity(range_theta, range_stl, phase):
    assert phase.type == 'RawPatternPhase', 'Must be RawPatternPhase!'
    f = interp1d((phase.raw_pattern_x),
      (phase.raw_pattern_y), bounds_error=False,
      fill_value=0)
    i = f(np.rad2deg(2 * range_theta))
    return i


def _get_diffracted_intensity(range_theta, range_stl, phase):
    assert phase.type == 'Phase', 'Must be Phase!'
    if not phase.valid_probs:
        logger.debug("- calc: get_diffracted_intensity reports: 'Invalid probability found!'")
        return np.zeros_like(range_stl)
    else:
        CSDS_arr, CSDS_real_mean = calculate_distribution(phase.CSDS)
        abs_scale = get_absolute_scale(phase.components, CSDS_real_mean, phase.W)
        stl_dim = range_stl.shape[0]
        repeat_to_stl = lambda arr: np.repeat((arr[(np.newaxis, ...)]), stl_dim, axis=0)
        W = repeat_to_stl(phase.W).astype(np.complex_)
        P = repeat_to_stl(phase.P).astype(np.complex_)
        SF, PF = get_structure_factors(range_stl, phase.G, phase.components)
        SFa = np.repeat((SF[..., np.newaxis, :]), (SF.shape[1]), axis=1)
        SFb = np.transpose((np.conjugate(SFa)), axes=(0, 2, 1))
        rank = P.shape[1]
        reps = rank / phase.G
        F = np.repeat(np.repeat((np.multiply(SFb, SFa)), reps, axis=2), reps, axis=1)
        PF = np.repeat((PF[..., np.newaxis, :]), (PF.shape[1]), axis=1)
        Q = np.multiply(np.repeat(np.repeat(PF, reps, axis=2), reps, axis=1), P)
        Qn = get_Q_matrices(Q, phase.CSDS.maximum)
        sub_total = np.zeros((Q.shape), dtype=(np.complex))
        for n in range(phase.CSDS.minimum, phase.CSDS.maximum + 1):
            progression_factor = 0
            for m in range(n + 1, phase.CSDS.maximum + 1):
                progression_factor += (m - n) * CSDS_arr[m]

            sub_total += 2 * progression_factor * Qn[(n - 1, ...)]

        CSDS_I = repeat_to_stl(np.identity(rank, dtype=(np.complex)) * CSDS_real_mean)
        sub_total = CSDS_I + sub_total
        sub_total = mmult(mmult(F, W), sub_total)
        intensity = np.real(np.trace(sub_total, axis1=2, axis2=1))
        return intensity * abs_scale