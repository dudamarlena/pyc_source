# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/image.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 4610 bytes
"""
This is the module for putting advanced/x-ray specific image
processing tools.  These should be interesting compositions of existing
tools, not just straight wrapping of np/scipy/scikit images.
"""
from __future__ import absolute_import, division, print_function
import six, logging
logger = logging.getLogger(__name__)
import numpy as np

def find_ring_center_acorr_1D(input_image):
    """
    Find the pixel-resolution center of a set of concentric rings.

    This function uses correlation between the image and it's mirror
    to find the approximate center of  a single set of concentric rings.
    It is assumed that there is only one set of rings in the image.  For
    this method to work well the image must have significant mirror-symmetry
    in both dimensions.

    Parameters
    ----------
    input_image : ndarray
        A single image.

    Returns
    -------
    calibrated_center : tuple
        Returns the index (row, col) of the pixel that rings
        are centered on.  Accurate to pixel resolution.
    """
    return tuple(bins[np.argmax(vals)] for vals, bins in (_corr_ax1(_im) for _im in (input_image.T, input_image)))


def _corr_ax1(input_image):
    """
    Internal helper function that finds the best estimate for the
    location of the vertical mirror plane.  For each row the maximum
    of the correlating with it's mirror is found.  The most common value
    is reported back as the location of the mirror plane.

    Parameters
    ----------
    input_image : ndarray
        The input image

    Returns
    -------
    vals : ndarray
        histogram of what pixel has the highest correlation

    bins : ndarray
        Bin edges for the vals histogram
    """
    dim = input_image.shape[1]
    m_ones = np.ones(dim)
    norm_mask = np.correlate(m_ones, m_ones, mode='full')
    est_by_row = [np.argmax(np.correlate(v, v[::-1], mode='full') / norm_mask) / 2 for v in input_image]
    return np.histogram(est_by_row, bins=np.arange(0, dim + 1))