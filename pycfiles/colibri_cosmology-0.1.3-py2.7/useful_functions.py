# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/colibri/useful_functions.py
# Compiled at: 2020-05-11 06:25:53
import numpy as np, scipy.interpolate as si, scipy.fftpack as sfft, scipy.optimize, sys
from six.moves import xrange
try:
    import fftlog
except ImportError:
    pass

def extrapolate(x, y, xmin, xmax, order):
    """
        This function extrapolates a given function (`y`) defined in some points (`x`) to some other
        points external to the extension of `x` itself. The extrapolation is a power-law of an
        order which must be specified in input
        The points `x` must be linearly spaced, `xmin` and `xmax` must be smaller and greater than
        `x.min()` and `x.max()` respectively.

        :type x: array/list
        :param x: Abscissa of the function. Must be linearly spaced.

        :type y: array/list
        :param y: Ordinates (evaluated at `x`) of the function.

        :type xmin: float
        :param xmin: Minimum abscissa where to extend the array.

        :type xmax: float
        :param xmax: Maximum abscissa where to extend the array.

        :type order: float
        :param order: Order of the power-law to use.

        Returns
        -------

        x_ext: array
            Extended/extrapolated abscissa.

        y_ext: array
            Extended/extrapolated ordinate.

        """
    assert np.allclose(np.diff(x), np.diff(x)[0], rtol=0.001), "'x' array not linearly spaced"
    dx = np.diff(x)[0]
    low_fit = np.polyfit(x[:4], y[:4], order)
    high_fit = np.polyfit(x[-4:], y[-4:], order)
    x_low = np.arange(xmin, x[1], dx)
    y_low = np.polyval(low_fit, x_low)
    x_high = np.arange(x[(-1)] + dx, xmax, dx)
    y_high = np.polyval(high_fit, x_high)
    x_ext = np.concatenate([x_low, x, x_high])
    y_ext = np.concatenate([y_low, y, y_high])
    return (
     x_ext, y_ext)


def extrapolate_log(x, y, xmin, xmax):
    """
        This function extrapolates a given function (`y`) defined in some points (`x`) to some other
        points external to the extension of `x` itself. The extrapolation is a power-law of an
        order which must be specified in input
        The points `x` must be log-spaced, `xmin` and `xmax` must be smaller and greater than
        `x.min()` and `x.max()` respectively.

        :type x: array/list
        :param x: Abscissa of the function. Must be linearly spaced.

        :type y: array/list
        :param y: Ordinates (evaluated at `x`) of the function.

        :type xmin: float
        :param xmin: Minimum abscissa where to extend the array.

        :type xmax: float
        :param xmax: Maximum abscissa where to extend the array.

        Returns
        -------

        x_ext: array
            Extended/extrapolated abscissa.

        y_ext: array
            Extended/extrapolated ordinate.
        """
    assert np.allclose(np.diff(np.log(x)), np.diff(np.log(x))[0], rtol=0.001), "'x' array not log-spaced"
    dx = x[1] / x[0]
    dlnx = np.log(dx)
    low_fit = np.polyfit(np.log(x[:2]), np.log(y[:2]), 1)
    high_fit = np.polyfit(np.log(x[-2:]), np.log(y[-2:]), 1)
    lnx_low = np.arange(np.log(xmin), np.log(x[0]), dlnx)
    lny_low = np.polyval(low_fit, lnx_low)
    lnx_high = np.arange(np.log(x[(-1)] * dx), np.log(xmax), dlnx)
    lny_high = np.polyval(high_fit, lnx_high)
    x_low = np.exp(lnx_low)
    y_low = np.exp(lny_low)
    x_high = np.exp(lnx_high)
    y_high = np.exp(lny_high)
    x_ext = np.concatenate([x_low, x, x_high])
    y_ext = np.concatenate([y_low, y, y_high])
    return (
     x_ext, y_ext)


def neutrino_masses(M_nu, hierarchy='normal'):
    """
        Value of neutrino masses according to particle physics and the Solar Neutrino Experiment.
        Taken from `Pylians <https://github.com/franciscovillaescusa/Pylians>`_ codes by Francisco Villaescusa-Navarro.

        :type M_nu: float
        :param M_nu: Value of the sum of neutrino masses (in :math:`eV`).

        :type hierarchy: string, default = `'normal'`
        :param hierarchy: Set the neutrino hierarchy.

         - `'normal'`, `'Normal'`, `'NH'`, `'N'`, `'n'` for normal hierarchy.
         - `'inverted'`, `'Inverted'`, `'IH'`, `'I'`, `'i'` for inverted hierarchy.
         - `'degenerate'`, `'Degenerate'`, `'DH'`, `'deg'`, `'D'`, `'d'` for degenerate hierarchy.

        Returns
        ----------

        m1, m2, m3: values of the three neutrino masses (in :math:`eV`).
        """
    delta21 = 7.5e-05
    delta31 = 0.00245
    M_NH_min = np.sqrt(delta21) + np.sqrt(delta31)
    M_IH_min = np.sqrt(delta31) + np.sqrt(delta21 + delta31)
    if hierarchy in ('normal', 'Normal', 'NH', 'N', 'n'):
        if M_nu < M_NH_min:
            raise ValueError('Normal hierarchy non allowed for M_nu = %.4f eV' % M_nu)
        else:
            m1_fun = lambda x: M_nu - x - np.sqrt(delta21 + x ** 2) - np.sqrt(delta31 + x ** 2)
            m1 = scipy.optimize.brentq(m1_fun, 0.0, M_nu)
            m2 = np.sqrt(delta21 + m1 ** 2)
            m3 = np.sqrt(delta31 + m1 ** 2)
    elif hierarchy in ('inverted', 'Inverted', 'IH', 'I', 'i'):
        if M_nu < M_IH_min:
            raise ValueError('Inverted hierarchy non allowed for M_nu = %.4f eV' % M_nu)
        else:
            m3_fun = lambda x: M_nu - x - np.sqrt(delta31 + x ** 2) - np.sqrt(delta21 + np.sqrt(delta31 + x ** 2) ** 2)
            m3 = scipy.optimize.brentq(m3_fun, 0.0, M_nu)
            m1 = np.sqrt(delta31 + m3 ** 2)
            m2 = np.sqrt(delta21 + m1 ** 2)
    elif hierarchy in ('degenerate', 'Degenerate', 'DH', 'deg', 'D', 'd'):
        m1, m2, m3 = M_nu / 3.0, M_nu / 3.0, M_nu / 3.0
    else:
        raise NameError('Hierarchy not recognized')
    return (m1, m2, m3)


def TopHat_window(x):
    """
        Top-hat window function in Fourier space.

        :param x: Abscissa
        :type x: array

        :return: array
        """
    return 3.0 / x ** 3 * (np.sin(x) - x * np.cos(x))


def smooth(y, box_pts):
    """
        This routine smooths an array of a certain range of points.

        :type y: array
        :param y: Array to smooth.

        :type box_pts: int
        :param box_pts: Number of points over which to smooth.

        :return: array
        """
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def Nyquist_frequency(boxsize, grid):
    r"""
        This routine returns the Nyquist frequency of a cosmological box where the density field is computed with a grid of a certain size.

        :type boxsize: float
        :param boxsize: Size of the cubic box in :math:`\mathrm{Mpc}/h`.

        :type grid: int
        :param grid: Thickness of grid.

        :return: float
        """
    return np.pi / (boxsize / grid)


def fundamental_frequency(boxsize):
    r"""
        This routine returns the fundamental frequency of a cosmological box where the density field is computed with a grid of a certain size.

        :type boxsize: float
        :param boxsize: Size of the cubic box in :math:`\mathrm{Mpc}/h`.

        :return: float
        """
    return 2.0 * np.pi / boxsize


def full_sky():
    """
        Total square degrees in the full sky.

        :return: float
        """
    return 4.0 * np.pi * (180.0 / np.pi) ** 2.0


def sky_fraction(area):
    """
        Returns the sky fraction given the survey size in square degrees.

        :type area: float
        :param area: Survey area in square degrees.

        :return: float
        """
    return area / full_sky()


def feedback_suppression(k, z, log_Mc, eta_b, z_c):
    r"""
        Suppression of the matter power spectrum according to the Baryon Correction Model
        (Schneider et al., 2015).

        .. warning::

         This function also exists in the class :func:`~colibri.cosmology.cosmo()`.

        :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
        :type k: array

        :param z: Redshifts.
        :type z: array

        :param log_Mc: Feedback mass: all halos below the mass of 10.**log_Mc are stripped of their gas.
        :type log_Mc: float>12.1

        :param eta_b: Ratio between the thermal velocity of the gas and the escape velocity from the halo.
        :type eta_b: float

        :param z_c: Scale redshift of feedback.
        :type z_c: float

        :return: 2D array of shape ``(len(z), len(k))``
        """
    K, Z = np.meshgrid(k, z)
    if eta_b <= 0.0:
        raise ValueError('eta_b must be grater than 0.')
    ks = 55.0
    stellar = 1.0 + (K / ks) ** 2.0
    B0 = 0.105 * log_Mc - 1.27
    assert B0 > 0.0, 'log_Mc must be grater than 12.096'
    B = B0 * 1.0 / (1.0 + (Z / z_c) ** 2.5)
    k_g = 0.7 * (1.0 - B) ** 4.0 * eta_b ** (-1.6)
    scale_ratio = K / k_g
    suppression = B / (1.0 + scale_ratio ** 3.0) + (1.0 - B)
    return suppression * stellar


def WDM_suppression(k, z, M_wdm, Omega_cdm, h, nonlinear=False):
    r"""
        Suppression of the matter power spectrum due to (thermal) warm dark matter. In the linear
        case, the formula by https://arxiv.org/pdf/astro-ph/0501562.pdf is followed;
        otherwise the formula by https://arxiv.org/pdf/1107.4094.pdf is used.
        The linear formula is an approximation strictly valid only at :math:`k < 5-10 \ h/\mathrm{Mpc}`.
        The nonlinear formula has an accuracy of 2% level at :math:`z < 3` and for masses larger than 0.5 keV.

        .. warning::

         This function also exists in the class :func:`~colibri.cosmology.cosmo()`, where ``Omega_cdm`` and ``h`` are set to the values fixed at initialization of the class.

        .. warning::

         This function returns the total suppression in power. To obtain the suppression in the transfer function, take the square root of the output.

        :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
        :type k: array

        :param z: Redshifts.
        :type z: array

        :param M_wdm: Mass of the warm dark matter particle in keV.
        :type M_wdm: float

        :param Omega_cdm: Total matter density parameter today
        :type Omega_cdm: float

        :param h: Hubble constant in units of 100 km/s/Mpc
        :type h: float

        :param nonlinear: Whether to return non-linear transfer function.
        :type nonlinear: boolean, default = False

        :return: 2D array of shape ``(len(z), len(k))``
        """
    K, Z = np.meshgrid(k, z)
    if not nonlinear:
        alpha_linear = 0.049 * M_wdm ** (-1.11) * (Omega_cdm / 0.25) ** 0.11 * (h / 0.7) ** 1.22
        nu = 1.12
        return (1.0 + (alpha_linear * K) ** (2.0 * nu)) ** (-10.0 / nu)
    else:
        nu, l, s = (3.0, 0.6, 0.4)
        alpha = 0.0476 * (1.0 / M_wdm) ** 1.85 * ((1.0 + Z) / 2.0) ** 1.3
        return (1.0 + (alpha * K) ** (nu * l)) ** (-s / nu)