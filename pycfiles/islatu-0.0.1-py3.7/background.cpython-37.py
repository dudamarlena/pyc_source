# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/islatu/background.py
# Compiled at: 2020-04-21 10:49:38
# Size of source mod 2**32: 3530 bytes
"""
Background substraction is a necssary component of reflectometry reduction,
where the background scattering is removed from the reflected intensity.

Herein are some function to enable that for a two-dimensional detector image.
"""
import numpy as np
from scipy.stats import multivariate_normal
from scipy.optimize import curve_fit
from uncertainties import unumpy as unp

def bivariate_normal(data, mu_1, mu_2, sigma_1, sigma_2, offset, factor):
    """
    Produce a bivariate normal distribution.

    Note: the covariance of the two dimensions is assumed to be zero to
    unsure greater stability.

    Args:
        data (array_like): Two-dimensional abscissa data.
        mu_1 (float): Mean in dimension 0 (horizontal).
        mu_2 (float): Mean in dimension 1 (vertical).
        sigma_1 (float): Variance in dimension 0 (horizontal).
        sigma_2 (float): Variance in dimension 1 (vertical).
        offset (float): Offset from the 0 for the ordinate, this is the
            background level.
        factor (float): Multiplicative factor for area of normal distribution.

    Returns:
        (array_like): Flattened ordinate data for bivariate normal
            distribution.
    """
    pos = np.empty(data[0].shape + (2, ))
    pos[:, :, 0] = data[0]
    pos[:, :, 1] = data[1]
    binormal = multivariate_normal([mu_1, mu_2], [[sigma_1, 0], [0, sigma_2]])
    return offset + binormal.pdf(pos).flatten() * factor


def fit_gaussian_2d(image, image_e, p0=None, bounds=None):
    """
    Fit a two-dimensional Gaussian function with some ordinate offset to an
    image with an uncertainty and return the results, index of offset and
    vertical distribution width.

    Args:
        image (array_like): The data to fit the Gaussian to.
        image_e (array_like): The data uncertainty.
        p0 (list, optional): An initial guess at the parameters. Defaults to
        values based on the image.
        bounds (tuple_of_list, optional): Bounds for the fitting. Defaults to
        values based on the image.

    Returns:
        (tuple): tuple containing:
            - (np.ndarray): The results (with uncertainties) for each of the 6 parameters fit.
            - (int): The index of the offset.
            - (int): The index of the vertical distribution width.
    """
    if p0 is None:
        p0 = [image.shape[0] / 2,
         image.shape[1] / 2,
         1,
         1,
         image.min(),
         image.max()]
    if bounds is None:
        bounds = (0,
         [
          image.shape[0],
          image.shape[1],
          100,
          100,
          image.max(),
          image.max() * 10])
    abscissa = np.array(np.mgrid[0:image.shape[0]:1, 0:image.shape[1]:1])
    popt, pcov = curve_fit(bivariate_normal,
      abscissa,
      (image.flatten()),
      bounds=bounds,
      sigma=(image_e.flatten()),
      p0=p0,
      maxfev=(2000 * (len(p0) + 1)))
    p_sigma = np.sqrt(np.diag(pcov))
    return (unp.uarray(popt, p_sigma), 4, 2)