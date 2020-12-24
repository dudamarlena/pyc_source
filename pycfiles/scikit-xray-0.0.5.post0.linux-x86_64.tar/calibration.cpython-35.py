# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/calibration.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 9030 bytes
"""
This is the module for calibration functions and data
"""
from __future__ import absolute_import, division, print_function
from collections import deque
import numpy as np, scipy.signal
from .constants import calibration_standards
from .feature import filter_peak_height, peak_refinement, refine_log_quadratic
from .utils import angle_grid, radial_grid, pairwise, bin_edges_to_centers, bin_1D

def estimate_d_blind(name, wavelength, bin_centers, ring_average, window_size, max_peak_count, thresh):
    r"""
    Estimate the sample-detector distance

    Given a radially integrated calibration image return an estimate for
    the sample-detector distance.  This function does not require a
    rough estimate of what d should be.

    For the peaks found the detector-sample distance is estimated via
    .. math ::

        D = \frac{r}{\tan 2\theta}

    where :math:`r` is the distance in mm from the calibrated center
    to the ring on the detector and :math:`D` is the distance from
    the sample to the detector.

    Parameters
    ----------
    name : str
        The name of the calibration standard.  Used to look up the
        expected peak location
        For valid options, see the name attribute on this function

    wavelength : float
        The wavelength of scattered x-ray in nm

    bin_centers : array
        The distance from the calibrated center to the center of
        the ring's annulus in mm

    ring_average : array
        The average intensity in the given ring of a azimuthally integrated
        powder pattern.  In counts [arb]

    window_size : int
        The number of elements on either side of a local maximum to
        use for locating and refining peaks.  Candidates are identified
        as a relative maximum in a window sized (2*window_size + 1) and
        the same window is used for fitting the peaks to refine the location.

    max_peak_count : int
        Use at most this many peaks

    thresh : float
        Fraction of maximum peak height

    Returns
    -------
    dist_sample : float
        The detector-sample distance in mm.  This is the mean of the estimate
        from all of the peaks used.

    std_dist_sample : float
        The standard deviation of d computed from the peaks used.
    """
    cal = calibration_standards[name]
    cands = scipy.signal.argrelmax(ring_average, order=window_size)[0]
    cands = filter_peak_height(ring_average, cands, thresh * np.max(ring_average), window=window_size)
    peaks_x, peaks_y = peak_refinement(bin_centers, ring_average, cands, window_size, refine_log_quadratic)
    tan2theta = np.tan(cal.convert_2theta(wavelength))
    slc = slice(0, np.min([len(tan2theta), len(peaks_x), max_peak_count]))
    d_array = peaks_x[slc] / tan2theta[slc]
    return (np.mean(d_array), np.std(d_array))


estimate_d_blind.name = list(calibration_standards)

def refine_center(image, calibrated_center, pixel_size, phi_steps, max_peaks, thresh, window_size, nx=None, min_x=None, max_x=None):
    """
    Refines the location of the center of the beam.

    This relies on being able to see the whole powder pattern.

    Parameters
    ----------
    image : ndarray
        The image

    calibrated_center : tuple
        (row, column) the estimated center

    pixel_size : tuple
        (pixel_height, pixel_width)

    phi_steps : int
        How many regions to split the ring into, should be >10

    max_peaks : int
        Number of rings to look it

    thresh : float
        Fraction of maximum peak height

    window_size : int, optional
        The window size to use (in bins) to use when refining peaks

    nx : int, optional
        Number of bins to use for radial binning

    min_x : float, optional
        The minimum radius to use for radial binning

    max_x : float, optional
        The maximum radius to use for radial binning

    Returns
    -------
    calibrated_center : tuple
        The refined calibrated center.
    """
    if nx is None:
        nx = int(np.mean(image.shape) * 2)
    phi = angle_grid(calibrated_center, image.shape, pixel_size).ravel()
    r = radial_grid(calibrated_center, image.shape, pixel_size).ravel()
    I = image.ravel()
    phi_steps = np.linspace(-np.pi, np.pi, phi_steps, endpoint=True)
    out = deque()
    for phi_start, phi_end in pairwise(phi_steps):
        mask = (phi <= phi_end) * (phi > phi_start)
        out.append(bin_1D(r[mask], I[mask], nx=nx, min_x=min_x, max_x=max_x))

    out = list(out)
    ring_trace = []
    for bins, b_sum, b_count in out:
        mask = b_sum > 10
        avg = b_sum[mask] / b_count[mask]
        bin_centers = bin_edges_to_centers(bins)[mask]
        cands = scipy.signal.argrelmax(avg, order=window_size)[0]
        cands = filter_peak_height(avg, cands, thresh * np.max(avg), window=window_size)
        ring_trace.append(bin_centers[cands[:max_peaks]])

    tr_len = [len(rt) for rt in ring_trace]
    mm = np.min(tr_len)
    ring_trace = np.vstack([rt[:mm] for rt in ring_trace]).T
    mean_dr = np.mean(ring_trace - np.mean(ring_trace, axis=1, keepdims=True), axis=0)
    phi_centers = bin_edges_to_centers(phi_steps)
    delta = np.mean(np.diff(phi_centers))
    col_shift = np.sum(np.sin(phi_centers) * mean_dr) * delta / (np.pi * pixel_size[1])
    row_shift = np.sum(np.cos(phi_centers) * mean_dr) * delta / (np.pi * pixel_size[0])
    return tuple(np.array(calibrated_center) + np.array([row_shift, col_shift]))