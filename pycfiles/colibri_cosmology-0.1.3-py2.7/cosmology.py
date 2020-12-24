# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/colibri/cosmology.py
# Compiled at: 2020-05-11 06:18:30
import colibri.constants as const, numpy as np, scipy.special as ss, scipy.integrate as sint, scipy.interpolate as si, scipy.misc as sm, colibri.useful_functions as UF, sys, warnings
from six.moves import xrange
from six import iteritems
try:
    from classy import Class
except ImportError:
    pass

try:
    import camb
except ImportError:
    pass

class cosmo:
    r"""
        The class ``cosmo`` takes as arguments a set of cosmological parameters and returns a ``cosmo`` instance,
        which contains several methods to compute useful cosmological quantities, such as distances, ages,
        scales, power spectra and evolution of cosmological parameters.
        This class supports :math:`\Lambda\mathrm{CDM}` cosmologies as well as massive neutrinos,
        evolving dark energy models and non-flat geometries.
        It accepts the following arguments, with the default values specified:

        :param Omega_m: Matter density parameter today (including massive neutrinos), :math:`\Omega_m`.
        :type Omega_m: float, default = 0.3089

        :param Omega_b: Baryon density parameter today (including massive neutrinos), :math:`\Omega_b`.
        :type Omega_b: float, default = 0.0486

        :param Omega_K: Curvature density parameter today (including massive neutrinos), :math:`\Omega_K`.
        :type Omega_K: float, default = 0
            
        :param N_nu: Number of active neutrino species.
        :type N_nu: int, default = 3

        :param M_nu: Neutrino masses expressed in eV. Its size must be <= ``N_nu``. When ``cosmo`` is called, this quantity will be transformed to an array (``self.M_nu``) of length ``N_nu`` containing the non-vanishing neutrino masses assigned here padded with zeros in order to reach ``N_nu``. E.g.: if ``M_nu = [0.2, 0.1]`` and ``N_nu = 3``, then ``self.M_nu`` will become ``[0.2, 0.1, 0.0]``.
        :type M_nu: float or list of floats, default = 0.

        :param N_eff: Effective number of neutrinos. This number should be greater than ``N_nu``.
        :type N_eff: float, default = 3.046

        :param As: Amplitude of primordial scaled perturbations. At least one between this and `sigma_8` must be different from None. If `As` is not None, it will be the parameter used to compute the amplitude of the power spectrum.
        :type As: float, default = 2.14e-9

        :param sigma_8: Root mean square amplitude fluctuation on scales of 8 :math:`\mathrm{Mpc}/h`. At least one between this         and `sigma_8` must be different from None. If ``sigma_8`` is not None, and ``As`` is None, the former will be the parameter used to compute the amplitude of the power spectrum.
        :type sigma_8: float, default = ``None``

        :param ns: Spectral index of scalar primordial perturbations.
        :type ns: float, default = 0.9667

        :param h: Hubble constant in units of 100 km/s/Mpc.
        :type h: float, default = 0.6774

        :param w0: Dark energy parameter of state today.
        :type w0: float, default = -1

        :param wa: Evolution of dark energy parameter of state.
        :type wa: float, default = 0

        :param tau: Optical depth to reionization.
        :type tau: float, default = 0.06

        :param T_cmb: CMB temperature today.
        :type T_cmb: float, default = 2.7255

        After initialization, the following quantities will be stored

        :param H0: Hubble constant in km/s/Mpc, i.e. :math:`100 h`.
        :param Omega_lambda: Dark energy/cosmological constant density parameter, :math:`\Omega_\Lambda`.
        :param Omega_nu: Neutrino density parameters, :math:`\Omega_\nu`.
        :param Omega_cdm: Cold dark matter density parameter today, :math:`\Omega_{cdm}`.
        :param Omega_cb: Cold dark matter + baryons density parameter today, :math:`\Omega_{cb}`.
        :param Omega_gamma: Photon density parameter today, :math:`\Omega_\gamma`.
        :param omega_m: Reduced matter density parameter today, :math:`\Omega_m h^2`.
        :param omega_cdm: Reduced cold dark matter density parameter today, :math:`\Omega_{cdm} h^2`.
        :param omega_cb: Reduced cold dark matter density parameter today, :math:`\Omega_{cb} h^2`.
        :param omega_b: Reduced baryon parameter today, :math:`\Omega_{b} h^2`.
        :param omega_nu: Reduced neutrino parameter today, :math:`\Omega_\nu h^2`.
        :param omega_gamma: Reduced photon density parameter today, :math:`\Omega_\gamma h^2`.
        :param omega_K: Reduced curvature parameter today, :math:`\Omega_K h^2`.
        :param massive_nu: Number of massive neutrinos.
        :param massless_nu: Number of massless neutrinos, :math:`N_{eff} - N_{massive \ \nu}`
        :param Omega_massive_nu: Massive neutrino density parameters today.
        :param Omega_massless_nu: Massless neutrino density parameters today.
        :param log10_As: If ``As`` is not None, base-10 logarithm of initial scalar amplitude.
        :param f_nu: Neutrino fractions, in units of :math:`\Omega_m`.
        :param f_nu_tot: Sum of neutrino fractions.
        :param f_b: Baryon fraction in units of :math:`\Omega_m`.
        :param f_c: Cold dark matter fraction in units of :math:`\Omega_m`.
        :param f_cb: Cold dark matter plus baryon fraction in units of :math:`\Omega_m`.
        :param Gamma_nu: Neutrino-to-photon temperature ratio.
        :param T_nu: Neutrino temperature today.
        :param M: Array of masses, used to sample (e.g.) mass functions
        :type M: array of 512 equally-spaced logarithmic bins from :math:`10^2` to :math:`10^{18} \ M_\odot/h`.
        :param delta_sc: Critical overdensity for spherical collapse (linear theory extrapolation), :math:`\delta_{sc} = \frac{3}{20} \left(12\pi\right)^{2/3} \approx 1.686`.
        :param eta_sc: Time of shell-crossing (radians), :math:`\eta_{sc} \approx 3.488`.
        :param delta_v: Critical underdensity for voids (linear theory extrapolation), :math:`\delta_v = - \frac{3}{20} \left[6 (\sinh \eta_{sc}-\eta_{sc})\right]^{2/3} \approx -2.717`.
        """

    def __init__(self, Omega_m=0.3089, Omega_b=0.0486, Omega_K=0.0, N_nu=3, M_nu=0.0, N_eff=3.046, As=2.14e-09, ns=0.9667, sigma_8=None, h=0.6774, w0=-1.0, wa=0.0, tau=0.06, T_cmb=2.7255):
        assert N_nu <= N_eff, 'Number of active neutrinos must be smaller than N_eff'
        assert len(np.atleast_1d(M_nu)) <= N_nu, 'Provided a number of neutrino masses greater than the actual number of neutrinos. Set N_nu to be at least equal to the length of M_nu'
        if As is None and sigma_8 is None:
            raise AssertionError('At least one between As and sigma_8 must be different from None.')
        self.Omega_m = Omega_m
        self.Omega_b = Omega_b
        self.Omega_K = Omega_K
        self.N_nu = N_nu
        self.M_nu = np.pad(np.atleast_1d(M_nu), (0, self.N_nu - len(np.atleast_1d(M_nu))), 'constant')
        self.N_eff = N_eff
        self.Gamma_nu = (4.0 / 11.0) ** (1.0 / 3.0) * (N_eff / self.N_nu) ** 0.25
        self.massive_nu = np.count_nonzero(self.M_nu)
        self.massless_nu = self.N_eff - self.massive_nu
        self.As = As
        if As is not None:
            self.log10_As = np.log10(As)
        self.sigma_8 = sigma_8
        self.ns = ns
        self.w0 = w0
        self.wa = wa
        self.tau = tau
        self.T_cmb = T_cmb
        self.T_nu = T_cmb * self.Gamma_nu
        self.theta = T_cmb / 2.7
        self.h = h
        self.H0 = 100.0 * self.h
        self.K = -self.Omega_K * (self.H0 / self.h / const.c) ** 2.0
        self.delta_sc = 3.0 / 20.0 * (12.0 * const.PI) ** (2.0 / 3.0)
        self.eta_sc = 3.48752242
        self.delta_v = -3.0 / 20.0 * (6.0 * (np.sinh(self.eta_sc) - self.eta_sc)) ** (2.0 / 3.0)
        self.M = np.logspace(2.0, 18.0, 512)
        self.Omega_gamma = const.alpha_BB * self.T_cmb ** 4.0 / (const.c * 1000.0) ** 2.0 / const.Msun * 1000.0 * const.Mpc_to_m ** 3.0 / const.rhoch2 / self.h ** 2.0
        self.Omega_nu = 15.0 / const.PI ** 4.0 * self.Gamma_nu ** 4.0 * self.Omega_gamma * np.array([ self.FermiDirac_integral(x / (const.kB * self.T_nu)) for x in self.M_nu ])
        self.Omega_cdm = self.Omega_m - self.Omega_b - np.sum(self.Omega_nu)
        self.Omega_cb = self.Omega_cdm + Omega_b
        self.Omega_lambda = 1.0 - self.Omega_cb - np.sum(self.Omega_nu) - self.Omega_K - self.Omega_gamma
        self.Omega_massive_nu = self.Omega_nu[np.where(self.M_nu != 0.0)]
        self.Omega_massless_nu = self.Omega_nu[np.where(self.M_nu == 0.0)]
        self.omega_m = Omega_m * h ** 2.0
        self.omega_b = Omega_b * h ** 2.0
        self.omega_K = Omega_K * h ** 2.0
        self.omega_cdm = self.Omega_cdm * h ** 2.0
        self.omega_cb = self.Omega_cb * h ** 2.0
        self.omega_nu = self.Omega_nu * h ** 2.0
        self.omega_gamma = self.Omega_gamma * h ** 2.0
        self.f_nu = self.Omega_nu / self.Omega_m
        self.f_nu_tot = np.sum(self.f_nu)
        self.f_cb = self.Omega_cb / self.Omega_m
        self.f_b = self.Omega_b / self.Omega_m
        self.f_c = self.Omega_cdm / self.Omega_m
        return

    def scale_factor(self, z=0.0):
        """
                Returns the scale factor given the redshift.

                :param z: Redshift.
                :type z: float, default = 0.0

                :return: float
                """
        return 1.0 / (1.0 + z)

    def redshift(self, a=1.0):
        """
                Returns the redshift given the scale factor.

                :param a: Scale factor.
                :type a: float, default = 1.0

                :return: float
                """
        return 1.0 / a - 1.0

    def age(self, z=0.0):
        r"""
                Cosmic time from Big Bang in :math:`\mathrm{Myr}`.

                :param z: Redshift.
                :type z: float, default = 0.0

                :return: float
                """
        integrand = lambda x: const.Mpc_to_km / (self.H(x) * (1.0 + x)) / const.Myr_to_s
        age, _ = sint.quad(integrand, z, np.inf)
        return age

    def lookback_time(self, z=1.0):
        """
                Cosmic time from today to a given redshift in Myr.

                :param z: Redshift.
                :type z: float, default = 1.0

                :return: float
                """
        integrand = lambda x: const.Mpc_to_km / (self.H(x) * (1.0 + x)) / const.Myr_to_s
        lookback, _ = sint.quad(integrand, 0.0, z)
        return lookback

    def Omega_cdm_z(self, z):
        r"""
                Cold dark matter density parameter at a given redshift

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{cdm}(z)`.
                """
        return self.Omega_cdm * (1.0 + z) ** 3.0 * (self.H0 / self.H(z)) ** 2.0

    def Omega_b_z(self, z):
        r"""
                Baryon density parameter at a given redshift

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{b}(z)`.
                """
        return self.Omega_b * (1.0 + z) ** 3.0 * (self.H0 / self.H(z)) ** 2.0

    def Omega_cb_z(self, z):
        r"""
                Cold dark matter plus baryon density parameter at a given redshift

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{cb}(z)`.
                """
        return self.Omega_cb * (1.0 + z) ** 3.0 * (self.H0 / self.H(z)) ** 2.0

    def FermiDirac_integral(self, y):
        r"""
                It computes the integral

                .. math::

                    \mathcal F(y) = \int_0^\infty dx \ x^2 \ \frac{(x^2+y^2)^{1/2}}{e^x+1},

                useful to compute the neutrino parameter of state
                :math:`w_\nu = \frac{1}{3}\left[1-\frac{\mathrm{d}\ln\mathcal F}{\mathrm{d} \ln y}\right]`

                :param y: Quantity related to neutrino mass, namely :math:`\frac{M_\nu}{(1+z) k_B T_\nu}`.
                :type y: float

                :return: float
                """
        result, _ = sint.quad(lambda x: x ** 2 * np.sqrt(x ** 2 + y ** 2) * 1.0 / (np.exp(x) + 1.0), 0.0, 100.0)
        return result

    def Omega_nu_z(self, z):
        r"""
                Neutrino density parameters at a given redshift.

                :param z: Redshifts.
                :type z: array

                :return: array of shape ``(self.N_nu, len(z))`` containing :math:`\Omega_\nu(z)`.
                
                """
        mnu = np.atleast_1d(self.M_nu)
        zz = np.atleast_1d(np.array(z))
        onuz = np.zeros((len(mnu), len(np.atleast_1d(z))))
        for i in xrange(len(mnu)):
            y = mnu[i] / ((1.0 + zz) * const.kB * self.T_nu)
            F = np.array(list(map(self.FermiDirac_integral, y)))
            onuz[i] = 15.0 / const.PI ** 4.0 * self.Omega_gamma * F * self.Gamma_nu ** 4.0 * (1.0 + zz) ** 4.0 * self.H0 ** 2.0 / self.H(zz) ** 2.0

        return onuz

    def Omega_m_z(self, z):
        r"""
                Matter density parameter at a given redshift.

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{m}(z)`.
                """
        return self.Omega_cdm_z(z) + self.Omega_b_z(z) + np.sum(self.Omega_nu_z(z), axis=0)

    def Omega_lambda_z(self, z):
        r"""
                Dark energy density parameter at a given redshift.

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{\Lambda}(z)`.
                """
        w_DE = self.w0 + self.wa * z / (1.0 + z)
        return self.Omega_lambda * (1.0 + z) ** (3.0 * (1.0 + w_DE)) * (self.H0 / self.H(z)) ** 2.0

    def Omega_K_z(self, z):
        r"""
                Curvature density parameter at a given redshift.

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{K}(z)`.
                """
        return self.Omega_K * (1.0 + z) ** 2.0 * (self.H0 / self.H(z)) ** 2.0

    def Omega_gamma_z(self, z):
        r"""
                Photon density parameter at a given redshift.

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`\Omega_{\gamma}(z)`.
                """
        return self.Omega_gamma * (1.0 + z) ** 4.0 * (self.H0 / self.H(z)) ** 2.0

    def w_DE(self, z):
        """
                Dark energy parameter of state ad function of redshift.

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`w_{de}(z)`.
                """
        return self.w0 + self.wa * z / (1.0 + z)

    def H(self, z):
        """
                Hubble function in km/s/Mpc. 

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`H(z)` in units of km/s/Mpc.
                """
        wde = self.w0 + self.wa * (z / (1.0 + z))
        y = np.outer(self.M_nu / (const.kB * self.T_nu), 1.0 / (1.0 + z))
        F = np.zeros_like(y)
        for i in xrange(len(np.atleast_1d(y))):
            F[i] = np.array(list(map(self.FermiDirac_integral, np.atleast_1d(y[i]))))

        neutrino_contribution = 15.0 / const.PI ** 4.0 * self.Gamma_nu ** 4.0 * self.Omega_gamma * F * (1.0 + z) ** 4.0
        return self.H0 * (self.Omega_cb * (1.0 + z) ** 3.0 + self.Omega_gamma * (1.0 + z) ** 4.0 + self.Omega_lambda * (1.0 + z) ** (3.0 * (1.0 + wde)) + self.Omega_K * (1.0 + z) ** 2.0 + np.sum(neutrino_contribution, axis=0)) ** 0.5

    def H_massive(self, z):
        r"""
                Hubble function in km/s/Mpc. It assumes that all neutrinos are pure matter and therefore
                :math:`w_\nu = 0`.
                For the minimum neutrino masses allowed by particle physics, assuming normal hierarchy
                and the correct differences of square masses, the error committed is about 0.01% at :math:`z=0`,
                0.5% at :math:`z = 100`, 5% at :math:`z = 1000` and 30% at :math:`z = \infty`. 

                :param z: Redshifts.
                :type z: array

                :return: array with :math:`H(z)` in units of km/s/Mpc.

                """
        return self.H0 * (self.Omega_cb * (1.0 + z) ** 3.0 + np.sum(self.Omega_nu) * (1.0 + z) ** 3.0 + self.Omega_lambda * (1.0 + z) ** (3.0 * (1.0 + self.w0 + self.wa * (z / (1.0 + z)))) + self.Omega_gamma * (1.0 + z) ** 4.0 + self.Omega_K * (1.0 + z) ** 2.0) ** 0.5

    def q_acc(self, z):
        """
                Acceleration parameter at a given redshift.

                :param z: Redshifts.
                :type z: array

                :return: array.
                """
        return self.Omega_gamma_z(z) + self.Omega_m_z(z) / 2.0 - self.Omega_lambda_z(z)

    def rho_crit(self, z):
        r"""
                Critical density of the Universe at a given redshift in units of :math:`h^2 M_\odot \mathrm{Mpc}^{-3}`.

                :param z: Redshifts.
                :type z: array

                :return: array.
                """
        return 3.0 * self.H(z) ** 2.0 / (8.0 * const.PI * const.G) / self.h ** 2.0

    def rho(self, z):
        r"""
                Matter density of the Universe at a given redshift in units of :math:`h^2 M_\odot \mathrm{Mpc}^{-3}`.

                :param z: Redshifts.
                :type z: array

                :return: array.
                """
        return self.rho_crit(z) * self.Omega_m_z(z)

    def z_eq(self):
        """
                Redshift at which radiation and matter had the same density.

                :return: float.
                """
        theta = self.T_cmb / 2.7
        return 25000.0 * self.Omega_m * self.h ** 2.0 * theta ** (-4.0)

    def k_eq(self):
        r"""
                Scale corresponding to epoch of equality (peak of matter power spectrum) in :math:`h/\mathrm{Mpc}`.

                :return: float.
                """
        z_eq = self.z_eq()
        H_eq = 100.0 * (2.0 * self.Omega_m_z(0.0) * (1.0 + z_eq) ** 3.0) ** 0.5
        return H_eq / const.c / (1.0 + z_eq)

    def TopHat_window(self, x):
        """
                Top-hat window function in Fourier space.

                :param x: Abscissa.
                :type x: array

                :return: array.
                """
        return 3.0 / x ** 3 * (np.sin(x) - x * np.cos(x))

    def comoving_distance(self, z, massive_nu_approx=False):
        r"""
                Comoving distance to a given redshift in :math:`\mathrm{Mpc}/h`.

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        z = np.atleast_1d(z)
        if massive_nu_approx:
            result = np.array([ sint.quad(lambda x: const.c * 1.0 / (self.H_massive(x) / self.h), 0.0, z[i], epsabs=1e-08)[0] for i in range(len(np.atleast_1d(z))) ])
        else:
            result = np.array([ sint.quad(lambda x: const.c * 1.0 / (self.H(x) / self.h), 0.0, z[i], epsabs=1e-08)[0] for i in range(len(np.atleast_1d(z))) ])
        return result

    def f_K(self, z, massive_nu_approx=False):
        r"""
                Geometric factor to a given redshift in :math:`\mathrm{Mpc}/h`. If :math:`\chi(z)` is the comoving distance and :math:`k` is the curvature, then

                .. math::
                        
                        f_K(z) =\left\{\begin{array}{ll}
                                        \chi(z) & \text{for } K=0 \

                                        \frac{1}{\sqrt{K}} \ \sin[\sqrt{K}\chi(z)] & \text{for } K>0

                                        \frac{1}{\sqrt{|K|}} \ \sinh[\sqrt{|K|}\chi(z)] & \text{for } K<0

                                        \end{array}.\right.

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        K = self.K
        if K == 0.0:
            return self.comoving_distance(z, massive_nu_approx)
        else:
            if K > 0.0:
                return 1.0 / K ** 0.5 * np.sin(K ** 0.5 * self.comoving_distance(z, massive_nu_approx))
            return 1.0 / np.abs(K) ** 0.5 * np.sinh(np.abs(K) ** 0.5 * self.comoving_distance(z, massive_nu_approx))

    def delta_f_K(self, z_1, z_2, massive_nu_approx=False):
        r"""
                Difference in geometric factor (distance) between two redshifts in :math:`\mathrm{Mpc}/h`.

                :param z_1: Redshift number 1.
                :type z_1: float

                :param z_2: Redshift number 2.
                :type z_2: float

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        K = self.K
        delta_chi = self.comoving_distance(z_1, massive_nu_approx) - self.comoving_distance(z_2, massive_nu_approx)
        if K == 0.0:
            return delta_chi
        else:
            if K > 0.0:
                return 1.0 / K ** 0.5 * np.sin(K ** 0.5 * delta_chi)
            return 1.0 / np.abs(K) ** 0.5 * np.sinh(np.abs(K) ** 0.5 * delta_chi)

    def luminosity_distance(self, z, massive_nu_approx=False):
        r"""
                Luminosity distance to a given redshift in :math:`\mathrm{Mpc}/h`.

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        com = self.f_K(z, massive_nu_approx)
        return com * (1.0 + z)

    def angular_diameter_distance(self, z, massive_nu_approx=False):
        r"""
                Angular diameter distance to a given redshift in :math:`\mathrm{Mpc}/h`.

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        com = self.f_K(z, massive_nu_approx)
        return com / (1.0 + z)

    def isotropic_volume_distance(self, z, massive_nu_approx=False):
        r"""
                Isotropic volume distance to a given redshift in :math:`\mathrm{Mpc}/h`.

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        return ((1.0 + z) ** 2.0 * self.angular_diameter_distance(z, massive_nu_approx) ** 2.0 * const.c * z * self.h / self.H(z)) ** (1.0 / 3.0)

    def v_rec(self, z, massive_nu_approx=False):
        """
                Recession velocity of galaxies at a given redshift in km/s.

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        return self.H(z) / self.h * self.comoving_distance(z, massive_nu_approx) / (1.0 + z)

    def l_to_k(self, l, z, massive_nu_approx=False):
        """
                Conversion factor from multipoles to scales given the redshift

                :param l: Multipoles
                :type l: array

                :param z: Redshifts.
                :type z: array

                :param massive_nu_approx: Whether to use ``self.H_massive()`` or ``self.H()`` to compute Hubble expansion, i.e. whether to consider massive neutrinos as matter or do the expensive computation.
                :type massive_nu_approx: boolean, default = False

                :return: array.
                """
        inv_dist = 1.0 / self.f_K(z, massive_nu_approx=False)
        scale = np.outer(l, inv_dist)
        return scale

    def R_bg(self, z):
        r"""
                Weigthed ratio :math:`\frac{3 \rho_b}{4 \rho_\gamma}` as a function of redshift

                :param z: Redshifts.
                :type z: array

                :return: array.
                """
        rho_b = self.Omega_b * self.rho_crit(0.0) * (1.0 + z) ** 3.0
        rho_gamma = self.Omega_gamma * self.rho_crit(0.0) * (1.0 + z) ** 4.0
        rho_massless_nu = rho_gamma * 7.0 / 8 * (4.0 / 11.0) ** (4.0 / 3.0) * self.massless_nu
        return 3.0 * rho_b / (4.0 * (rho_gamma + rho_massless_nu))

    def c_s(self, z):
        """
                Speed of sound at a given redshift, in km/s.
                Approximation valid only before recombination, say :math:`z > 1200`.

                :param z: Redshifts.
                :type z: array

                :return: array.
                """
        R = self.R_bg(z)
        return const.c / np.sqrt(3.0 * (1.0 + R))

    def neutrino_thermal_velocity(self, z):
        r"""
                Thermal velocity in km/s of each neutrino species at a given redshift.
                Approximation valid only at :math:`z \ll z_\mathrm{nr}`

                :param z: Redshifts.
                :type z: array

                :return: array.
                """
        vel = np.zeros(self.N_nu)
        for i in xrange(self.N_nu):
            if self.M_nu[i] == 0.0:
                vel[i] = const.c
            else:
                fac = 5.0 / 3.0 * 5.0 * ss.zeta(5.0) / ss.zeta(3.0)
                vel[i] = fac ** 0.5 * (const.kB * self.T_nu / self.M_nu[i]) * (1.0 + z) * const.c

        return vel

    def z_d(self):
        """
                Drag epoch redshift according to Eisenstein & Hu approximation

                :return: float.
                """
        om_m = self.Omega_m - np.sum(self.Omega_nu)
        om_b = self.Omega_b
        h = self.h
        b1 = 0.313 * (om_m * h * h) ** (-0.419) * (1 + 0.607 * (om_m * h * h) ** 0.674)
        b2 = 0.238 * (om_m * h * h) ** 0.223
        z_d = 1291.0 * (1 + b1 * (om_b * h * h) ** b2) * (om_m * h * h) ** 0.251 / (1.0 + 0.659 * (om_m * h * h) ** 0.828)
        return z_d

    def r_s(self):
        """
                Sound horizon at drag epoch

                :return: float.
                """
        if 'classy' not in sys.modules:
            return self.r_s_drag()
        else:
            params = {'A_s': self.As, 
               'n_s': self.ns, 
               'h': self.h, 
               'omega_b': self.Omega_b * self.h ** 2.0, 
               'omega_cdm': self.Omega_cdm * self.h ** 2.0, 
               'Omega_k': self.Omega_K, 
               'N_ur': self.massless_nu, 
               'N_ncdm': self.massive_nu}
            if self.massive_nu != 0:
                params['m_ncdm'] = (', ').join(str(x) for x in self.M_nu[(self.M_nu != 0.0)])
            cosmo = Class()
            cosmo.set(params)
            cosmo.compute()
            rs = cosmo.rs_drag() * cosmo.h()
            cosmo.struct_cleanup()
            cosmo.empty()
            return rs

    def r_s_drag(self):
        rs, _ = sint.quad(lambda x: self.c_s(x) / self.H(x), self.z_d(), np.inf)
        return rs * self.h

    def sigma2(self, z=0.0, k=[], pk=[]):
        r"""
                Mass variance in spheres as a function of mass.

                :param z: Redshift.
                :type z: float, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`.  If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :return: An interpolated function that gives :math:`\sigma^2(\log_{10}(M))`, evaluable between 2 and 18 (therefore between :math:`M = 10^2` and :math:`10^{18} \ M_\odot/h`).
                """
        return self.sigma2_j(z=z, k=k, pk=pk)

    def sigma2_j(self, z=0.0, k=[], pk=[], var='cb', window='th', j=0, smooth=False, R_sm=5.5):
        r"""
                Multipoles of the mass variance as function of mass, namely:

                .. math::

                    \sigma^2_j(M) = \int_0^\infty \frac{dk \ k^2}{2\pi^2} P(k) \ W^2[kR(M)],

                where :math:`W` is a window function, :math:`R` is a radius in :math:`\mathrm{Mpc}/h` and :math:`M` is the mass enclosed in such radius according to the window function.

                :param z: Redshift.
                :type z: float, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :param var: component with respect to which to compute the variance.

                 - 'cb' : cold dark matter + baryons
                 - 'cdm': cold dark matter
                 - 'b'  : baryons
                 - 'nu' : neutrinos
                 - 'tot': total matter
                :type var: string, default = 'cb'

                :param j: Order of multipole.
                :type j: even integer, default = 0

                :param smooth: Further smoothing of the density field with a Gaussian filter (useful for void size function).
                :type smooth: boolean, default = True

                :param R_sm: Size of second filter in :math:`\mathrm{Mpc}/h.`
                :type R_sm: float, default = 5.5

                :param window: Window function used to filter.

                 - `'th'`,`'th'`,`'tophat'`,`'top-hat'` for top-hat filter
                 - `'gauss'`, `'Gaussian'`, `'Gauss'`, `'gaussian'`, `'g'`, for Gaussian

                :type window: string, default = 'th'

                :return: An interpolated function that gives :math:`\sigma^2_j(\log_{10}(M))`, evaluable between 2 and 18 (therefore between :math:`M = 10^2` and :math:`10^{18} \ M_\odot/h`).
                """
        if not len(np.atleast_1d(z)) == 1:
            raise TypeError('Only one redshift per time')
        if k == [] and pk == []:
            k, pk = self.camb_Pk(k=np.logspace(-4.0, 2.7, 201), z=z, var_1=var, var_2=var)
            pk = pk[0]
        assert np.max(k) >= 99.0, 'k_max too low to obtain a convergent result. Minimum 1e2.'
        assert np.min(k) <= 0.001, 'k_min too high to obtain a convergent result. Minimum 1e-3.'
        assert len(k) >= 200, "size of 'k' too low to obtain a convergent result. At least 200 points."
        assert np.all([ np.isclose(np.log(k[(ind + 1)] / k[ind]), np.log(k[(ind + 2)] / k[(ind + 1)]), atol=0.0001, rtol=0.01) for ind in xrange(len(k[:-2]))
                      ]), 'k are not regularly log-spaced'
        kappa, P_kappa = UF.extrapolate_log(k, pk, 1e-06, 100000000.0)
        dlnk = np.log(kappa[1] / kappa[0])
        if var == 'cb':
            omega = self.Omega_cb
        else:
            if var == 'cdm':
                omega = self.Omega_cdm
            elif var == 'b':
                omega = self.Omega_b
            elif var == 'nu':
                omega = self.Omega_nu
            elif var == 'tot':
                omega = self.Omega_m
            else:
                raise NameError("Component unknown, use 'cb', 'cdm', 'b', 'nu', 'tot'")
            rho = self.rho_crit(0.0) * omega
            M = self.M
            R = self.radius_of_mass(M, var=var, window=window)
            k, r = np.meshgrid(kappa, R)
            if window in ('TH', 'th', 'tophat', 'top-hat'):
                W = self.TopHat_window(k * r)
            elif window in ('gauss', 'Gaussian', 'Gauss', 'gaussian', 'g'):
                W = np.exp(-(k * r) ** 2.0 / 2.0)
            else:
                raise NameError('Window not known')
            sm = np.ones_like(R)
            if smooth:
                sm = np.exp(-k ** 2.0 * (r / R_sm) ** 2.0 / 2.0)
            integral = np.zeros_like(R)
            for i in xrange(len(R)):
                integrand = kappa ** (3.0 + 2.0 * j) * P_kappa / (2.0 * const.PI ** 2.0) * W[i] ** 2.0 * sm[i] ** 2.0
                integral[i] = np.trapz(integrand, dx=dlnk)

        if j > 0:
            integral = scipy.signal.savgol_filter(integral, 21, 3)
        sigma_squared = si.interp1d(np.log10(M), integral, 'cubic')
        return sigma_squared

    def mass_in_radius(self, R, var='cb', window='th'):
        r"""
                Mass contained in a sphere of radius R in :math:`M_\odot/h`.

                :param R: Radii in :math:`\mathrm{Mpc}/h`.
                :type R: array

                :param var: component with respect to which to compute the variance.

                 - 'cb' : cold dark matter + baryons
                 - 'cdm': cold dark matter
                 - 'b'  : baryons
                 - 'nu' : neutrinos
                 - 'tot': total matter
                :type var: string, default = 'cb'

                :param window: Window function used to filter.

                 - `'th'`,`'th'`,`'tophat'`,`'top-hat'` for top-hat filter
                 - `'gauss'`, `'Gaussian'`, `'Gauss'`, `'gaussian'`, `'g'`, for Gaussian
                :type window: string, default = 'th'

                :return: array.
                """
        if var == 'cb':
            omega = self.Omega_cb
        else:
            if var == 'cdm':
                omega = self.Omega_cdm
            else:
                if var == 'b':
                    omega = self.Omega_b
                elif var == 'nu':
                    omega = self.Omega_nu
                elif var == 'tot':
                    omega = self.Omega_m
                else:
                    raise NameError("Component unknown, use 'cb', 'cdm', 'b', 'nu', 'tot'")
                rho_bg = self.rho_crit(0.0) * omega
                if window in ('TH', 'th', 'tophat', 'top-hat'):
                    return 4.0 / 3.0 * const.PI * rho_bg * R ** 3.0
            if window in ('gauss', 'Gaussian', 'Gauss', 'gaussian', 'g'):
                return rho_bg * (2.0 * const.PI * R ** 2.0) ** (3.0 / 2.0)
        raise NameError('window not known')

    def radius_of_mass(self, M, var='cb', window='th'):
        r"""
                Radius that contains a certain amount of mass in :math:`\mathrm{Mpc}/h`.

                :param M: Masses in :math:`M_\odot/h`.
                :type M: array

                :param var: component with respect to which to compute the variance.

                 - 'cb' : cold dark matter + baryons
                 - 'cdm': cold dark matter
                 - 'b'  : baryons
                 - 'nu' : neutrinos
                 - 'tot': total matter
                :type var: string, default = 'cb'

                :param window: Window function used to filter.

                 - `'th'`,`'th'`,`'tophat'`,`'top-hat'` for top-hat filter
                 - `'gauss'`, `'Gaussian'`, `'Gauss'`, `'gaussian'`, `'g'`, for Gaussian
                :type window: string, default = 'th'

                :return: array.
                """
        if var == 'cb':
            omega = self.Omega_cb
        else:
            if var == 'cdm':
                omega = self.Omega_cdm
            else:
                if var == 'b':
                    omega = self.Omega_b
                elif var == 'nu':
                    omega = self.Omega_nu
                elif var == 'tot':
                    omega = self.Omega_m
                else:
                    raise NameError("Component unknown, use 'cb', 'cdm', 'b', 'nu', 'tot'")
                rho_bg = self.rho_crit(0.0) * omega
                if window in ('TH', 'th', 'tophat', 'top-hat'):
                    return (3.0 * M / (4.0 * const.PI * rho_bg)) ** (1.0 / 3.0)
            if window in ('gauss', 'Gaussian', 'Gauss', 'gaussian', 'g'):
                return (M / rho_bg) ** (1.0 / 3.0) / (2.0 * const.PI) ** 0.5
        raise NameError('window not known')

    def volume_of_radius(self, R, window='th'):
        r"""
                Volume of a window function of a given radius in :math:`(\mathrm{Mpc}/h)^3`.

                :param R: Radii in :math:`\mathrm{Mpc}/h`.
                :type R: array

                :param var: component with respect to which to compute the variance.

                 - 'cb' : cold dark matter + baryons
                 - 'cdm': cold dark matter
                 - 'b'  : baryons
                 - 'nu' : neutrinos
                 - 'tot': total matter
                :type var: string, default = 'cb'

                :param window: Window function used to filter.

                 - `'th'`,`'th'`,`'tophat'`,`'top-hat'` for top-hat filter
                 - `'gauss'`, `'Gaussian'`, `'Gauss'`, `'gaussian'`, `'g'`, for Gaussian
                :type window: string, default = 'th'

                :return: array.
                """
        if window in ('TH', 'th', 'tophat', 'top-hat'):
            return 4.0 / 3.0 * const.PI * R ** 3.0
        if window in ('gauss', 'Gaussian', 'Gauss', 'gaussian', 'g'):
            return (2.0 * const.PI * R ** 2.0) ** 1.5
        raise NameError("window not known, use 'TH' or 'gauss'")

    def volume_of_mass(self, M, var='cb', window='th'):
        r"""
                Volume of a window function of a given mass in :math:`(\mathrm{Mpc}/h)^3`.

                :param M: Masses in :math:`M_\odot/h`.
                :type M: array

                :param var: component with respect to which to compute the variance.

                 - 'cb' : cold dark matter + baryons
                 - 'cdm': cold dark matter
                 - 'b'  : baryons
                 - 'nu' : neutrinos
                 - 'tot': total matter
                :type var: string, default = 'cb'

                :param window: Window function used to filter.

                 - `'th'`,`'th'`,`'tophat'`,`'top-hat'` for top-hat filter
                 - `'gauss'`, `'Gaussian'`, `'Gauss'`, `'gaussian'`, `'g'`, for Gaussian
                :type window: string, default = 'th'

                :return: array.
                """
        R = self.radius_of_mass(M, var=var, window=window)
        return self.volume_of_radius(R, window=window)

    def lagrange_to_euler(self, z=0.0, delta_v=None, delta_c=None):
        r"""
                Mapping between Eulerian and Lagrangian radii in :math:`\mathrm{Mpc}/h`.

                :param z: Redshift
                :type z: float

                :param delta_v: Critical underdensity in linear theory.
                :type delta_v: float

                :param delta_c: Critical overdensity in linear theory.
                :type delta_c: float

                :return: array.
                """
        if delta_v == None:
            delta_v = self.delta_v
        if delta_c == None:
            delta_c = self.delta_sc
        return (1 - self.D_1(z) * delta_v / delta_c) ** (delta_c / 3.0)

    def peak_height(self, z=0.0, k=[], pk=[]):
        r"""
                Peak height as a function of log10(M).

                :param z: Redshift.
                :type z: float, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :return: An interpolated function that gives :math:`\sigma^2_j(\log_{10}(M))`, evaluable between 2 and 18 (therefore between :math:`M = 10^2` and :math:`10^{18} \ M_\odot/h`).

                """
        if not np.size(z) == 1:
            raise TypeError('Only one redshift per time')
        if k == [] and pk == []:
            k, pk = self.camb_Pk(k=np.logspace(-4.0, 2.7, 201), z=z, var_1='cb', var_2='cb')
            pk = pk[0]
        sigma = self.sigma2(z, k, pk)
        M = self.M
        nu = si.interp1d(np.log10(M), self.delta_sc / sigma(np.log10(M)) ** 0.5, 'cubic')
        return nu

    def ShethTormen_mass_function(self, sigma, a=0.707, p=0.3, delta_th=None):
        r"""
                Universal mass function by Sheth-Tormen as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param a: Sheth-Tormen mass function parameter.
                :type a: float, default = 0.707

                :param p: Sheth-Tormen mass function parameter.
                :type p: float<0.5, default = 0.3

                :param delta_th': Threshold for collapse.
                :type delta_th': float, default = None

                :return: array
                """
        if delta_th == None:
            delta_th = self.delta_sc
        nu = np.abs(delta_th) / sigma
        n = nu ** 2.0
        A = 1.0 / (1.0 + 2.0 ** (-p) * ss.gamma(0.5 - p) / np.sqrt(const.PI))
        ST = A * np.sqrt(2.0 * a * n / const.PI) * (1.0 + 1.0 / (a * n) ** p) * np.exp(-a * n / 2.0)
        return ST

    def PressSchechter_mass_function(self, sigma, delta_th=None):
        r"""
                Universal mass function by Press-Schechter as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param delta_th: Threshold for collapse.
                :type delta_th: float, default = None

                :return: array
                """
        return self.ShethTormen_mass_function(sigma, a=1.0, p=0.0, delta_th=delta_th)

    def Tinker_mass_function(self, sigma, z=0.0, Delta=200.0):
        r"""
                Universal mass function by Tinker as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param Delta: Overdensity of collapsed objects.
                :type Delta: 200<=float<=3200, default = 200

                :return: array
                """
        alpha = 10.0 ** (-(0.75 / np.log10(Delta / 75.0)) ** 1.2)
        logDelta = np.log10(Delta)
        delta_array = [
         200.0, 300.0, 400.0, 600.0, 800.0, 1200.0, 1600.0, 2400.0, 3200.0]
        A_array = [0.1858659, 0.1995973, 0.2115659, 0.2184113,
         0.2480968, 0.2546053, 0.26, 0.26, 0.26]
        a_array = [1.466904, 1.521782, 1.559186, 1.614585,
         1.869936, 2.128056, 2.301275, 2.529241, 2.661983]
        b_array = [2.571104, 2.254217, 2.048674, 1.869559,
         1.588649, 1.507134, 1.464374, 1.436827, 1.40521]
        c_array = [1.193958, 1.270316, 1.335191, 1.446266,
         1.581345, 1.79505, 1.965613, 2.237466, 2.439729]
        A_d = si.interp1d(delta_array, A_array, 'cubic')
        a_d = si.interp1d(delta_array, a_array, 'cubic')
        b_d = si.interp1d(delta_array, b_array, 'cubic')
        c_d = si.interp1d(delta_array, c_array, 'cubic')
        A = A_d(Delta) * (1.0 + z) ** (-0.14)
        a = a_d(Delta) * (1.0 + z) ** (-0.06)
        b = b_d(Delta) * (1.0 + z) ** (-alpha)
        c = c_d(Delta)
        return A * ((sigma / b) ** (-a) + 1.0) * np.exp(-c / sigma ** 2.0)

    def MICE_mass_function(self, sigma, z=0.0):
        r"""
                Universal mass function by Crocce et al. (2010) as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param z: Redshift.
                :type z: float, default = 0

                :return: array
                """
        A = 0.58 * (1.0 + z) ** (-0.13)
        a = 1.37 * (1.0 + z) ** (-0.15)
        b = 0.3 * (1.0 + z) ** (-0.084)
        c = 1.036 * (1.0 + z) ** (-0.024)
        return A * (sigma ** (-a) + b) * np.exp(-c / sigma ** 2.0)

    def ShethTormen_bias(self, sigma, a=0.707, p=0.3, delta_th=None):
        r"""
                Eulerian bias for the Sheth-Tormen mass function as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param a: Sheth-Tormen mass function parameter.
                :type a': float, default = 0.707

                :param p: Sheth-Tormen mass function parameter.
                :type p: float<0.5, default = 0.3

                :param delta_th: Threshold for collapse.
                :type delta_th: float, default = None

                :return: array
                """
        if delta_th == None:
            delta_th = self.delta_sc
        nu = np.abs(delta_th) / sigma
        b = 1.0 + (a * nu ** 2.0 - 1.0) / self.delta_sc + 2.0 * p / self.delta_sc / (1.0 + (a * nu ** 2.0) ** p)
        return b

    def PressSchechter_bias(self, sigma):
        r"""
                Eulerian bias for the Press-Schechter mass function as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param delta_th: Threshold for collapse.
                :type delta_th: float, default = None

                :return: array
                """
        return self.ShethTormen_bias(sigma, a=1.0, p=0.0)

    def Tinker_bias(self, sigma, z=0.0, Delta=200.0):
        r"""
                Eulerian bias for the Tinker mass function as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param Delta: Overdensity of collapsed objects.
                :type Delta: 200<=float<=3200, default = 200

                :return: array
                """
        y = np.log10(Delta)
        A = 1.0 + 0.24 * y * np.exp(-(4.0 / y) ** 4.0)
        a = 0.44 * y - 0.88
        C = 0.019 + 0.107 * y + 0.19 * np.exp(-(4.0 / y) ** 4.0)
        B, b, c = (0.183, 1.5, 2.4)
        nu = self.delta_sc / sigma
        return 1.0 - A * nu ** a / (nu ** a + self.delta_sc ** a) + B * nu ** b + C * nu ** c

    def halo_bias(self, sigma, mass_fun='ST', **kwargs):
        r"""
                Eulerian bias for the a given halo mass function as function of the RMS mass fluctuation in spheres :math:`\sigma(M)`.

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param mass_fun: Kind of halo mass function.

                 - 'Sheth-Tormen','ST','ShethTormen' for Sheth-Tormen
                 - 'Press-Schechter', 'PS', 'PressSchechter' for Press-Schechter
                 - 'Tinker', 'T', 'T08' for Tinker et al. (2008)

                :type mass_fun: string, default = `'ST'`

                :param kwargs: Keyword arguments to pass to `'mass_fun'`.

                :return: array
                """
        if mass_fun in ('Sheth-Tormen', 'ST', 'ShethTormen'):
            return self.ShethTormen_bias(sigma=sigma, **kwargs)
        if mass_fun in ('Press-Schechter', 'PS', 'PressSchechter'):
            return self.PressSchechter_bias(sigma=sigma)
        if mass_fun in ('Tinker', 'T', 'T08'):
            return self.Tinker_bias(sigma=sigma, **kwargs)
        raise NameError("Unknown mass function, use 'Sheth-Tormen','ST','ShethTormen' / 'Press-Schechter', 'PS', 'PressSchechter' / 'Tinker', 'T', 'T08'")

    def effective_bias(self, z=0.0, M_min=10000000000.0, M_max=1e+17, k=[], pk=[], mass_fun='ST', **kwargs):
        r"""
                It computes the effective halo bias as

                .. math::

                    b_\mathrm{eff} = \frac{\int_{M_{min}}^{M_{max}} dM \ b(M) \ \frac{dn}{dM}}{\int_{M_{min}}^{M_{max}} dM \ \frac{dn}{dM}}

                where :math:`b(M)` is the linear halo bias given the kind of mass function.

                :param z: Redshift.
                :type z: float, default = 0

                :param M_min: Minimum halo mass in :math:`M_\odot/h`.
                :type M_min: float>1e2, default = 1e10

                :param M_min: Maximum halo mass in :math:`M_\odot/h`.
                :type M_max: float<1e18, default = 1e17

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :param mass_fun: Kind of halo mass function.

                 - 'Sheth-Tormen','ST','ShethTormen' for Sheth-Tormen
                 - 'Press-Schechter', 'PS', 'PressSchechter' for Press-Schechter
                 - 'Tinker', 'T', 'T08' for Tinker et al. (2008)

                :type mass_fun: string, default = `'ST'`

                :param kwargs: Keyword arguments to pass to `'mass_fun'`.

                :return: float
                """
        if not np.size(z) == 1:
            raise TypeError('Only one redshift per time')
        if k == [] and pk == []:
            k, pk = self.camb_Pk(k=np.logspace(-4.0, 2.7, 201), z=z, var_1='cb', var_2='cb')
            pk = pk[0]
        logM = np.log10(self.M)
        conv = np.log(10.0)
        HMF = self.halo_mass_function(z=z, k=k, pk=pk, mass_fun=mass_fun, **kwargs)
        sigma2 = self.sigma2(z=z, k=k, pk=pk)
        bias = self.halo_bias((sigma2(logM) ** 0.5), mass_fun=mass_fun, **kwargs)
        BIAS = si.interp1d(logM, bias, kind='cubic')
        numerator, _ = sint.quad(lambda m: HMF(m) * BIAS(m) * conv * 10.0 ** m, np.log10(M_min), np.log10(M_max))
        denominator, _ = sint.quad(lambda m: HMF(m) * conv * 10.0 ** m, np.log10(M_min), np.log10(M_max))
        return numerator / denominator

    def halo_mass_function(self, z=0.0, k=[], pk=[], mass_fun='Sheth-Tormen', **kwargs):
        r"""
                Halo mass function, i.e. number of halos per unit volume per unit mass.

                :param z: Redshift.
                :type z: float, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :param mass_fun: Kind of halo mass function.

                 - 'Sheth-Tormen','ST','ShethTormen' for Sheth-Tormen
                 - 'Press-Schechter', 'PS', 'PressSchechter' for Press-Schechter
                 - 'Tinker', 'T', 'T08' for Tinker et al. (2008)

                :type mass_fun: string, default = `'ST'`

                :param kwargs: Keyword arguments to pass to `'mass_fun'`.

                :return: An interpolated function that gives :math:`\frac{dn}{dM}(\log_{10}(M))` in :math:`h^4 \ \mathrm{Mpc}^{-3} \ M_\odot^{-1}`, evaluable between 2 and 18 (therefore between :math:`M = 10^2` and :math:`10^{18} \ M_\odot/h`).
                """
        if not np.size(z) == 1:
            raise TypeError('Only one redshift per time')
        if k == [] and pk == []:
            k, pk = self.camb_Pk(k=np.logspace(-4.0, 2.7, 201), z=z, var_1='cb', var_2='cb')
            pk = pk[0]
        rho = self.rho_crit(0.0) * self.Omega_cb
        M = self.M[1:-1]
        s2 = self.sigma2(z, k, pk)
        log_der = sm.derivative(s2, np.log10(M), dx=0.01, n=1, order=3)
        log_der *= -1.0 / 2.0 / s2(np.log10(M)) * np.log10(np.exp(1.0))
        s = s2(np.log10(M)) ** 0.5
        if mass_fun in ('Sheth-Tormen', 'ST', 'ShethTormen'):
            f_nu = self.ShethTormen_mass_function(sigma=s, **kwargs)
        elif mass_fun in ('Tinker', 'T', 'T08'):
            f_nu = self.Tinker_mass_function(sigma=s, z=z, **kwargs)
        elif mass_fun in ('MICE', 'Crocce', 'C'):
            f_nu = self.MICE_mass_function(sigma=s, z=z)
        elif mass_fun in ('Press-Schechter', 'PS', 'PressSchechter'):
            f_nu = self.PressSchechter_mass_function(sigma=s)
        else:
            raise NameError("Unknown mass function, use 'Sheth-Tormen','ST','ShethTormen' / 'MICE', 'Crocce', 'C' / 'Press-Schechter', 'PS', 'PressSchechter' / 'Tinker', 'T', 'T08'")
        hmf = rho / M ** 2.0 * log_der * f_nu
        hmf = si.interp1d(np.log10(M), hmf, 'cubic')
        return hmf

    def f_nu_voids(self, sigma, delta_c=None, delta_v=None, truncation=30):
        """
                Function to compute the void size function

                :param sigma: RMS mass fluctuation.
                :type sigma: array

                :param delta_v: Critical underdensity in linear theory. If None, it is substituted by self.delta_sc.
                :type delta_v: float, default = None

                :param delta_c: Void in cloud parameter. If None, it is substituted by self.delta_v.
                :type delta_c: float, default = None

                :param truncation: Order at which truncate the sum.
                :type truncation: integer>11, default = 30

                :return: array.
                """
        assert truncation > 11, "Sum will not converge, choose value for 'truncation' >= 12"
        if delta_c == None:
            delta_c = self.delta_sc
        if delta_v == None:
            delta_v = self.delta_v
        dv = np.abs(delta_v)
        D = dv / (delta_c + dv)
        x = D / dv * sigma
        ns = len(sigma)
        vdn = np.zeros(ns)
        for i_s in xrange(ns):
            vdn[i_s] = 2.0 * np.sum([ np.exp(-(j * const.PI * x[i_s]) ** 2.0 / 2.0) * j * const.PI * x[i_s] ** 2.0 * np.sin(j * const.PI * D) for j in xrange(1, truncation) ])

        return vdn

    def void_size_function(self, z=0.0, ratio=1.72, k=[], pk=[], model='Vdn', var='cb', **kwargs):
        r"""
                Computes the void size function per logarithmic interval of radius. Units of :math:`(h/\mathrm{Mpc})^3`.

                :param z: Redshift.
                :type z: float, default = 0

                :param ratio: Ratio between radii of voids in linear and non-linear theory.
                :type ratio: float, default = 1.72

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :param model: Model to use for void size function.

                 - 'Vdn', 'volume conserving', 'VolumeConserving' for Volume conserving
                 - 'SvdW', 'Sheth-van de Weygaert', 'ShethVanDeWeygaert' for Sheth-Van De Weygaert
                 - 'linear', 'lin', 'L' for linear model

                :type model: string, default = `'VdN'`

                :param var: Component to use to compute the variance.

                 - 'cb' : cold dark matter + baryons
                 - 'tot': total matter
                :type var: string, default = 'cb'

                :param kwargs: Arguments to pass to ``self.f_nu_voids``

                :return: An interpolated function that gives :math:`\frac{dn}{d\ln R}(R)` in :math:`h^3 \ \mathrm{Mpc}^{-3}`.
                """
        if not np.size(z) == 1:
            raise TypeError('Only one redshift per time')
        if k == [] and pk == []:
            k, pk = self.camb_Pk(k=np.logspace(-4.0, 2.7, 201), z=z, var_1=var, var_2=var)
            pk = pk[0]
        if model in ('Vdn', 'volume conserving', 'VolumeConserving'):
            rat = ratio
            shift = 1.0
        elif model in ('SvdW', 'Sheth-van de Weygaert', 'ShethVanDeWeygaert'):
            rat = ratio
            shift = ratio ** 3.0
        elif model in ('linear', 'lin', 'L'):
            rat = 1.0
            shift = 1.0
        else:
            raise NameError("Void size function model unknown, use 'Vdn', 'volume conserving', 'VolumeConserving' / 'SvdW', 'Sheth-van de Weygaert', 'ShethVanDeWeygaert' / 'linear', 'lin', 'L'")
        M = self.M[1:-1]
        s2 = self.sigma2(z, k, pk)
        sigma = s2(np.log10(M)) ** 0.5
        log_der = sm.derivative(s2, np.log10(M), dx=0.01, n=1, order=3) * -3.0 / (2.0 * sigma ** 2.0) * np.log10(np.exp(1.0))
        if var == 'cb':
            omega = self.Omega_cb
        elif var == 'tot':
            omega = self.Omega_m
        else:
            raise NameError("'var' unknown, choose between 'cb' and 'tot'")
        rho_v = rat ** (-3.0) * self.rho_crit(0.0) * omega
        R = self.radius_of_mass(M)
        V = lambda r: self.volume_of_radius(R)
        dndr = shift * self.f_nu_voids(sigma, **kwargs) / V(R) * log_der
        vsf = si.interp1d(R, dndr)
        return vsf

    def F_BBKS(self, x):
        """
                Function related to peak number density. 'x' is a quantity related to the derivative
                of the density field with respect to the RMS mass fluctuation.

                :param x: Abscissa.
                :type x: array

                :return: array.
                """
        num1 = (x ** 3.0 - 3.0 * x) / 2.0 * (ss.erf(x * np.sqrt(5.0 / 2.0)) + ss.erf(x * np.sqrt(5.0 / 8.0)))
        num2 = np.sqrt(2.0 / (5.0 * const.PI)) * (31.0 * x ** 2.0 / 4.0 + 8.0 / 5.0) * np.exp(-5.0 * x ** 2.0 / 8.0)
        num3 = np.sqrt(2.0 / (5.0 * const.PI)) * (x ** 2.0 / 2.0 - 8.0 / 5.0) * np.exp(-5.0 * x ** 2.0 / 2.0)
        return num1 + num2 + num3

    def Gauss(self, x, mean, var):
        """
                Normalized Gaussian function.

                :param x: Abscissa.
                :type x: array

                :param mean: Mean of the Gaussian.
                :type mean: float

                :param var: Variance of the Gaussian, i.e. the square of the standard deviation.
                :type var: float

                :return: array.
                """
        return np.exp(-(x - mean) ** 2.0 / (2.0 * var)) / np.sqrt(2.0 * const.PI * var)

    def G_n_BBKS(self, n, gamma_p, nu):
        """
                Functions related to peaks number density and mass function, as described in Bardeen et al. (1986).

                :param n: Order of integral.
                :type n: integer
                    

                :param gamma_p: Index in excursion set.
                :type gamma_p: float

                :param nu: Peak height.
                :type nu: array

                :return: array
                """
        var = 1.0 - np.array(gamma_p) ** 2.0
        mean = np.array(gamma_p) * np.array(nu)
        G = np.array(list(map(lambda m, v: sint.quad(lambda x: x ** n * self.F_BBKS(x) * self.Gauss(x, m, v), 0.0, np.inf)[0], mean, var)))
        return G

    def dndR_EST(self, R, z, k, pk, delta_v, a=1.0, p=0.0):
        r"""
                This routine returns the void size function, i.e. the number of voids per
                unit volume per unit radius, according ot the Excursion Set of Troughs theory.
                Units of :math:`(h/\mathrm{Mpc})^3`.

                :param R: Lagrangian radii in :math:`\mathrm{Mpc}/h`.
                :type R: array

                :param z: Redshift.
                :type z: float

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array

                :param delta_v: Critical underdensity in linear theory. If None, it is substituted by self.delta_sc.
                :type delta_v: float

                :param a: Sheth-Tormen-like parameter
                :type a: float

                :param p: Sheth-Tormen-like parameter
                :type p: float

                Returns
                ----------

                NumPy array
                """
        R = R / self.lagrange_to_euler(z=z, delta_v=delta_v)
        s0 = self.sigma2_j(k=k, pk=pk, j=0, smooth=True, window='th')
        s1 = self.sigma2_j(k=k, pk=pk, j=1, smooth=True, window='th')
        s2 = self.sigma2_j(k=k, pk=pk, j=2, smooth=True, window='th')
        dv = np.abs(delta_v)
        rho_bg = self.Omega_cb * self.rho_crit(0.0)
        M = self.mass_in_radius(R, window='th')
        gamma_p = s1(np.log10(M)) / np.sqrt(s0(np.log10(M)) * s2(np.log10(M)))
        R_star = np.sqrt(3.0 * s1(np.log10(M)) / s2(np.log10(M)))
        nu = dv / s0(np.log10(M)) ** 0.5
        G1 = self.G_n_BBKS(1, gamma_p, nu)
        f_ST = self.ShethTormen_mass_function(s0(np.log10(M)) ** 0.5, delta_th=dv, a=a, p=p) / (2.0 * nu)
        f_nu = self.volume_of_radius(R, 'th') / (2.0 * const.PI * R_star ** 2.0) ** (3.0 / 2.0) * f_ST * G1 / (gamma_p * nu)
        log_der = sm.derivative(s0, np.log10(M), dx=0.01, n=1, order=3)
        loge = np.log10(np.exp(1.0))
        dnu_dr = -3.0 / 2.0 * nu / R * loge / s0(np.log10(M)) * log_der
        V = self.volume_of_radius(R, 'th')
        dndR = f_nu / V * dnu_dr
        return dndR

    def y_fs(self, k):
        r"""
                Quantity related to free-streaming scale.

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :return: array
                """
        theta = self.T_cmb / 2.7
        chi = k * theta ** 2.0 / self.Omega_m
        f_nu = np.sum(np.atleast_1d(self.f_nu))
        f_cb = self.f_cb
        y_fs = 17.2 * f_nu * (1.0 + 0.488 * f_nu ** (-7.0 / 6.0)) * (self.massive_nu * chi / f_nu) ** 2.0
        return y_fs

    def k_FS(self, z):
        r"""
                Free-streaming scale in :math:`h/\mathrm{Mpc}`.

                :param z: Redshifts.
                :type z: array

                :return: array
                """
        E = self.H_massive(z) / self.H0
        return 0.82 * np.sum(np.atleast_1d(self.M_nu)) * E / (1.0 + z) ** 2.0

    def D_1(self, z):
        """
                Matter growth factor for a LCDM cosmology (i.e. scale-independent) at a
                given redshift, normalized to 1 today.

                :param z: Redshifts.
                :type z: array

                :return: array
                """
        nz = len(np.atleast_1d(z))
        d1 = np.zeros(nz)
        if nz == 1:
            z = [
             z]
        for i in xrange(nz):
            LCDM, _ = sint.quad(lambda x: (1 + x) * (self.H0 / self.H_massive(x)) ** 3.0, z[i], np.inf)
            d1[i] = LCDM * self.H_massive(z[i]) / self.H0

        LCDM0, _ = sint.quad(lambda x: (1 + x) * (self.H0 / self.H_massive(x)) ** 3.0, 0.0, np.inf)
        d1 *= 1.0 / LCDM0
        return d1

    def growth_cb(self, k, z):
        """
                Non normalized scale-dependent growth factor for cdm+baryons.
                See :func:`~colibri.cosmology.cosmo.D_cb()` for further information
                """
        LCDM = self.D_1(z)
        if np.sum(np.atleast_1d(self.M_nu)) == 0.0:
            LCDM = np.array([ LCDM for i in xrange(len(np.atleast_1d(k))) ])
            return np.transpose(LCDM)
        else:
            K, Z = np.meshgrid(k, z)
            f_cb = self.f_cb
            f_nu = np.sum(np.atleast_1d(self.f_nu))
            LCDM = np.transpose([ LCDM for i in xrange(len(np.atleast_1d(k))) ]) / self.D_1(self.z_d())
            p_cb = 1.0 / 4.0 * (5.0 - np.sqrt(1.0 + 24.0 * f_cb))
            growth_cb = (1.0 + (LCDM / (1.0 + self.y_fs(K))) ** 0.7) ** (p_cb / 0.7) * LCDM ** (1.0 - p_cb)
            return growth_cb

    def D_cb(self, k, z):
        r"""
                Cold dark matter + baryon scale-dependent growth factor at a given redshift,
                normalized to 1 today.

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :param z: Redshifts.
                :type z: array

                :return: 2D array of shape ``(len(z), len(k))``
                """
        return self.growth_cb(k, z) / self.growth_cb(k, 0.0)

    def growth_cbnu(self, k, z):
        """
                Unnormalized scale-dependent growth factor for matter.
                See :func:`~colibri.cosmology.cosmo.D_cb()` for further information
                """
        LCDM = self.D_1(z)
        if np.sum(self.M_nu) == 0.0:
            LCDM = np.array([ LCDM for i in xrange(len(np.atleast_1d(k))) ])
            return np.transpose(LCDM)
        else:
            K, Z = np.meshgrid(k, z)
            f_cb = self.f_cb
            f_nu = np.sum(np.atleast_1d(self.f_nu))
            LCDM = np.transpose([ LCDM for i in xrange(len(np.atleast_1d(k))) ]) / self.D_1(self.z_d())
            p_cb = 1.0 / 4.0 * (5.0 - np.sqrt(1.0 + 24.0 * f_cb))
            growth_cbnu = (f_cb ** (0.7 / p_cb) + (LCDM / (1.0 + self.y_fs(K))) ** 0.7) ** (p_cb / 0.7) * LCDM ** (1.0 - p_cb)
            return growth_cbnu

    def D_cbnu(self, k, z):
        r"""
                Total matter (i.e. cold dark matter + baryon + neutrino) scale-dependent growth factor
                at a given redshift, normalized to 1 today.

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :param z: Redshifts.
                :type z: array

                :return: 2D array of shape ``(len(z), len(k))``
                """
        return self.growth_cbnu(k, z) / self.growth_cbnu(k, 0.0)

    def M_p(self, L, N, kind='cb'):
        r"""
                Mass of a single particle (in :math:`M_\odot/h`) in a simulation box, given the length L of the box
                itself (in :math:`\mathrm{Mpc}/h`) and the number of particles N per side.

                :param L: Boxsize in :math:`\mathrm{Mpc}/h`.
                :type L: array

                :param N: Number of particles per side.
                :type N: array

                :param kind:

                 - 'cb' : cold dark matter + baryons
                 - 'cdm': cold dark matter
                 - 'b'  : baryons
                 - 'nu' : neutrinos
                 - 'tot': total matter
                :type kind: string, default = `'cb'`

                :return: 2D array of shape ``(len(N), len(L))``
                """
        L = np.array(L)
        N = np.array(N)
        L_over_N = np.outer(L, 1.0 / N)
        if kind == 'cdm':
            omega = self.Omega_cdm
        elif kind == 'cb':
            omega = self.Omega_cb
        elif kind == 'nu':
            omega = self.Omega_nu
        elif kind == 'b':
            omega = self.Omega_b
        else:
            raise NameError("unknown kind of particle, use 'cb', 'cdm', 'b', 'nu'")
        return L_over_N ** 3.0 * omega * self.rho_crit(0.0)

    def feedback_suppression(self, k, z, log_Mc, eta_b, z_c):
        r"""
                Suppression of the matter power spectrum according to the Baryon Correction Model
                (Schneider et al., 2015).

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

    def WDM_suppression(self, k, z, M_wdm, nonlinear=False):
        r"""
                Suppression of the matter power spectrum due to (thermal) warm dark matter. In the linear
                case, the formula by https://arxiv.org/pdf/astro-ph/0501562.pdf is followed;
                otherwise the formula by https://arxiv.org/pdf/1107.4094.pdf is used.
                The linear formula is an approximation strictly valid only at :math:`k < 5-10 \ h/\mathrm{Mpc}`.
                The nonlinear formula has an accuracy of 2% level at :math:`z < 3` and for masses larger than 0.5 keV.

                .. warning::

                 This function returns the total suppression in power. To obtain the suppression in the transfer function, take the square root of the output.

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array

                :param z: Redshifts.
                :type z: array

                :param M_wdm: Mass of the warm dark matter particle in keV.
                :type M_wdm: float

                :param nonlinear: Whether to return non-linear transfer function.
                :type nonlinear: boolean, default = False

                :return: 2D array of shape ``(len(z), len(k))``
                """
        K, Z = np.meshgrid(k, z)
        if not nonlinear:
            alpha_linear = 0.049 * M_wdm ** (-1.11) * (self.Omega_cdm / 0.25) ** 0.11 * (self.h / 0.7) ** 1.22
            nu = 1.12
            return (1.0 + (alpha_linear * K) ** (2.0 * nu)) ** (-10.0 / nu)
        else:
            nu, l, s = (3.0, 0.6, 0.4)
            alpha = 0.0476 * (1.0 / M_wdm) ** 1.85 * ((1.0 + Z) / 2.0) ** 1.3
            return (1.0 + (alpha * K) ** (nu * l)) ** (-s / nu)

    def camb_Pk(self, z=0.0, k=np.logspace(-4.0, 2.0, 1001), nonlinear=False, halofit='mead', var_1='tot', var_2='tot', **kwargs):
        r"""
                This routine uses the CAMB Boltzmann solver to return power spectra for the chosen cosmology.
                Depending on the value of 'nonlinear', the power spectrum is linear or non-linear; the 'halofit'
                argument chooses the non-linear model.

                :param z: Redshifts.
                :type z: array, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = ``np.logspace(-4., 2., 1001)``

                :param nonlinear: Whether to return non-linear power spectra.
                :type nonlinear: boolean, default = False

                :type halofit: string, default = 'mead'
                :param halofit: Which version of Halofit to use. Choose among 'mead', 'original', 'bird', 'peacock',
                    'takahashi', 'halomodel', 'casarini', 'mead2015'. See CAMB documentation for further info.

                :param var_1: Density field for the first component of the power spectrum.
                :type var_1: string, default = 'tot'

                :param var_2: Density field for the second component of the power spectrum.

                 - `'tot'`   : total matter 
                 - `'cdm'`   : cold dark matter
                 - `'b'`     : baryons
                 - `'nu'`    : neutrinos
                 - `'cb'`    : cold dark matter + baryons
                 - `'rad'`   : radiation
                 - `'v_cdm'` : cdm velocity
                 - `'v_b'`   : baryon velocity
                 - `'Phi'`   : Weyl potential
                :type var_2: string, default = `'tot'`

                :param kwargs: Keyword arguments to be passed to ``camb.model.CAMBparams.InitPower.set_params``, ``camb.model.CAMBparams.InitPower.set_dark_energy`` and ``camb.model.CAMBparams.set_cosmology``. See CAMB documentation for further info: https://camb.readthedocs.io/en/latest/

                Returns
                -------

                k: array
                    Scales in :math:`h/\mathrm{Mpc}`. Basically the same 'k' of the input.

                pk: 2D array of shape ``(len(z), len(k))``
                    Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`.
                """
        params = camb.model.CAMBparams()
        local_extra_parameter_values = locals()['kwargs']
        all_params_initial = params.InitPower.set_params.__code__.co_varnames[1:]
        all_params_cosmology = params.set_cosmology.__code__.co_varnames[1:]
        all_params_dark_energy = params.set_dark_energy.__code__.co_varnames[1:]
        kwargs_initial, kwargs_cosmology, kwargs_dark_energy = {}, {}, {}
        for i in local_extra_parameter_values:
            if i in all_params_initial:
                kwargs_initial[i] = local_extra_parameter_values[i]
            elif i in all_params_cosmology:
                kwargs_cosmology[i] = local_extra_parameter_values[i]
            elif i in all_params_dark_energy:
                kwargs_dark_energy[i] = local_extra_parameter_values[i]
            else:
                print 'warning: %s parameter not being used' % i

        params.InitPower.set_params(ns=self.ns, As=self.As, **kwargs_initial)
        params.set_cosmology(H0=(100.0 * self.h), ombh2=(self.Omega_b * self.h ** 2.0), omch2=(self.Omega_cdm * self.h ** 2.0), mnu=np.sum(self.M_nu), nnu=self.N_eff, num_massive_neutrinos=self.massive_nu, standard_neutrino_neff=3.046, omk=self.Omega_K, tau=self.tau, TCMB=self.T_cmb, **kwargs_cosmology)
        params.set_dark_energy(w=self.w0, wa=self.wa, **kwargs_dark_energy)
        z = np.atleast_1d(z)
        nz = len(z)
        components = {'tot': 'delta_tot', 'cdm': 'delta_cdm', 
           'b': 'delta_baryon', 
           'nu': 'delta_nu', 
           'cb': 'delta_nonu', 
           'rad': 'delta_photon', 
           'v_cdm': 'v_newtonian_cdm', 
           'v_b': 'v_newtonian_baryon', 
           'Phi': 'Weyl'}
        npoints = 1001
        if nonlinear == True:
            camb.nonlinear.Halofit(halofit_version=halofit)
            params.NonLinear = camb.model.NonLinear_both
        params.set_matter_power(redshifts=z, kmax=k.max() * 2.5, silent=True)
        results = camb.get_results(params)
        kh, z, pkh = results.get_matter_power_spectrum(minkh=k.min() / 2.0, maxkh=k.max() * 2.5, npoints=npoints, var1=components[var_1], var2=components[var_2])
        power = si.interp1d(kh, pkh, kind='cubic')
        pk = power(k)
        return (
         k, pk)

    def camb_XPk(self, z=0.0, k=np.logspace(-4.0, 2.0, 1001), nonlinear=False, halofit='mead', var_1=[
 'tot'], var_2=[
 'tot'], **kwargs):
        r"""
                The function CAMB_XPk() runs the Python wrapper of CAMB and returns auto- and 
                cross-spectra for all the quantities specified in 'var_1' and 'var_2'.
                Depending on the value of 'nonlinear', the power spectrum is linear or non-linear.
                It returns scales in units of :math:`h/\mathrm{Mpc}` and power spectra in units of (:math:`(\mathrm{Mpc}/h)^3`.

                :param z: Redshifts.
                :type z: array, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = ``np.logspace(-4., 2., 1001)``

                :param nonlinear: Whether to return non-linear power spectra.
                :type nonlinear: boolean, default = False

                :type halofit: string, default = 'mead'
                :param halofit: Which version of Halofit to use. Choose among 'mead', 'original', 'bird', 'peacock',
                    'takahashi', 'halomodel', 'casarini', 'mead2015'. See CAMB documentation for further info.

                :param var_1: Density field for the first component of the power spectrum.
                :type var_1: list of strings, default = ['tot']

                :param var_2: Density field for the second component of the power spectrum.

                 - `'tot'`   : total matter 
                 - `'cdm'`   : cold dark matter
                 - `'b'`     : baryons
                 - `'nu'`    : neutrinos
                 - `'cb'`    : cold dark matter + baryons
                 - `'rad'`   : radiation
                 - `'v_cdm'` : cdm velocity
                 - `'v_b'`   : baryon velocity
                 - `'Phi'`   : Weyl potential
                :type var_2: list of strings, default = ['tot']

                :param kwargs: Keyword arguments to be passed to ``camb.model.CAMBparams.InitPower.set_params``, ``camb.model.CAMBparams.InitPower.set_dark_energy`` and ``camb.model.CAMBparams.set_cosmology``. See CAMB documentation for further info: https://camb.readthedocs.io/en/latest/

                Returns
                -------

                k: array
                    Scales in :math:`h/\mathrm{Mpc}`. Basically the same 'k' of the input.

                pk: dictionary
                    Keys are given by `'var_1-var_2'`. Each of these is a 2D array of shape ``(len(z), len(k))`` containing :math:`P_\mathrm{var_1-var_2}(z,k)` in units of :math:`(\mathrm{Mpc}/h)^3`.

                """
        params = camb.model.CAMBparams()
        local_extra_parameter_names = locals()['kwargs']
        all_params_initial = params.InitPower.set_params.__code__.co_varnames[1:]
        all_params_cosmology = params.set_cosmology.__code__.co_varnames[1:]
        all_params_dark_energy = params.set_dark_energy.__code__.co_varnames[1:]
        kwargs_initial, kwargs_cosmology, kwargs_dark_energy = {}, {}, {}
        for i in local_extra_parameter_names:
            if i in all_params_initial:
                kwargs_initial[i] = local_extra_parameter_names[i]
            elif i in all_params_cosmology:
                kwargs_cosmology[i] = local_extra_parameter_names[i]
            elif i in all_params_dark_energy:
                kwargs_dark_energy[i] = local_extra_parameter_names[i]
            else:
                print 'warning: %s parameter not being used' % local_extra_parameter_names[i]

        params.InitPower.set_params(ns=self.ns, As=self.As, **kwargs_initial)
        params.set_cosmology(H0=(100.0 * self.h), ombh2=(self.Omega_b * self.h ** 2.0), omch2=(self.Omega_cdm * self.h ** 2.0), mnu=np.sum(self.M_nu), nnu=self.N_eff, num_massive_neutrinos=self.massive_nu, standard_neutrino_neff=3.046, omk=self.Omega_K, tau=self.tau, TCMB=self.T_cmb, **kwargs_cosmology)
        params.set_dark_energy(w=self.w0, wa=self.wa, **kwargs_dark_energy)
        z = np.atleast_1d(z)
        nz = len(z)
        if nz > 3:
            spline = 'cubic'
        else:
            spline = 'linear'
        components = {'tot': 'delta_tot', 'cdm': 'delta_cdm', 
           'b': 'delta_baryon', 
           'nu': 'delta_nu', 
           'cb': 'delta_nonu', 
           'rad': 'delta_photon', 
           'v_cdm': 'v_newtonian_cdm', 
           'v_b': 'v_newtonian_baryon', 
           'Phi': 'Weyl'}
        npoints = 1001
        if nonlinear == True:
            camb.nonlinear.Halofit(halofit_version=halofit)
            params.NonLinear = camb.model.NonLinear_both
        pk = {}
        params.set_matter_power(redshifts=z, kmax=k.max() * 2.5, silent=True)
        results = camb.get_results(params)
        for c1 in var_1:
            for c2 in var_2:
                string = c1 + '-' + c2
                kh, zz, ppkk = results.get_matter_power_spectrum(minkh=k.min() / 2.0, maxkh=k.max() * 2.5, npoints=npoints, var1=components[c1], var2=components[c2])
                if nz != 1:
                    power = si.interp2d(kh, zz, ppkk, kind=spline)
                    pk[string] = power(k, z)
                    pk[string] = np.nan_to_num(pk[string])
                else:
                    power = si.interp1d(kh, ppkk, kind=spline)
                    pk[string] = power(k)
                    pk[string] = np.nan_to_num(pk[string])

        return (
         k, pk)

    def class_Pk(self, z=0.0, k=np.logspace(-4.0, 2.0, 1001), nonlinear=False, **kwargs):
        r"""
                This routine uses CLASS to return power spectra for the chosen cosmology. Depending
                on the value of 'nonlinear', the power spectrum is linear or non-linear.

                :param z: Redshifts.
                :type z: array, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = ``np.logspace(-4., 2., 1001)``

                :param nonlinear: Whether to return non-linear power spectra.
                :type nonlinear: boolean, default = False

                :param kwargs: Keyword arguments of ``classy.pyx`` (see the file `explanatory.ini` in Class or https://github.com/lesgourg/class_public/blob/master/python/classy.pyx)

                Returns
                -------

                k: array
                    Scales in :math:`h/\mathrm{Mpc}`. Basically the same 'k' of the input.

                pk: 2D array of shape ``(len(z), len(k))``
                    Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`.
                """
        if nonlinear == True:
            halofit = 'HALOFIT'
        else:
            halofit = ''
        nk = len(np.atleast_1d(k))
        nz = len(np.atleast_1d(z))
        if nz == 1.0:
            z = np.array([z])
        else:
            z = np.array(z)
        kmax = max(k[(-1)], 500.0)
        zmax = max(z[(-1)], 101.0)
        tau = self.tau
        params = {'output': 'mPk dTk', 
           'n_s': self.ns, 
           'h': self.h, 
           'omega_b': self.Omega_b * self.h ** 2.0, 
           'omega_cdm': self.Omega_cdm * self.h ** 2.0, 
           'Omega_k': self.Omega_K, 
           'tau_reio': self.tau, 
           'T_cmb': self.T_cmb, 
           'P_k_max_h/Mpc': kmax, 
           'z_max_pk': zmax, 
           'non linear': halofit}
        if self.sigma_8 is not None:
            params['sigma8'] = self.sigma_8
        else:
            params['A_s'] = self.As
        if self.w0 != -1.0 or self.wa != 0.0:
            params['Omega_fld'] = self.Omega_lambda
            params['w0_fld'] = self.w0
            params['wa_fld'] = self.wa
        params['N_ur'] = self.massless_nu
        params['N_ncdm'] = self.massive_nu
        if self.massive_nu != 0:
            params['m_ncdm'] = (', ').join(str(x) for x in self.M_nu[(self.M_nu != 0.0)])
        for key, value in kwargs.items():
            if key not in params:
                params[key] = value
            else:
                raise KeyError('Parameter %s already exists in the dictionary, impossible to substitute it.' % key)

        cosmo = Class()
        cosmo.set(params)
        cosmo.compute()
        k *= self.h
        pk = np.zeros((nz, nk))
        for i in xrange(nk):
            for j in range(nz):
                pk[(j, i)] = cosmo.pk(k[i], z[j]) * self.h ** 3.0

        k /= self.h
        cosmo.struct_cleanup()
        cosmo.empty()
        return (
         k, pk)

    def class_XPk(self, z=0.0, k=np.logspace(-4.0, 2.0, 1001), nonlinear=False, var_1=[
 'tot'], var_2=[
 'tot'], **kwargs):
        r"""
                The function class_XPk() runs the Python wrapper of CLASS and returns auto- and 
                cross-spectra for all the quantities specified in 'var_1' and 'var_2'.
                Depending on the value of 'nonlinear', the power spectrum is linear or non-linear.
                Halofit by Takahashi is empoyed.

                :param z: Redshifts.
                :type z: array, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = ``np.logspace(-4., 2., 1001)``

                :param nonlinear: Whether to return non-linear power spectra.
                :type nonlinear: boolean, default = False

                :param var_1: Density field for the first component of the power spectrum.
                :type var_1: list of strings, default = ['tot']

                :param var_2: Density field for the second component of the power spectrum.

                 - `'tot'`   : total matter 
                 - `'cdm'`   : cold dark matter
                 - `'b'`     : baryons
                 - `'nu'`    : massive neutrinos
                 - `'ur'`    : massless neutrinos
                 - `'cb'`    : cold dark matter + baryons
                 - `'rad'`   : radiation
                 - `'Phi'`   : Weyl potential
                 - `'Psi'`   : Weyl potential
                :type var_2: list of strings, default = ['tot']

                :param kwargs: Keyword arguments of ``classy.pyx`` (see the file `explanatory.ini` in Class or https://github.com/lesgourg/class_public/blob/master/python/classy.pyx)

                Returns
                -------

                k: array
                    Scales in :math:`h/\mathrm{Mpc}`. Basically the same 'k' of the input.

                pk: dictionary
                    Keys are given by `'var_1-var_2'`. Each of these is a 2D array of shape ``(len(z), len(k))`` containing :math:`P_\mathrm{var_1-var_2}(z,k)` in units of :math:`(\mathrm{Mpc}/h)^3`.
                """
        components = {'tot': 'd_tot', 'cdm': 'd_cdm', 
           'b': 'd_b', 
           'nu': 'd_nu', 
           'ur': 'd_ur', 
           'cb': 'd_cb', 
           'rad': 'd_g', 
           'Phi': 'phi', 
           'Psi': 'psi'}
        if nonlinear == True:
            halofit = 'HALOFIT'
        else:
            halofit = ''
        nk = len(np.atleast_1d(k))
        nz = len(np.atleast_1d(z))
        if nz == 1.0:
            z = np.array([z])
        else:
            z = np.array(z)
        kmax = max(k[(-1)], 500.0)
        zmax = max(z[(-1)], 101.0)
        tau = self.tau
        params = {'output': 'mPk dTk', 
           'n_s': self.ns, 
           'h': self.h, 
           'omega_b': self.Omega_b * self.h ** 2.0, 
           'omega_cdm': self.Omega_cdm * self.h ** 2.0, 
           'Omega_k': self.Omega_K, 
           'tau_reio': self.tau, 
           'T_cmb': self.T_cmb, 
           'P_k_max_h/Mpc': kmax, 
           'z_max_pk': zmax, 
           'non linear': halofit}
        if self.sigma_8 is not None:
            params['sigma8'] = self.sigma_8
        else:
            params['A_s'] = self.As
        if self.w0 != -1.0 or self.wa != 0.0:
            params['Omega_fld'] = self.Omega_lambda
            params['w0_fld'] = self.w0
            params['wa_fld'] = self.wa
        params['N_ur'] = self.massless_nu
        params['N_ncdm'] = self.massive_nu
        if self.massive_nu != 0:
            params['m_ncdm'] = (', ').join(str(x) for x in self.M_nu[(self.M_nu != 0.0)])
        for key, value in kwargs.items():
            if key not in params:
                params[key] = value
            else:
                raise KeyError('Parameter %s already exists in the dictionary, impossible to substitute it.' % key)

        cosmo = Class()
        cosmo.set(params)
        cosmo.compute()
        nk = len(np.atleast_1d(k))
        nz = len(np.atleast_1d(z))
        n1 = len(var_1)
        n2 = len(var_2)
        if nz == 1.0:
            z = np.array([z])
        else:
            z = np.array(z)
        k *= self.h
        pk_m = np.zeros((nz, nk))
        for i in xrange(nk):
            for j in range(nz):
                pk_m[(j, i)] = cosmo.pk(k[i], z[j]) * self.h ** 3.0

        k /= self.h
        pk = {}
        for c1 in var_1:
            for c2 in var_2:
                string = c1 + '-' + c2
                pk[string] = np.zeros((len(np.atleast_1d(z)), len(k)))
                for ind_z in xrange(len(np.atleast_1d(z))):
                    TF = cosmo.get_transfer(z=z[ind_z])
                    k_T = TF['k (h/Mpc)']
                    T_m = TF['d_tot']
                    T_cdm = TF['d_cdm']
                    T_b = TF['d_b']
                    T_phi = TF['phi']
                    T_psi = TF['psi']
                    T_rad = TF['d_g']
                    T_ur = TF['d_ur']
                    TF['d_cb'] = (self.Omega_cdm * T_cdm + self.Omega_b * T_b) / self.Omega_cb
                    T_nu = np.array([ el[1] for el in list(filter(lambda item: item[0].startswith('d_ncdm'), TF.items())) ])
                    try:
                        TF['d_nu'] = np.sum(self.M_nu[(self.M_nu != 0.0)] * T_nu.T, axis=1) / np.sum(self.M_nu)
                    except np.AxisError:
                        TF['d_nu'] = np.zeros(len(k_T))

                    tm_int = si.interp1d(k_T, T_m, kind='cubic', fill_value='extrapolate')
                    transf_m = tm_int(k)
                    t1_int = si.interp1d(k_T, TF[components[c1]], kind='cubic', fill_value='extrapolate')
                    t2_int = si.interp1d(k_T, TF[components[c2]], kind='cubic', fill_value='extrapolate')
                    transf_1 = t1_int(k)
                    transf_2 = t2_int(k)
                    pk[string][ind_z] = pk_m[ind_z] * transf_1 * transf_2 / transf_m ** 2.0

        cosmo.struct_cleanup()
        cosmo.empty()
        return (
         k, pk)

    def EisensteinHu_Pk(self, z=0.0, k=np.logspace(-4.0, 2.0, 1001), sigma_8=0.83):
        r"""
                It returns the linear power spectrum in the Eisenstein & Hu approximation.

                .. warning::

                 This function does not allow to use non-flat FRW universes! ``Omega_K`` will be therefore
                 set to 0 and its value devolved to ``Omega_m``.

                .. warning::

                 This function does not reproduce massive neutrinos! Therefore ``Omega_nu`` will be set to 0 and its value transferred to ``Omega_m``.

                .. warning::

                 This function only uses :math:`w_{de} = -1`.

                .. warning::

                 This code uses :math:`\sigma_8` as a normalization. :math:`A_s` will not have any impact.

                :param z: Redshifts.
                :type z: array, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = ``np.logspace(-4., 2., 1001)``

                :param sigma_8: RMS mass fluctuation in spheres of 8 :math:`\mathrm{Mpc}/h` of radius.
                :type sigma_8: float, default = 0.83

                Returns
                -------

                k: array
                    Scales in :math:`h/\mathrm{Mpc}`. Basically the same 'k' of the input.

                pk: 2D array of shape ``(len(z), len(k))``
                    Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`.

                """
        om_m = self.Omega_m
        om_b = self.Omega_b
        n_tld = self.ns - 1.0
        h = self.h
        theta = self.T_cmb / 2.7
        if np.sum(np.atleast_1d(self.M_nu)) != 0.0:
            warnings.warn('EisensteinHu_Pk is not able to reproduce massive neutrinos as it uses the Eisenstein & Hu approximation (1998) for the linear power spectrum. The Omega_nu parameter will be transferred to Omega_lambda such that Omega_lambda -> (Omega_lambda + Omega_nu)')
            om_m -= np.sum(self.Omega_nu)
        if self.w0 != -1.0 or self.wa != 0.0:
            warnings.warn('nw_Pk is not able to reproduce non-static dark energy with w0 != -1. The dark enerdy parameters will be set to w0 = -1, wa = 0')
        if self.Omega_K != 0.0:
            warnings.warn('EisensteinHu_Pk is not able to reproduce non-flat FRW metric! The Omega_K parameter will be transferred to Omega_lambda such that Omega_lambda -> (Omega_lambda + Omega_K)')
            om_m -= self.Omega_K
        rk = k * h
        e = np.exp(1.0)
        thet = 2.728 / 2.7
        b1 = 0.313 * (om_m * h * h) ** (-0.419) * (1 + 0.607 * (om_m * h * h) ** 0.674)
        b2 = 0.238 * (om_m * h * h) ** 0.223
        zd = 1291.0 * (1 + b1 * (om_b * h * h) ** b2) * (om_m * h * h) ** 0.251 / (1.0 + 0.659 * (om_m * h * h) ** 0.828)
        ze = 25000.0 * om_m * h * h / thet ** 4.0
        rd = 31500.0 * om_b * h * h / thet ** 4.0 / zd
        re = 31500.0 * om_b * h * h / thet ** 4.0 / ze
        rke = 0.0746 * om_m * h * h / thet ** 2.0
        s = 2.0 / 3.0 / rke * np.sqrt(6.0 / re) * np.log((np.sqrt(1.0 + rd) + np.sqrt(rd + re)) / (1 + np.sqrt(re)))
        rks = 1.6 * (om_b * h * h) ** 0.52 * (om_m * h * h) ** 0.73 * (1.0 + (10.4 * om_m * h * h) ** (-0.95))
        q = rk / 13.41 / rke
        y = (1.0 + ze) / (1.0 + zd)
        g = y * (-6.0 * np.sqrt(1 + y) + (2.0 + 3.0 * y) * np.log((np.sqrt(1.0 + y) + 1.0) / (np.sqrt(1.0 + y) - 1.0)))
        ab = g * 2.07 * rke * s / (1.0 + rd) ** 0.75
        a1 = (46.9 * om_m * h * h) ** 0.67 * (1 + (32.1 * om_m * h * h) ** (-0.532))
        a2 = (12.0 * om_m * h * h) ** 0.424 * (1 + (45.0 * om_m * h * h) ** (-0.582))
        ac = a1 ** (-om_b / om_m) * a2 ** (-(om_b / om_m) ** 3.0)
        B1 = 0.944 / (1 + (458.0 * om_m * h * h) ** (-0.708))
        B2 = (0.395 * om_m * h * h) ** (-0.0266)
        bc = 1.0 / (1.0 + B1 * ((1.0 - om_b / om_m) ** B2 - 1.0))
        f = 1.0 / (1.0 + (rk * s / 5.4) ** 4.0)
        c1 = 14.2 + 386.0 / (1.0 + 69.9 * q ** 1.08)
        c2 = 14.2 / ac + 386.0 / (1.0 + 69.9 * q ** 1.08)
        tc = f * np.log(e + 1.8 * bc * q) / (np.log(e + 1.8 * bc * q) + c1 * q * q) + (1.0 - f) * np.log(e + 1.8 * bc * q) / (np.log(e + 1.8 * bc * q) + c2 * q * q)
        bb = 0.5 + om_b / om_m + (3.0 - 2.0 * om_b / om_m) * np.sqrt((17.2 * om_m * h * h) ** 2.0 + 1.0)
        bn = 8.41 * (om_m * h * h) ** 0.435
        ss = s / (1.0 + (bn / rk / s) ** 3.0) ** (1.0 / 3.0)
        tb = np.log(e + 1.8 * q) / (np.log(e + 1.8 * q) + c1 * q * q) / (1 + (rk * s / 5.2) ** 2.0)
        fac = np.exp(-(rk / rks) ** 1.4)
        tb = (tb + ab * fac / (1.0 + (bb / rk / s) ** 3.0)) * np.sin(rk * ss) / rk / ss
        T = om_b / om_m * tb + (1 - om_b / om_m) * tc
        power_tmp = k ** self.ns * (2.0 * const.PI ** 2.0) * T ** 2.0
        norm = sigma_8 / self.compute_sigma_8(k=k, pk=power_tmp)
        power_tmp *= norm ** 2.0
        nz = len(np.atleast_1d(z))
        if nz == 1:
            z = np.array([z])
        nk = len(np.atleast_1d(k))
        Pk = np.zeros((nz, nk))
        for i in xrange(nz):
            Pk[i] = power_tmp * (self.D_1(z[i]) / self.D_1(0.0)) ** 2.0

        return (k, Pk)

    def remove_bao(self, k_in, pk_in, k_low=0.028, k_high=0.45):
        r"""
                This routine removes the BAOs from the input power spectrum and returns
                the no-wiggle power spectrum in :math:`(\mathrm{Mpc}/h)^3`.
                Originally written by Mario Ballardini (you can find it in `the montepython repository <https://github.com/brinckmann/montepython_public/blob/master/montepython/likelihood_class.py>`_ .
                )

                :param k_in: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k_in: array

                :param pk_in: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`.
                :type pk_in: array

                :param k_low: Lowest scale to spline in :math:`h/\mathrm{Mpc}`.
                :type k_low: float, default = 2.8e-2

                :param k_high: Highest scale to spline in :math:`h/\mathrm{Mpc}`.
                :type k_high: float, default = 4.5e-1

                :return: array, power spectrum without BAO.
                """
        k_ref = [
         k_low, k_high]
        _interp_pk = si.interp1d(np.log(k_in), np.log(pk_in), kind='quadratic', bounds_error=False)
        interp_pk = lambda x: np.exp(_interp_pk(np.log(x)))
        idxs = np.where(np.logical_or(k_in <= k_ref[0], k_in >= k_ref[1]))
        _pk_smooth = si.UnivariateSpline(np.log(k_in[idxs]), np.log(pk_in[idxs]), k=3, s=0)
        pk_smooth = lambda x: np.exp(_pk_smooth(np.log(x)))
        fwiggle = si.UnivariateSpline(k_in, pk_in / pk_smooth(k_in), k=3, s=0)
        derivs = np.array([ fwiggle.derivatives(_k) for _k in k_in ]).T
        d2 = si.UnivariateSpline(k_in, derivs[2], k=3, s=1.0)
        wzeros = d2.roots()
        wzeros = wzeros[np.where(np.logical_and(wzeros >= k_ref[0], wzeros <= k_ref[1]))]
        wzeros = np.concatenate((wzeros, [k_ref[1]]))
        try:
            wtrend = si.UnivariateSpline(wzeros, fwiggle(wzeros), k=3, s=None, ext='extrapolate')
        except:
            wtrend = si.UnivariateSpline(k_in, fwiggle(k_in), k=3, s=None, ext='extrapolate')

        idxs = np.where(np.logical_and(k_in > k_ref[0], k_in < k_ref[1]))
        pk_nobao = pk_smooth(k_in)
        pk_nobao[idxs] *= wtrend(k_in[idxs])
        ipk = si.interp1d(k_in, pk_nobao, kind='cubic', bounds_error=False, fill_value=0.0)
        pk_nobao = ipk(k_in)
        return pk_nobao

    def compute_sigma_8(self, z=0.0, k=[], pk=[], var='tot'):
        r"""
                This routine computes :math:`sigma_8`.

                :param z: Redshift.
                :type z: array, default = 0

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :param var: component with respect to which to compute the variance.

                    - 'tot'   : total matter 
                    - 'cdm'   : cold dark matter
                    - 'b'     : baryons
                    - 'nu'    : neutrinos
                    - 'cb'    : cold dark matter + baryons
                    - 'rad'   : radiation
                    - 'v_cdm' : cdm velocity
                    - 'v_b'   : baryon velocity
                    - 'Phi'   : Weyl potential
                :type var: string, default = 'tot'

                :return: float
                """
        if pk == []:
            k, PkL = self.camb_Pk(z=z, k=np.logspace(-4.0, 2.5, 201), var_1=fundamental, var_2=fundamental)
        else:
            k, PkL = k, [pk]
        assert np.max(k) >= 10.0, 'k_max too low to obtain a convergent result. Use k_max >= 10 h/Mpc.'
        assert np.min(k) <= 0.001, 'k_min too high to obtain a convergent result. Use k_min <= 0.001 h/Mpc.'
        assert len(k) >= 100, "size of 'k' too low to obtain a convergent result. Use at least 100 points."
        R = 8.0
        integral = np.zeros(len(np.atleast_1d(z)))
        for i in range(len(np.atleast_1d(z))):
            integrand = k ** 3.0 * PkL[i] / (2.0 * const.PI ** 2.0) * self.TopHat_window(k * R) ** 2.0
            integral[i] = np.trapz(integrand, x=np.log(k))

        return integral ** 0.5

    def normalize_Pk(self, k, pk, new_sigma8):
        r"""
                This routine normalizes the input power spectrum to the required :math:`sigma_8`.

                :param k: Scales in units of :math:`h/\mathrm{Mpc}`.
                :type k: array, default = []

                :param pk: Power spectrum in units of :math:`(\mathrm{Mpc}/h)^3`. If not given, it is computed at the given redshift with CAMB.
                :type pk: array, default = []

                :param new_sigma_8: Value to which normalize.
                :type new_sigma8: float

                :return: array of normalized power spectrum in :math:`(\mathrm{Mpc}/h)^3`.
                """
        s8_in = self.compute_sigma_8(k=k, pk=pk)
        return pk * (new_sigma8 / s8_in) ** 2.0

    def class_Cl(self, l_max=3000, lensing=True, do_tensors=True, l_max_tensors=500, r=0.07, **kwargs):
        """
                Computation of the CMB angular power spectrum for the chosen cosmology.

                :param l_max: Maximum multipole to compute.
                :type l_max: integer, default = 3000

                :param lensing: Compute lensed components.
                :type lensing: boolean, default = True

                :param do_tensors: Compute tensors components.
                :type do_tensors: boolean, default = True

                :param l_max_tensors: Maximum multipole for computation of tensor components.
                :type l_max_tensors: int, default = 3000

                :param r: Tensor-to-scalar ratio.
                :type r: float, default = 0.07

                :param kwargs: Keyword arguments of Class (see the file `explanatory.ini` in Class for a list of them)

                Returns
                -------

                l: array
                    Array of integers that goes from 2 to ``l_max``

                Cl: dictionary
                    Contains the CMB angular power spectrum.

                    - `'TT'`, `'TE'`, `'EE'`, `'BB'` are the unlensed components
                    - `'TT-lensed', `'TE-lensed'`, `'EE-lensed'`, `'BB-lensed'` are the lensed components

                """
        params = {'output': 'tCl, pCl', 
           'r': r, 
           'YHe': 0.249, 
           'l_max_scalars': l_max, 
           'A_s': self.As, 
           'n_s': self.ns, 
           'h': self.h, 
           'omega_b': self.Omega_b * self.h ** 2.0, 
           'omega_cdm': self.Omega_cdm * self.h ** 2.0, 
           'Omega_k': self.Omega_K, 
           'tau_reio': self.tau, 
           'T_cmb': self.T_cmb}
        if self.w0 != -1.0 or self.wa != 0.0:
            params['Omega_fld'] = self.Omega_lambda
            params['w0_fld'] = self.w0
            params['wa_fld'] = self.wa
        params['N_ur'] = self.massless_nu
        params['N_ncdm'] = self.massive_nu
        if self.massive_nu != 0:
            params['m_ncdm'] = (', ').join(str(x) for x in self.M_nu[(self.M_nu != 0.0)])
        if do_tensors:
            params['modes'] = 's,t'
            params['l_max_tensors'] = l_max_tensors
        else:
            params['modes'] = 's'
        if lensing:
            params['output'] += ', lCl'
            params['lensing'] = 'yes'
        for key, value in kwargs.items():
            if key not in params:
                params[key] = value
            else:
                raise KeyError('Parameter %s already exists in the dictionary, impossible to substitute it.' % key)

        cosmo = Class()
        cosmo.set(params)
        cosmo.compute()
        cl_dict = cosmo.raw_cl(l_max)
        l = cl_dict['ell']
        Cl = {}
        Cl['TT'] = cl_dict['tt']
        Cl['TE'] = cl_dict['te']
        Cl['EE'] = cl_dict['ee']
        if do_tensors:
            Cl['BB'] = cl_dict['bb']
        if lensing:
            cl_dict_lens = cosmo.lensed_cl(l_max)
            Cl['TT-lensed'] = cl_dict_lens['tt']
            Cl['TE-lensed'] = cl_dict_lens['te']
            Cl['EE-lensed'] = cl_dict_lens['ee']
            if do_tensors:
                Cl['BB-lensed'] = cl_dict_lens['bb']
        return (
         l, Cl)