# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/colibri/weak_lensing.py
# Compiled at: 2020-04-14 11:56:34
import colibri.constants as const, colibri.cosmology as cc, numpy as np, scipy.interpolate as si, scipy.integrate as sint, colibri.fourier as FF
from six.moves import xrange
import colibri.nonlinear as NL
from math import sqrt

class weak_lensing:
    """
        The class :func:`~colibri.weak_lensing.weak_lensing` contains all the functions usefult to compute
        the shear power spectra and correlation functions in the flat sky and Limber's approximation.
        It also computes window functions and galaxy pdf. The initialization requires the redshifts and
        scales to integrate (this choice is dictated by the fact that in this way one can use power spectra
        from simulations). Also routines to compute the intrinsic alignment terms are present
        (linear and nonlinear alignment model by `Hirata & Seljak <https://arxiv.org/abs/astro-ph/0406275>`_.

        :param cosmology: Fixes the cosmological parameters. If not declared, the default values are chosen (see :func:`~colibri.cosmology.cosmo` documentation).
        :type cosmology: ``cosmo`` instance, default = ``cosmology.cosmo()``

        :param z_limits: Lower and upper limit of integration along the line of sight. This arguments avoids useless integration at high redshift, where there are essentially no galaxies. Both numbers must be non-negative and the first number must be smaller than the second. If the lower limit is set to 0, it will be enhanced by 1e-10 to avoid divergences at the origin of the lightcone.
        :type z_limits: 2-uple or list/array of length 2, default = (0., 5.)

        """

    def __init__(self, z_limits=(0.0, 5.0), cosmology=cc.cosmo()):
        self.cosmology = cosmology
        assert len(z_limits) == 2, 'Limits of integration must be a 2-uple or a list of length 2,with z_min at first place and z_max at 2nd place'
        assert z_limits[0] < z_limits[1], 'z_min (lower limit of integration) must be smaller than z_max (upper limit)'
        self.z_min = z_limits[0]
        self.z_max = z_limits[1]
        if self.z_min == 0.0:
            self.z_min += 1e-10
        self.nz_integration = int((self.z_max - self.z_min) * 40 + 2)
        self.z_integration = np.linspace(self.z_min, self.z_max, self.nz_integration)
        self.nz_windows = int((self.z_max - self.z_min) * 20 + 2)
        self.z_windows = np.linspace(self.z_min, self.z_max, self.nz_windows)
        self.geometric_factor = self.geometric_factor_f_K(self.z_integration)
        self.geometric_factor_windows = self.geometric_factor_f_K(self.z_windows)
        self.Hubble = self.cosmology.H_massive(self.z_integration) / self.cosmology.h
        self.Hubble_windows = self.cosmology.H_massive(self.z_windows) / self.cosmology.h

    def load_power_spectra(self, k, z, power_spectra=None, nonlinear=True, code='Class'):
        r"""
                This routine interpolates the total matter power spectrum (using the CDM prescription) in scales (units of :math:`h/\mathrm{Mpc}`) and redshifts. If `power_spectra` is set to ``None``, the power spectra are first computed at the scales and redshifts required and the interpolated; if `power_spectra` is not ``None``, it must be a 2D array of shape ``(len(z), len(k))`` which contains the power spectrum (in units of :math:`(\mathrm{Mpc}/h)^3`) evaluated at the scales and redshifts specified above.

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :param z: Redshifts at which power spectrum must be/is computed.
                :type z: array

                :param power_spectra: If given, it must be a 2D array of shape ``(len(z), len(k))`` which contains the power spectrum (in units of :math:`(\mathrm{Mpc}/h)^3`) evaluated at the scales and redshifts specified above.
                :type power_spectra: 2D NumPy array, default = ``None``

                :param nonlinear: Whether to return nonlinear power spectra. Used only if ``power_spectra`` is not ``None``.
                :type nonlinear: boolean, default = ``True``

                :param code: Which code use to compute the linear power spectrum. Used only if ``power_spectra`` is not ``None``.

                 - [`'Class'`, `'class'`, `'Xclass'`, `'XClass'`] for `CLASS <http://class-code.net/>`_
                 - [`'Camb'`, `'CAMB'`, `'camb'`, `'Xcamb'`, `'XCamb'`, `'XCAMB'`] for `CAMB <https://camb.info/>`_
                 - [`'EH'`, `'eh'`, `'Eisenstein-Hu'`] for Eisenstein-Hu (then turned non-linear with :func:`~colibri.nonlinear.halofit_operator`)

                :type code: string, default = `'Class'`.

                :return: Nothing, but a 2D-interpolated object ``self.power_spectra_interpolator`` containing :math:`P(k,z)` in units of :math:`(\mathrm{Mpc}/h)^3` is created
                """
        self.k = np.atleast_1d(k)
        self.z = np.atleast_1d(z)
        self.nk = len(k)
        self.nz = len(z)
        self.k_min = k.min()
        self.k_max = k.max()
        self.z_int_min = z.min()
        self.z_int_max = z.max()
        assert self.z_int_max >= self.z_max, 'Maximum redshift for power spectrum must be at least as large as the maximum redshift for integration (at least %.2f)' % self.z_max
        assert self.z_int_min <= self.z_min, 'Minimum redshift for power spectrum must be at least as small as the minimum redshift for integration (at most %.2f)' % self.z_min
        if self.nz > 3:
            kind_of_interpolation = 'cubic'
        else:
            kind_of_interpolation = 'linear'
        if power_spectra is None:
            f_nu = np.sum(self.cosmology.f_nu)
            f_cb = self.cosmology.f_cb
            if code in ('Class', 'class', 'Xclass', 'XClass'):
                k_lin, pk_lin = self.cosmology.class_XPk(z=self.z, k=self.k, var_1=['cb', 'nu'], var_2=['cb', 'nu'])
            elif code in ('Camb', 'CAMB', 'camb', 'Xcamb', 'XCamb', 'XCAMB'):
                k_lin, pk_lin = self.cosmology.camb_XPk(z=self.z, k=self.k, var_1=['cb', 'nu'], var_2=['cb', 'nu'])
            elif code in ('EH', 'eh', 'Eisenstein-Hu'):
                try:
                    k_lin, pk_eh = self.cosmology.EisensteinHu_Pk(z=self.z, k=self.k, sigma_8=self.cosmology.sigma_8)
                except TypeError:
                    raise TypeError('sigma_8 value is currently set to None in self.cosmology. Set it to a float.')

                pk_lin = {}
                pk_lin['cb-cb'] = pk_eh
                pk_lin['cb-nu'] = np.zeros_like(pk_eh)
                pk_lin['nu-nu'] = np.zeros_like(pk_eh)
            else:
                raise NameError('Boltzmann solver not recognized')
            if nonlinear == False:
                pk_m = f_cb ** 2.0 * pk_lin['cb-cb'] + 2.0 * f_nu * f_cb * pk_lin['cb-nu'] + f_nu ** 2.0 * pk_lin['nu-nu']
                self.power_spectra_interpolator = si.interp2d(self.k, self.z, pk_m, kind_of_interpolation)
            else:
                pk_lin_cb = pk_lin['cb-cb']
                do_nonlinear = NL.halofit_operator(z=self.z, k=self.k, pk=pk_lin_cb, cosmology=self.cosmology)
                k_hf, pk_hf = do_nonlinear.k, do_nonlinear.pk_nl
                pk_m = f_cb ** 2.0 * pk_hf + 2.0 * f_nu * f_cb * pk_lin['cb-nu'] + f_nu ** 2.0 * pk_lin['nu-nu']
                self.power_spectra_interpolator = si.interp2d(self.k, self.z, pk_m, kind_of_interpolation)
        else:
            self.power_spectra_interpolator = si.interp2d(self.k, self.z, power_spectra, kind_of_interpolation, fill_value=0.0)
        return

    def euclid_distribution(self, z, zmin, zmax, a=2.0, b=1.5, z_med=0.9):
        r"""
                Example function for the distribution of source galaxy. This distribution in particular is
                expected to be used in the Euclid mission:

                .. math::

                    n(z) \propto z^a \ \exp{\left[-\left(\frac{z}{z_{med}/\sqrt 2}\right)^b\right]}

                This distribution will eventually be normalized such that its integral on all redshifts is 1.

                :param z: Redshifts.
                :type z: array

                :param zmin: Lower edge of the bin.
                :type zmin: float

                :param zmax: Upper edge of the bin.
                :type zmax: float

                :param a: Parameter of the distribution.
                :type a: float, default = 1.5

                :param b: Parameter of the distribution.
                :type b: float, default = 1.5

                :param z_med: Median redshift of the distribution.
                :type z_med: float, default = 0.9

                :return: array
                """
        z_0 = z_med / sqrt(2.0)
        step = 0.01
        lower = 0.5 * (1.0 + np.tanh((z - zmin) / step))
        upper = 0.5 * (1.0 + np.tanh((zmax - z) / step))
        n = (z / z_0) ** a * np.exp(-(z / z_0) ** b) * lower * upper
        return n

    def euclid_distribution_with_photo_error(z, zmin, zmax, a=2.0, b=1.5, z_med=0.9, f_out=0.1, c_b=1.0, z_b=0.0, sigma_b=0.05, c_o=1.0, z_o=0.1, sigma_o=0.05):
        r"""
                Example function for the distribution of source galaxy. This distribution in particular is expected to be used in the Euclid mission. Here also the effect of photometric errors is included.

                .. math::

                 n^{(i)}(z) \propto \int_{z_i^-}^{z_i^+} dy \ z^a \ \exp{\left[-\left(\frac{z}{z_{med}/\sqrt 2}\right)^b\right]} \ p_\mathrm{ph}(y|z)

                where

                .. math::

                 p_\mathrm{ph}(y|z) = \frac{1-f_\mathrm{out}}{\sqrt{2\pi}\sigma_b(1+z)} \ \exp\left[-\frac{1}{2} \left(\frac{z-c_b y -z_b}{\sigma_b(1+z)}\right)^2\right] +

                 + \frac{f_\mathrm{out}}{\sqrt{2\pi}\sigma_o(1+z)} \ \exp\left[-\frac{1}{2} \left(\frac{z-c_o y -z_o}{\sigma_o(1+z)}\right)^2\right]

                :param z: Redshifts.
                :type z: array

                :param zmin: Lower edge of the bin.
                :type zmin: float

                :param zmax: Upper edge of the bin.
                :type zmax: float

                :param a: Parameter of the distribution.
                :type a: float, default = 1.5

                :param b: Parameter of the distribution.
                :type b: float, default = 1.5

                :param z_med: Median redshift of the distribution.
                :type z_med: float, default = 0.9

                :param f_out: Fraction of outliers
                :type f_out: float, default = 0.1

                :param c_b: Parameter of the Gaussian (normalization) representing the uncertainty on the photometric error for in-liers.
                :type c_b: float, default = 1.0

                :param z_b: Parameter of the Gaussian (scale-redshift) representing the uncertainty on the photometric error for in-liers.
                :type z_b: float, default = 0.0

                :param sigma_b: Parameter of the Gaussian (width) representing the uncertainty on the photometric error for in-liers.
                :type sigma_b: float, default = 0.05

                :param c_o: Parameter of the Gaussian (normalization) representing the uncertainty on the photometric error for out-liers.
                :type c_o: float, default = 1.0

                :param z_o: Parameter of the Gaussian (scale-redshift) representing the uncertainty on the photometric error for out-liers.
                :type z_o: float, default = 0.1

                :param sigma_o: Parameter of the Gaussian (width) representing the uncertainty on the photometric error for out-liers.
                :type sigma_o: float, default = 0.05

                :return: array
                """
        z_0 = z_med / sqrt(2.0)
        gal_distr = (z / z_0) ** a * np.exp(-(z / z_0) ** b)
        distr_in = (1.0 - f_out) / (2.0 * c_b) * (ss.erf((z - c_b * zmin - z_b) / (sqrt(2.0) * sigma_b * (1.0 + z))) - ss.erf((z - c_b * zmax - z_b) / (sqrt(2.0) * sigma_b * (1.0 + z))))
        distr_out = f_out / (2.0 * c_o) * (ss.erf((z - c_o * zmin - z_o) / (sqrt(2.0) * sigma_o * (1.0 + z))) - ss.erf((z - c_o * zmax - z_o) / (sqrt(2.0) * sigma_o * (1.0 + z))))
        photo_err_func = distr_in + distr_out
        return photo_err_func * gal_distr

    def gaussian_distribution(self, z, mean, sigma):
        """
                Example function for the distribution of source galaxy. Here we use a Gaussian galaxy distribution

                :param z: Redshifts.
                :type z: array

                :param mean: Mean redshift of the distribution.
                :type mean: float

                :param sigma: Width of the Gaussian
                :type sigma: float

                :return: array
                """
        exponent = -0.5 * ((z - mean) / sigma) ** 2.0
        return np.exp(exponent)

    def constant_distribution(z, zmin, zmax):
        """
                Example function for the distribution of source galaxy. Here we use a constant distribution of sources.

                :param z: Redshifts.
                :type z: array

                :param zmin: Lower edge of the bin.
                :type zmin: float

                :param zmax: Upper edge of the bin.
                :type zmax: float

                :return: array
                """
        step = 0.01
        lower = 0.5 * (1.0 + np.tanh((z - zmin) / step))
        upper = 0.5 * (1.0 + np.tanh((zmax - z) / step))
        n = z ** 0.0 * lower * upper
        return n

    def comoving_distance(self, z, z0=0.0):
        """
                Comoving distance between two redshifts. It assumes neutrinos as matter.
                This latter assumption introduces a bias of less than 0.02% at :math:`z<10` for even the lowest
                neutrino masses allowed by particle physics.

                :param z: Redshifts.
                :type z: array

                :param z0: Pivot redshift.
                :type z0: float, default = 0

                :return: array
                """
        c = const.c
        z = np.atleast_1d(z)
        length = len(z)
        result = np.zeros(length)
        for i in xrange(length):
            result[i], _ = sint.quad(lambda x: c * 1.0 / (self.cosmology.H_massive(x) / self.cosmology.h), z0, z[i], epsabs=1e-08)

        return result

    def geometric_factor_f_K(self, z, z0=0.0):
        """
                Geometric factor (distance) between two given redshifts ``z`` and ``z0``. It assumes neutrinos as matter. This latter assumption introduces a bias of less than 0.02 % at :math:`z<10` for even the lowest neutrino masses allowed by particle physics.

                :param z: Redshifts.
                :type z: array

                :param z0: Pivot redshift.
                :type z0: float, default = 0

                :return: array
                """
        K = self.cosmology.K
        chi_z = self.comoving_distance(z, z0)
        if K == 0.0:
            return chi_z
        else:
            if K > 0.0:
                return 1.0 / K ** 0.5 * np.sin(K ** 0.5 * chi_z)
            return 1.0 / np.abs(K) ** 0.5 * np.sinh(np.abs(K) ** 0.5 * chi_z)

    def load_window_functions(self, galaxy_distributions):
        r"""
                This function computes the window function to use in the shear power spectrum, evaluated at
                ``self.z_integration``. It automatically normalizes the galaxy distribution function such that the
                integral over redshifts is 1. It does not return anything but it creates the quantities
                ``self.window_function`` and ``self.window_function_IA`` (for shear and intrinsic aligment signals).
                Given a galaxy distribution :math:`n^{(i)}(z)` in the `i`-th bin:

                .. math::

                   W^{(i)}(z) = \frac{3}{2}\Omega_m \ \frac{H_0^2}{c^2} \ f_K[\chi(z)] (1+z) \int_z^\infty dx \ n^{(i)}(x) \ \frac{f_K[\chi(z-x)]}{f_K[\chi(z)]}

                .. math::

                   W^{(i)}_{IA}(z) = n^{(i)}(z) \frac{H(z)}{c}

                :param galaxy_distributions: The distribution of galaxies in each bin for which the shear spectra need to be computed. A list of functions containing the distribution of galaxies in each bin considered. Every element of this list is in turn a list. The first element is the name of a defined function describing a galaxy distribution in redshift. The first argument of said function must be redshift. All the other arguments must be specified by the second element of the list, which is a dictionary.
                :type galaxy_distributions: nested list 

                An example call can be, for 3 bins all with a :func:`~colibri.weak_lensing.euclid_distribution` with default arguments for ``a`` and ``b`` but different bin edges ``zmin``, ``zmax``:

                .. code-block:: python

                   self.load_window_functions(galaxy_distributions = [[self.euclid_distribution, {'zmin': 0.00, 'zmax': 0.72}],
                                                                      [self.euclid_distribution, {'zmin': 0.72, 'zmax': 1.11}],
                                                                      [self.euclid_distribution, {'zmin': 1.11, 'zmax': 5.00}]])

                :return: Nothing, but the quantities ``self.window_function`` and ``self.window_function_IA`` will be created: these are lists of length ``len(galaxy_distributions)`` of interpolated functions from ``z_limits.min()`` to ``z_limits.max()``.

                """
        n_bins = len(galaxy_distributions)
        norm_const = [ sint.quad(lambda x: galaxy_distributions[i][0](x, **galaxy_distributions[i][1]), 0.0, np.inf)[0]
         for i in range(n_bins) ]
        zz_tmp = np.linspace(self.z_integration.min(), self.z_integration.max(), 1001)
        self.window_function = []
        self.window_function_IA = []
        constant = 3.0 / 2.0 * self.cosmology.Omega_m * (self.cosmology.H0 / self.cosmology.h / const.c) ** 2.0 * (1.0 + self.z_windows) * self.geometric_factor_windows
        for galaxy_bin in xrange(n_bins):
            n_z = galaxy_distributions[galaxy_bin][0]
            args = galaxy_distributions[galaxy_bin][1]
            integral = list(map(lambda z_i: sint.quad(lambda x: n_z(x, **args) * self.geometric_factor_f_K(x, z_i) / self.geometric_factor_f_K(x), z_i, self.z_max, epsrel=0.001)[0], self.z_windows))
            window_function_tmp = constant * integral / norm_const[galaxy_bin]
            window_function_IA_tmp = n_z(self.z_windows, **args) * self.Hubble_windows / const.c / norm_const[galaxy_bin]
            self.window_function.append(si.Akima1DInterpolator(self.z_windows, window_function_tmp))
            self.window_function_IA.append(si.interp1d(self.z_integration, n_z(self.z_integration, **args) * self.Hubble / const.c / norm_const[galaxy_bin], 'cubic'))

    def intrinsic_alignment_kernel(self, A_IA, k, z, IA_model='linear alignment', **kwargs):
        r"""
                Intrinsic alignment correction function.

                :param A_IA: Intrinsic alignment amplitude.
                :type A_IA: float

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :param z: Redshifts at which the function must be computed.
                :type z: array

                :param IA_model: Model to use to implement linear alignment. Implemented models are

                  - `'linear alignment'`, `'Linear Alignment'`, `'linear_alignment'`, `'la'`, `'LA'` for Linear alignment
                  - `'non-linear alignment'`, `'nonlinear alignment'`, `'nla'`, `'NLA'` for Non-linear alignment

                :type IA_model: string, default = 'linear alignment'

                :param kwargs: Keyword arguments for the IA function.

                :return: 2D array containing the correction function :math:`F(k,z)` for intrinsic alignment
                """
        C1 = 5e-14
        front = -A_IA * C1 * self.cosmology.rho_crit(z=0.0) * self.cosmology.Omega_m
        k = np.array(k)
        nk = len(np.atleast_1d(k))
        nz = len(np.atleast_1d(z))
        growth = self.cosmology.D_cbnu(k=k, z=z)
        if IA_model in ('linear alignment', 'Linear Alignment', 'linear_alignment',
                        'la', 'LA'):
            return front * 1.0 / growth
        if IA_model in ('non-linear alignment', 'nonlinear alignment', 'nla', 'NLA'):
            return front * 1.0 / growth * np.tile(self.nonlinear_alignment_term(z=z, **kwargs), nk).reshape(nz, -1)
        raise NameError('Instrinsic alignment model unknown')

    def nonlinear_alignment_term(self, L_mean, z, eta_IA, beta, L0=46000000000.0, z0=0.62):
        r"""
                Non-linear alignment term, goes directly into self.intrinsic_alignment_kernel.

                :param L_mean: Average luminosity of galaxies in :math:`L_\odot`
                :type L_mean: float

                :param z: Redshifts at which the function must be computed.
                :type z: array

                :param eta_IA: Exponent for redshift dependence of intrinsic alignment.
                :type eta_IA: float

                :param beta: Exponent for luminosity dependence of intrinsic alignment.
                :type beta: float

                :param L0: Pivot luminosity.
                :type L0: float, default = 4.6e10, corresponding to an absolute `r`-band magnitude of -22

                :param z0: Pivot redshift.
                :type z0: float, default = 0.62

                :return: array
                """
        return ((1.0 + z) / (1.0 + z0)) ** eta_IA * (L_mean / L0) ** beta

    def shear_power_spectrum(self, l, IA=None, kwargs_power_spectra={}, kwargs_IA={}):
        r"""
                This function computes the shear power spectrum using the Limber's and the flat-sky approximations.
                Given two redshift bins `i` and `j` the equation is

                .. math::

                  C^{(ij)}(\ell) = \int_0^\infty dz \ \frac{c}{H(z)} \ \frac{W^{(i)}(z) W^{(j)}(z)}{f_K^2[\chi(z)]} \ P\left(\frac{\ell}{f_K[\chi(z)]}, z\right),

                where :math:`P(k,z)` is the matter power spectrum and :math:`W^{(i)}(z)` are the window functions.

                :param l: Multipoles at which to compute the shear power spectra.
                :type l: array

                :param IA: Intrinsic alignment model to implement. Together with ``kwargs_IA`` defines the kernel for the calculation of the intrinsic alignment terms. If set to ``None``, these terms will be set to zero.

                  - `'linear alignment'`, `'Linear Alignment'`, `'linear_alignment'`, `'la'`, `'LA'` for Linear alignment
                  - `'non-linear alignment'`, `'nonlinear alignment'`, `'nla'`, `'NLA'` for Non-linear alignment

                :type IA: string, default = ``None``
                    

                :param kwargs_power_spectra: Keyword arguments to pass to ``self.load_power_spectra`` (used only if ``power_spectra == None``).
                :type kwargs_power_spectra: dictionary, default = {}
                    
                :param kwargs_IA: Keyword arguments to pass to intrinsic alignment model (used only if ``IA != None``)
                :type kwargs_IA: dictionary, default = {}

                :return: shear power spectrum :math:`C^{(ij)}(\ell)` for all bin pairs whose window function was generated by :func:`~colibri.weak_lensing.load_window_functions`.
                :rtype:  dictionary containing 3 keys:

                    - ``'GG'``: shear power spectrum;
                    - ``'GI'``: galaxy-IA term;
                    - ``'II'``: IA-IA term.

                    Each key is a 3-D array whose entries are ``Cl[bin i, bin j, multipole l]``
                """
        try:
            n_bin = len(self.window_function)
        except AttributeError:
            raise AttributeError('Load window functions using the self.load_window_functions method')

        zz = self.z_integration
        n_l = len(np.atleast_1d(l))
        n_z = self.nz_integration
        HH = self.Hubble
        Cl = {'GG': np.zeros((n_bin, n_bin, n_l)), 'GI': np.zeros((n_bin, n_bin, n_l)), 
           'II': np.zeros((n_bin, n_bin, n_l))}
        try:
            power_spectra = self.power_spectra_interpolator
        except AttributeError:
            print "Power spectra not found, loading them using 'load_power_spectra' method with arguments from 'kwargs_power_spectra'"
            self.load_power_spectra(**kwargs_power_spectra)
            power_spectra = self.power_spectra_interpolator

        assert np.atleast_1d(l).min() > self.k_min * self.geometric_factor_f_K(self.z_min), "Minimum 'l' is too low. Extend to lower k_min? Use lower z_min?"
        assert np.atleast_1d(l).max() < self.k_max * self.geometric_factor_f_K(self.z_max), "Maximum 'l' is too high. Extend to higher k_max? Use higher z_min?"
        PS = np.zeros((n_l, n_z))
        for il in xrange(n_l):
            for iz in range(n_z):
                PS[(il, iz)] = power_spectra(l[il] * 1.0 / self.geometric_factor[iz], zz[iz])

        windows = np.array([ self.window_function[i](zz) for i in xrange(n_bin) ])
        for i in xrange(n_bin):
            for j in xrange(n_bin):
                Cl['GG'][(i, j)] = [ sint.simps(const.c / HH * windows[i] * windows[j] * PS[xx] / self.geometric_factor ** 2.0, x=zz) for xx in range(len(np.atleast_1d(l))) ]

        if IA != None:
            IA_windows = np.array([ self.window_function_IA[i](zz) for i in xrange(n_bin) ])
            F_IA = self.intrinsic_alignment_kernel(k=self.k, z=zz, IA_model=IA, **kwargs_IA)
            F_IA_interp = si.interp2d(self.k, zz, F_IA, kind='cubic')
            for i in xrange(n_bin):
                for j in xrange(n_bin):
                    for il in xrange(n_l):
                        F = np.zeros(n_z)
                        for iz in xrange(n_z):
                            F[iz] = F_IA_interp(l[il] * 1.0 / self.geometric_factor[iz], zz[iz])

                        Cl['GI'][(i, j, il)] = sint.simps(const.c / HH * (IA_windows[i] * windows[j] + IA_windows[j] * windows[i]) * F * PS[il] / self.geometric_factor ** 2.0, x=zz)
                        Cl['II'][(i, j, il)] = sint.simps(const.c / HH * IA_windows[i] * IA_windows[j] * F ** 2.0 * PS[il] / self.geometric_factor ** 2.0, x=zz)

        return Cl

    def shear_correlation_functions(self, theta, IA=None, kwargs_power_spectra={}, kwargs_IA={}):
        r"""
                This function computes the two shear correlation functions using the Limber's and the flat-sky approximations. It first computes :func:`~colibri.weak_lensing.shear_power_spectrum` and then computes its Hankel transform with :func:`~colibri.fourier.Hankel` (therefore this function requires the ``FFTlog`` package)

                .. math::

                    \xi_{+/-}^{(ij)}(\theta) = \int_0^\infty \frac{d\ell}{2\pi} \ \ell \ C^{(ij)}(\ell) \ J_{0/4} (\ell\theta)

                :param theta: Angles (in :math:`\mathrm{arcmin}` units) where to compute the shear correlation functions
                :type theta: array

                :param IA: Intrinsic alignment model to implement. Together with ``kwargs_IA`` defines the kernel for the calculation of the intrinsic alignment terms. If set to ``None``, these terms will be set to zero.

                  - `'linear alignment'`, `'Linear Alignment'`, `'linear_alignment'`, `'la'`, `'LA'` for Linear alignment
                  - `'non-linear alignment'`, `'nonlinear alignment'`, `'nla'`, `'NLA'` for Non-linear alignment

                :type IA: string, default = ``None``
                    

                :param kwargs_power_spectra: Keyword arguments to pass to ``self.load_power_spectra`` (used only if ``power_spectra == None``).
                :type kwargs_power_spectra: dictionary, default = {}
                    
                :param kwargs_IA: Keyword arguments to pass to intrinsic alignment model (used only if ``IA != None``)
                :type kwargs_IA: dictionary, default = {}

                :return: shear correlation functions :math:`\xi_+^{(ij)}(\theta)` and :math:`\xi_-^{(ij)}(\theta)` for all bins whose window function was generated by :func:`~colibri.weak_lensing.load_window_functions`.

                :rtype: two dictionaries each containing 3 keys:

                    - ``'GG'``: shear power spectrum;
                    - ``'GI'``: galaxy-IA term;
                    - ``'II'``: IA-IA term.

                    Each key is a 3-D array whose entries are ``Cl[bin i, bin j, multipole l]``
                """
        l = np.geomspace(1.0, 500000.0, 256)
        zz = self.z_integration
        n_theta = len(np.atleast_1d(theta))
        n_z = self.nz_integration
        HH = self.Hubble
        Cl = self.shear_power_spectrum(l=l, IA=IA, kwargs_power_spectra=kwargs_power_spectra, kwargs_IA=kwargs_IA)
        NN = 8192
        n_bin = len(self.window_function)
        xi_plus_tmp = {'GG': np.zeros((n_bin, n_bin, NN)), 'GI': np.zeros((n_bin, n_bin, NN)), 
           'II': np.zeros((n_bin, n_bin, NN))}
        xi_minus_tmp = {'GG': np.zeros((n_bin, n_bin, NN)), 'GI': np.zeros((n_bin, n_bin, NN)), 
           'II': np.zeros((n_bin, n_bin, NN))}
        xi_plus = {'GG': np.zeros((n_bin, n_bin, n_theta)), 'GI': np.zeros((n_bin, n_bin, n_theta)), 
           'II': np.zeros((n_bin, n_bin, n_theta))}
        xi_minus = {'GG': np.zeros((n_bin, n_bin, n_theta)), 'GI': np.zeros((n_bin, n_bin, n_theta)), 
           'II': np.zeros((n_bin, n_bin, n_theta))}
        for i in range(n_bin):
            for j in range(n_bin):
                theta_tmp, xi_plus_tmp['GG'][(i, j)] = FF.Hankel(l, Cl['GG'][(i, j)] / (2.0 * np.pi), order=0, N=NN)
                theta_tmp, xi_minus_tmp['GG'][(i, j)] = FF.Hankel(l, Cl['GG'][(i, j)] / (2.0 * np.pi), order=4, N=NN)
                if IA != None:
                    for component in ['GI', 'II']:
                        theta_tmp, xi_plus_tmp[component][(i, j)] = FF.Hankel(l, Cl[component][(i, j)] / (2.0 * np.pi), order=0, N=NN)
                        theta_tmp, xi_minus_tmp[component][(i, j)] = FF.Hankel(l, Cl[component][(i, j)] / (2.0 * np.pi), order=4, N=NN)

        theta_tmp *= 180.0 / np.pi * 60.0
        for i in range(n_bin):
            for j in range(n_bin):
                for comp in ['GG', 'GI', 'II']:
                    xi_plus_interp = si.interp1d(theta_tmp, xi_plus_tmp[comp][(i, j)], 'cubic')
                    xi_minus_interp = si.interp1d(theta_tmp, xi_minus_tmp[comp][(i, j)], 'cubic')
                    xi_plus[comp][(i, j)] = xi_plus_interp(theta)
                    xi_minus[comp][(i, j)] = xi_minus_interp(theta)

        del xi_plus_tmp
        del xi_minus_tmp
        return (xi_plus, xi_minus)