# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/calculations/specimen.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3723 bytes
import numpy as np
from math import radians, tan
from scipy.interpolate.interpolate import interp1d
from .goniometer import get_fixed_to_ads_correction_range
from .phases import get_intensity

def get_clipped_intensities(specimen):
    exp = specimen.observed_intensity.transpose()[(..., specimen.selected_range)]
    cal = specimen.total_intensity[(..., specimen.selected_range)]
    return (exp, cal)


def get_machine_correction_range(specimen):
    """
        Calculate a correction factor for a certain sample length,
        sample absorption and machine setup.
    """
    goniometer = specimen.goniometer
    range_st = np.sin(specimen.range_theta)
    correction_range = np.ones_like(specimen.range_theta)
    if goniometer.divergence_mode == 'AUTOMATIC':
        correction_range *= get_fixed_to_ads_correction_range(specimen.range_theta, goniometer)
    if goniometer.has_absorption_correction > 0.0:
        absorption = goniometer.absorption * goniometer.sample_surf_density * 0.001
        if absorption > 0.0:
            correction_range *= np.minimum(1.0 - np.exp(-2.0 * absorption / range_st), 1.0)
    if goniometer.divergence_mode == 'FIXED':
        if goniometer.divergence > 0:
            L_Rta = goniometer.sample_length / (goniometer.radius * tan(radians(goniometer.divergence)))
            correction_range *= np.minimum(range_st * L_Rta, 1)
    return correction_range


def calculate_phase_intensities(specimen):
    """
        Gets phase intensities for the provided phases
        Returns a 2-tuple containing 2-theta values and phase intensities.
    """
    range_stl = 2 * np.sin(specimen.range_theta) / specimen.goniometer.wavelength
    correction_range = get_machine_correction_range(specimen)

    def get_phase_intensities(phases):
        for phase in phases:
            if phase != None:
                correction = correction_range if phase.apply_correction else 1.0
                yield get_intensity(specimen.range_theta, range_stl, specimen.goniometer.soller1, specimen.goniometer.soller2, specimen.goniometer.mcr_2theta, phase) * correction
            else:
                yield np.zeros_like(range_stl)

    def interpolate_wavelength(I, new_wavelength, fraction):
        new_theta = np.arcsin(range_stl * new_wavelength * 0.5)
        f = interp1d(new_theta, (I * fraction), bounds_error=False, fill_value=0.0)
        return f(specimen.range_theta)

    def apply_wavelength_distribution(I):
        for new_wavelength, fraction in specimen.goniometer.wavelength_distribution:
            I += interpolate_wavelength(I, new_wavelength, fraction)

        return I

    return (
     correction_range,
     np.swapaxes(np.array([[apply_wavelength_distribution(I) for I in get_phase_intensities(specimen.phases[z_index])] for z_index in range(len(specimen.z_list))],
       dtype=(np.float_)), 0, 1))


def calculate_scaled_intensities(specimen, scale, fractions, bgshift):
    specimen.background_intensity = bgshift * specimen.correction
    specimen.scaled_phase_intensities = (fractions * specimen.phase_intensities.transpose()).transpose() * scale
    specimen.total_intensity = np.sum((specimen.scaled_phase_intensities), axis=0) + specimen.background_intensity
    return specimen