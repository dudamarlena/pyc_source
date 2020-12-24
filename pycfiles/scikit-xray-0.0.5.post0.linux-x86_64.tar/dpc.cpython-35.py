# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/dpc.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 15513 bytes
"""
This module is for Differential Phase Contrast (DPC) imaging based on
Fourier shift fitting
"""
from __future__ import absolute_import, division, print_function
import logging
logger = logging.getLogger(__name__)
import numpy as np
from scipy.optimize import minimize

def image_reduction(im, roi=None, bad_pixels=None):
    """
    Sum the image data over rows and columns.

    Parameters
    ----------
    im : ndarray
        Input image.

    roi : ndarray, optional
        [r, c, row, col], selects ROI im[r : r + row, c : c + col]. Default is
        None, which uses the whole image.

    bad_pixels : list, optional
        List of (row, column) tuples marking bad pixels.
        [(1, 5), (2, 6)] --> 2 bad pixels --> (1, 5) and (2, 6). Default is
        None.

    Returns
    -------
    xline : ndarray
        The row vector of the sums of each column.

    yline : ndarray
        The column vector of the sums of each row.

    """
    if bad_pixels:
        im = im.copy()
        for row, column in bad_pixels:
            im[(row, column)] = 0

    if roi:
        r, c, row, col = roi
        im = im[r:r + row, c:c + col]
    xline = np.sum(im, axis=0)
    yline = np.sum(im, axis=1)
    return (
     xline, yline)


def _rss_factory(length):
    """
    A factory function for returning a residue function for use in dpc fitting.
    The main reason to do this is to generate a closure over beta so that
    linspace is only called once.

    Parameters
    ----------
    length : int
        The length of the data vector that the returned function can deal with.

    Returns
    -------
    function
        A function with signature f(v, xdata, ydata) which is suitable for use
        as a cost function for use with scipy.optimize.

    """
    beta = complex(0.0, 1.0) * np.linspace(-(length - 1) // 2, (length - 1) // 2, length)

    def _rss(v, ref_reduction, diff_reduction):
        """
        Internal function used by fit()
        Cost function to be minimized in nonlinear fitting

        Parameters
        ----------
        v : list
            Fit parameters.
            v[0], amplitude of the sample transmission function at one scanning
            point;
            v[1], the phase gradient (along x or y direction) of the sample
            transmission function.

        ref_reduction : ndarray
            Extra argument passed to the objective function. In DPC, it's the
            sum of the reference image data along x or y direction.

        diff_refuction : ndarray
            Extra argument passed to the objective function. In DPC, it's the
            sum of one captured diffraction pattern along x or y direction.

        Returns
        --------
        float
            Residue value.

        """
        diff = diff_reduction - ref_reduction * v[0] * np.exp(v[1] * beta)
        return np.sum((diff * np.conj(diff)).real)

    return _rss


def dpc_fit(rss, ref_reduction, diff_reduction, start_point, solver='Nelder-Mead', tol=1e-06, max_iters=2000):
    """
    Nonlinear fitting for 2 points.

    Parameters
    ----------
    rss : callable
        Objective function to be minimized in DPC fitting.

    ref_reduction : ndarray
        Extra argument passed to the objective function. In DPC, it's the sum
        of the reference image data along x or y direction.

    diff_reduction : ndarray
        Extra argument passed to the objective function. In DPC, it's the sum
        of one captured diffraction pattern along x or y direction.

    start_point : list
        start_point[0], start-searching value for the amplitude of the sample
        transmission function at one scanning point.
        start_point[1], start-searching value for the phase gradient (along x
        or y direction) of the sample transmission function at one scanning
        point.

    solver : str, optional
        Type of solver, one of the following (default 'Nelder-Mead'):
        * 'Nelder-Mead'
        * 'Powell'
        * 'CG'
        * 'BFGS'
        * 'Anneal'
        * 'L-BFGS-B'
        * 'TNC'
        * 'COBYLA'
        * 'SLSQP'

    tol : float, optional
        Termination criteria of nonlinear fitting. Default is 1e-6.

    max_iters : int, optional
        Maximum iterations of nonlinear fitting. Default is 2000.

    Returns
    -------
    tuple
        Fitting result: intensity attenuation and phase gradient.

    """
    return minimize(rss, start_point, args=(ref_reduction, diff_reduction), method=solver, tol=tol, options=dict(maxiter=max_iters)).x


dpc_fit.solver = [
 'Nelder-Mead',
 'Powell',
 'CG',
 'BFGS',
 'Anneal',
 'L-BFGS-B',
 'TNC',
 'COBYLA',
 'SLSQP']

def recon(gx, gy, scan_xstep, scan_ystep, padding=0, weighting=0.5):
    """
    Reconstruct the final phase image.

    Parameters
    ----------
    gx : ndarray
        Phase gradient along x direction.

    gy : ndarray
        Phase gradient along y direction.

    scan_xstep : float
        Scanning step size in x direction (in micro-meter).

    scan_ystep : float
        Scanning step size in y direction (in micro-meter).

    padding : int, optional
        Pad a N-by-M array to be a (N*(2*padding+1))-by-(M*(2*padding+1)) array
        with the image in the middle with a (N*padding, M*padding) thick edge
        of zeros. Default is 0.
        padding = 0 --> v (the original image, size = (N, M))
                        0 0 0
        padding = 1 --> 0 v 0 (the padded image, size = (3 * N, 3 * M))
                        0 0 0

    weighting : float, optional
        Weighting parameter for the phase gradient along x and y direction when
        constructing the final phase image.
        Valid in [0, 1]. Default value = 0.5, which means that gx and gy
        equally contribute to the final phase image.

    Returns
    -------
    phase : ndarray
        Final phase image.

    """
    if weighting < 0 or weighting > 1:
        raise ValueError('weighting should be within the range of [0, 1]!')
    pad = 2 * padding + 1
    gx = np.asarray(gx)
    rows, cols = gx.shape
    pad_row = rows * pad
    pad_col = cols * pad
    gx_padding = np.zeros((pad_row, pad_col), dtype='d')
    gy_padding = np.zeros((pad_row, pad_col), dtype='d')
    roi_slice = (
     slice(padding * rows, (padding + 1) * rows),
     slice(padding * cols, (padding + 1) * cols))
    gx_padding[roi_slice] = gx
    gy_padding[roi_slice] = gy
    tx = np.fft.fftshift(np.fft.fft2(gx_padding))
    ty = np.fft.fftshift(np.fft.fft2(gy_padding))
    mid_col = pad_col // 2 + 1
    mid_row = pad_row // 2 + 1
    ax = 2 * np.pi * np.arange(1 - mid_col, pad_col - mid_col + 1) / (pad_col * scan_xstep)
    ay = 2 * np.pi * np.arange(1 - mid_row, pad_row - mid_row + 1) / (pad_row * scan_ystep)
    kappax, kappay = np.meshgrid(ax, ay)
    div_v = kappax ** 2 * (1 - weighting) + kappay ** 2 * weighting
    c = complex(-0.0, -1.0) * (kappax * tx * (1 - weighting) + kappay * ty * weighting) / div_v
    c = np.fft.ifftshift(np.where(div_v == 0, 0, c))
    phase = np.fft.ifft2(c)[roi_slice].real
    return phase


def dpc_runner(ref, image_sequence, start_point, pixel_size, focus_to_det, scan_rows, scan_cols, scan_xstep, scan_ystep, energy, padding=0, weighting=0.5, solver='Nelder-Mead', roi=None, bad_pixels=None, negate=True, scale=True):
    """
    Controller function to run the whole Differential Phase Contrast (DPC)
    imaging calculation.

    Parameters
    ----------
    ref : ndarray
        The reference image for a DPC calculation.

    image_sequence : iterable of 2D arrays
        Return diffraction patterns (2D Numpy arrays) when iterated over.

    start_point : list
        start_point[0], start-searching value for the amplitude of the sample
        transmission function at one scanning point.
        start_point[1], start-searching value for the phase gradient (along x
        or y direction) of the sample transmission function at one scanning
        point.

    pixel_size : tuple
        Physical pixel (a rectangle) size of the detector in um.

    focus_to_det : float
        Focus to detector distance in um.

    scan_rows : int
        Number of scanned rows.

    scan_cols : int
        Number of scanned columns.

    scan_xstep : float
        Scanning step size in x direction (in micro-meter).

    scan_ystep : float
        Scanning step size in y direction (in micro-meter).

    energy : float
        Energy of the scanning x-ray in keV.

    padding : int, optional
        Pad a N-by-M array to be a (N*(2*padding+1))-by-(M*(2*padding+1)) array
        with the image in the middle with a (N*padding, M*padding) thick edge
        of zeros. Default is 0.
        padding = 0 --> v (the original image, size = (N, M))
                        0 0 0
        padding = 1 --> 0 v 0 (the padded image, size = (3 * N, 3 * M))
                        0 0 0

    weighting : float, optional
        Weighting parameter for the phase gradient along x and y direction when
        constructing the final phase image.
        Valid in [0, 1]. Default value = 0.5, which means that gx and gy
        equally contribute to the final phase image.

    solver : str, optional
        Type of solver, one of the following (default 'Nelder-Mead'):
        * 'Nelder-Mead'
        * 'Powell'
        * 'CG'
        * 'BFGS'
        * 'Anneal'
        * 'L-BFGS-B'
        * 'TNC'
        * 'COBYLA'
        * 'SLSQP'

    roi : ndarray, optional
        [r, c, row, col], selects ROI im[r : r + row, c : c + col]. Default is
        None.

    bad_pixels : list, optional
        List of (row, column) tuples marking bad pixels.
        [(1, 5), (2, 6)] --> 2 bad pixels --> (1, 5) and (2, 6). Default is
        None.

    negate : bool, optional
        If True (default), negate the phase gradient along x direction before
        reconstructing the final phase image. Default is True.

    scale : bool, optional
        If True, scale gx and gy according to the experiment set up.
        If False, ignore pixel_size, focus_to_det, energy. Default is True.

    Returns
    -------
    phase : ndarray
        The final reconstructed phase image.

    amplitude : ndarray
        Amplitude of the sample transmission function.

    References: text [1]_
    .. [1] Yan, H. et al. Quantitative x-ray phase imaging at the nanoscale by
    multilayer Laue lenses. Sci. Rep. 3, 1307; DOI:10.1038/srep01307 (2013).

    """
    if weighting < 0 or weighting > 1:
        raise ValueError('weighting should be within the range of [0, 1]!')
    ax = np.zeros((scan_rows, scan_cols), dtype='d')
    ay = np.zeros((scan_rows, scan_cols), dtype='d')
    gx = np.zeros((scan_rows, scan_cols), dtype='d')
    gy = np.zeros((scan_rows, scan_cols), dtype='d')
    phase = np.zeros((scan_rows, scan_cols), dtype='d')
    refx, refy = image_reduction(ref, roi, bad_pixels)
    ref_fx = np.fft.fftshift(np.fft.ifft(refx))
    ref_fy = np.fft.fftshift(np.fft.ifft(refy))
    ffx = _rss_factory(len(ref_fx))
    ffy = _rss_factory(len(ref_fy))
    num_images = len(image_sequence)
    steps = np.max((num_images // 100, 1))
    for index, im in enumerate(image_sequence):
        i, j = np.unravel_index(index, (scan_rows, scan_cols))
        imx, imy = image_reduction(im, roi, bad_pixels)
        fx = np.fft.fftshift(np.fft.ifft(imx))
        fy = np.fft.fftshift(np.fft.ifft(imy))
        _ax, _gx = dpc_fit(ffx, ref_fx, fx, start_point, solver)
        _ay, _gy = dpc_fit(ffy, ref_fy, fy, start_point, solver)
        gx[(i, j)] = _gx
        gy[(i, j)] = _gy
        ax[(i, j)] = _ax
        ay[(i, j)] = _ay
        if (index + 1) % steps == 0:
            logger.debug('dpc {}% complete'.format(100 * (index + 1) // num_images))

    if scale:
        if pixel_size[0] != pixel_size[1]:
            raise ValueError('In DPC, detector pixels are squares!')
        lambda_ = 0.00124 / energy
        gx *= len(ref_fx) * pixel_size[0] / (lambda_ * focus_to_det)
        gy *= len(ref_fy) * pixel_size[0] / (lambda_ * focus_to_det)
    if negate:
        gx *= -1
    phase = recon(gx, gy, scan_xstep, scan_ystep, padding, weighting)
    return (
     phase, (ax + ay) / 2)


dpc_runner.solver = [
 'Nelder-Mead',
 'Powell',
 'CG',
 'BFGS',
 'Anneal',
 'L-BFGS-B',
 'TNC',
 'COBYLA',
 'SLSQP']