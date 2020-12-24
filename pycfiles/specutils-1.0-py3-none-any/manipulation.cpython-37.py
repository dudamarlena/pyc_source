# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nearl/projects/specutils/build/lib/specutils/manipulation/manipulation.py
# Compiled at: 2020-03-17 18:47:05
# Size of source mod 2**32: 2528 bytes
"""
A module for analysis tools dealing with uncertainties or error analysis in
spectra.
"""
import copy, numpy as np, operator
__all__ = [
 'snr_threshold']

def snr_threshold(spectrum, value, op=operator.gt):
    """
    Calculate the mean S/N of the spectrum based on the flux and uncertainty
    in the spectrum. This will be calculated over the regions, if they
    are specified.

    Parameters
    ----------
    spectrum : `~specutils.Spectrum1D`, `~specutils.SpectrumCollection` or `~astropy.nddata.NDData`
        The spectrum object overwhich the S/N threshold will be calculated.

    value: ``float``
        Threshold value to be applied to flux / uncertainty.

    op: One of operator.gt, operator.ge, operator.lt, operator.le or
        the str equivalent '>', '>=', '<', '<='
        The mathematical operator to apply for thresholding.

    Returns
    -------
    spectrum: `~specutils.Spectrum1D`
        Output object with ``spectrum.mask`` set based on threshold.

    Notes
    -----
    The input object will need to have the uncertainty defined in order for the SNR
    to be calculated.

    """
    operator_mapping = {'>':operator.gt, 
     '<':operator.lt, 
     '>=':operator.ge, 
     '<=':operator.le}
    if not hasattr(spectrum, 'uncertainty') or spectrum.uncertainty is None:
        raise Exception('S/N thresholding requires the uncertainty be defined.')
    if op not in [operator.gt, operator.ge, operator.lt, operator.le]:
        if op not in operator_mapping.keys():
            raise ValueError('Threshold operator must be a string or operator that represents greater-than, less-than, greater-than-or-equal or less-than-or-equal')
    elif isinstance(op, str):
        op = operator_mapping[op]
    elif hasattr(spectrum, 'flux'):
        data = spectrum.flux
    else:
        if hasattr(spectrum, 'data'):
            data = spectrum.data * (spectrum.unit if spectrum.unit is not None else 1)
        else:
            raise ValueError('Could not find data attribute.')
    mask = ~op(data / spectrum.uncertainty.quantity, value)
    spectrum_out = copy.copy(spectrum)
    spectrum_out._mask = mask
    return spectrum_out