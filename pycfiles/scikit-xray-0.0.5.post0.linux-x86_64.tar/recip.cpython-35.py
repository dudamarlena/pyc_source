# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/recip.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 8818 bytes
"""

This module is for functions and classes specific to reciprocal space
calculations.

"""
from __future__ import absolute_import, division, print_function
import logging, numpy as np
from .utils import verbosedict
logger = logging.getLogger(__name__)
import time
try:
    from pyFAI import geometry as geo
except ImportError:
    geo = None

try:
    import src.ctrans as ctrans
except ImportError:
    try:
        import ctrans
    except ImportError:
        ctrans = None

def process_to_q(setting_angles, detector_size, pixel_size, calibrated_center, dist_sample, wavelength, ub, frame_mode=None):
    """
    This will compute the hkl values for all pixels in a shape specified by
    detector_size.

    Parameters
    ----------
    setting_angles : ndarray
        six angles of all the images - Required shape is [num_images][6] and
        required type is something that can be cast to a 2D numpy array
        Angle order: delta, theta, chi, phi, mu, gamma (degrees)

    detector_size : tuple
        2 element tuple defining the number of pixels in the detector. Order is
        (num_columns, num_rows)

    pixel_size : tuple
        2 element tuple defining the size of each pixel in mm. Order is
        (column_pixel_size, row_pixel_size).  If not in mm, must be in the same
        units as `dist_sample`

    calibrated_center : tuple
        2 element tuple defining the center of the detector in pixels. Order
        is (column_center, row_center)(x y)

    dist_sample : float
        distance from the sample to the detector (mm). If not in mm, must be
        in the same units as `pixel_size`

    wavelength : float
        wavelength of incident radiation (Angstroms)

    ub : ndarray
        UB matrix (orientation matrix) 3x3 matrix

    frame_mode : str, optional
        Frame mode defines the data collection mode and thus the desired
        output from this function. Defaults to hkl mode (frame_mode=4)
        'theta'    : Theta axis frame.
        'phi'      : Phi axis frame.
        'cart'     : Crystal cartesian frame.
        'hkl'      : Reciprocal lattice units frame.
        See the `process_to_q.frame_mode` attribute for an exact list of
        valid options.

    Returns
    -------
    hkl : ndarray
        (Qx, Qy, Qz) - HKL values
        shape is [num_images * num_rows * num_columns][3]

    Notes
    -----
    Six angles of an image: (delta, theta, chi, phi, mu, gamma )
    These axes are defined according to the following references.

    References: text [1]_, text [2]_

    .. [1] M. Lohmeier and E.Vlieg, "Angle calculations for a six-circle
       surface x-ray diffractometer," J. Appl. Cryst., vol 26, pp 706-716,
       1993.

    .. [2] E. Vlieg, "A (2+3)-Type surface diffractometer: Mergence of the
       z-axis and (2+2)-Type geometries," J. Appl. Cryst., vol 31, pp 198-203,
       1998.

    """
    if frame_mode is None:
        frame_mode = 4
    else:
        str_to_int = verbosedict((k, j + 1) for j, k in enumerate(process_to_q.frame_mode))
        frame_mode = str_to_int[frame_mode]
    ub = np.asarray(ub)
    setting_angles = np.atleast_2d(setting_angles)
    if setting_angles.ndim != 2:
        raise ValueError('setting_angles is expected to be a 2-D array with dimensions [num_images][num_angles]. You provided an array with dimensions {0}'.format(setting_angles.shape))
    if setting_angles.shape[1] != 6:
        raise ValueError('It is expected that there should be six angles in the setting_angles parameter. You provided {0} angles.'.format(setting_angles.shape[1]))
    t1 = time.time()
    hkl = ctrans.ccdToQ(angles=setting_angles * np.pi / 180.0, mode=frame_mode, ccd_size=detector_size, ccd_pixsize=pixel_size, ccd_cen=calibrated_center, dist=dist_sample, wavelength=wavelength, UBinv=np.matrix(ub).I)
    t2 = time.time()
    logger.info('Processing time for {0} {1} x {2} images took {3} seconds.'.format(setting_angles.shape[0], detector_size[0], detector_size[1], t2 - t1))
    return hkl[:, :3]


process_to_q.frame_mode = [
 'theta', 'phi', 'cart', 'hkl']

def hkl_to_q(hkl_arr):
    """
    This module compute the reciprocal space (q) values from known HKL array
    for each pixel of the detector for all the images

    Parameters
    ----------
    hkl_arr : ndarray
        (Qx, Qy, Qz) - HKL array
        shape is [num_images * num_rows * num_columns][3]

    Returns
    -------
    q_val : ndarray
        Reciprocal values for each pixel for all images
        shape is [num_images * num_rows * num_columns]
    """
    return np.linalg.norm(hkl_arr, axis=1)


def calibrated_pixels_to_q(detector_size, pyfai_kwargs):
    """
    For a given detector and pyfai calibrated geometry give back the q value
    for each pixel in the detector.

    Parameters
    -----------
    detector_size : tuple
        2 element tuple defining the number of pixels in the detector. Order is
        (num_columns, num_rows)
    pyfai_kwargs: dict
        The dictionary of pyfai geometry kwargs, given by pyFAI's calibration
        Ex: dist, poni1, poni2, rot1, rot2, rot3, splineFile, wavelength,
        detector, pixel1, pixel2

    Returns
    -------
    q_val : ndarray
        Reciprocal values for each pixel shape is [num_rows * num_columns]
    """
    if geo is None:
        raise RuntimeError('You must have pyFAI installed to use this function.')
    a = geo.Geometry(**pyfai_kwargs)
    return a.qArray(detector_size)