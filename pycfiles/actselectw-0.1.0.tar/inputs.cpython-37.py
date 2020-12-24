# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/steven/Documents/Projects/radio/EOR/OthersCodes/21cmFAST/21cmFAST/src/py21cmfast/inputs.py
# Compiled at: 2020-02-13 15:47:20
# Size of source mod 2**32: 28090 bytes
"""
Input parameter classes.

There are four input parameter/option classes, not all of which are required for any
given function. They are :class:`UserParams`, :class:`CosmoParams`, :class:`AstroParams`
and :class:`FlagOptions`. Each of them defines a number of variables, and all of these
have default values, to minimize the burden on the user. These defaults are accessed via
the ``_defaults_`` class attribute of each class. The available parameters for each are
listed in the documentation for each class below.

Along with these, the module exposes ``global_params``, a singleton object of type
:class:`GlobalParams`, which is a simple class providing read/write access to a number of parameters
used throughout the computation which are very rarely varied.
"""
import contextlib, logging
from os import path
from astropy.cosmology import Planck15
from ._utils import StructInstanceWrapper
from ._utils import StructWithDefaults
from .c_21cmfast import ffi
from .c_21cmfast import lib
logger = logging.getLogger('21cmFAST')

class GlobalParams(StructInstanceWrapper):
    __doc__ = '\n    Global parameters for 21cmFAST.\n\n    This is a thin wrapper over an allocated C struct, containing parameter values\n    which are used throughout various computations within 21cmFAST. It is a singleton;\n    that is, a single python (and C) object exists, and no others should be created.\n    This object is not "passed around", rather its values are accessed throughout the\n    code.\n\n    Parameters in this struct are considered to be options that should usually not have\n    to be modified, and if so, typically once in any given script or session.\n\n    Values can be set in the normal way, eg.:\n\n    >>> global_params.ALPHA_UVB = 5.5\n\n    The class also provides a context manager for setting parameters for a well-defined\n    portion of the code. For example, if you would like to set ``Z_HEAT_MAX`` for a given\n    run:\n\n    >>> with global_params.use(Z_HEAT_MAX=25):\n    >>>     p21c.run_lightcone(...)  # uses Z_HEAT_MAX=25 for the entire run.\n    >>> print(global_params.Z_HEAT_MAX)\n    35.0\n\n    Attributes\n    ----------\n    ALPHA_UVB : float\n        Power law index of the UVB during the EoR.  This is only used if `INHOMO_RECO` is\n        True (in :class:`FlagOptions`), in order to compute the local mean free path\n        inside the cosmic HII regions.\n    EVOLVE_DENSITY_LINEARLY : bool\n        Whether to evolve the density field with linear theory (instead of 1LPT or Zel\'Dovich).\n        If choosing this option, make sure that your cell size is\n        in the linear regime at the redshift of interest. Otherwise, make sure you resolve\n        small enough scales, roughly we find BOX_LEN/DIM should be < 1Mpc\n    SMOOTH_EVOLVED_DENSITY_FIELD : bool\n        If True, the zeldovich-approximation density field is additionally smoothed\n        (aside from the implicit boxcar smoothing performed when re-binning the ICs from\n        DIM to HII_DIM) with a Gaussian filter of width ``R_smooth_density*BOX_LEN/HII_DIM``.\n        The implicit boxcar smoothing in ``perturb_field()`` bins the density field on\n        scale DIM/HII_DIM, similar to what Lagrangian codes do when constructing Eulerian\n        grids. In other words, the density field is quantized into ``(DIM/HII_DIM)^3`` values.\n        If your usage requires smooth density fields, it is recommended to set this to True.\n        This also decreases the shot noise present in all grid based codes, though it\n        overcompensates by an effective loss in resolution. **Added in 1.1.0**.\n    R_smooth_density : float\n        Determines the smoothing length to use if `SMOOTH_EVOLVED_DENSITY_FIELD` is True.\n    SECOND_ORDER_LPT_CORRECTIONS : bool\n        Use second-order Lagrangian perturbation theory (2LPT).\n        Set this to True if the density field or the halo positions are extrapolated to\n        low redshifts. The current implementation is very naive and adds a factor ~6 to\n        the memory requirements. Reference: Scoccimarro R., 1998, MNRAS, 299, 1097-1118\n        Appendix D.\n    HII_ROUND_ERR : float\n        Rounding error on the ionization fraction. If the mean xHI is greater than\n        ``1 - HII_ROUND_ERR``, then finding HII bubbles is skipped, and a homogeneous\n        xHI field of ones is returned. Added in  v1.1.0.\n    FIND_BUBBLE_ALGORITHM : int, {1,2}\n        Choose which algorithm used to find HII bubbles. Options are: (1) Mesinger & Furlanetto 2007\n        method of overlapping spheres: paint an ionized sphere with radius R, centered on pixel\n        where R is filter radius. This method, while somewhat more accurate, is slower than (2),\n        especially in mostly ionized universes, so only use for lower resolution boxes\n        (HII_DIM<~400). (2) Center pixel only method (Zahn et al. 2007). This is faster.\n    N_POISSON : int\n        If not using the halo field to generate HII regions, we provide the option of\n        including Poisson scatter in the number of sources obtained through the conditional\n        collapse fraction (which only gives the *mean* collapse fraction on a particular\n        scale. If the predicted mean collapse fraction is less than  `N_POISSON * M_MIN`,\n        then Poisson scatter is added to mimic discrete halos on the subgrid scale (see\n        Zahn+2010).Use a negative number to turn it off.\n\n        .. note:: If you are interested in snapshots of the same realization at several\n                  redshifts,it is recommended to turn off this feature, as halos can\n                  stochastically "pop in and out of" existence from one redshift to the next.\n\n    T_USE_VELOCITIES : bool\n        Whether to use velocity corrections in 21-cm fields\n\n        .. note:: The approximation used to include peculiar velocity effects works\n                  only in the linear regime, so be careful using this (see Mesinger+2010)\n\n    MAX_DVDR : float\n        Maximum velocity gradient along the line of sight in units of the hubble parameter at z.\n        This is only used in computing the 21cm fields.\n\n        .. note:: Setting this too high can add spurious 21cm power in the early stages,\n                  due to the 1-e^-tau ~ tau approximation (see Mesinger\'s 21cm intro paper and mao+2011).\n                  However, this is still a good approximation at the <~10% level.\n\n    VELOCITY_COMPONENT : int\n        Component of the velocity to be used in 21-cm temperature maps (1=x, 2=y, 3=z)\n    DELTA_R_HII_FACTOR : float\n        Factor by which to scroll through filter radius for bubbles\n    HII_FILTER : int, {0, 1, 2}\n        Filter for the Halo or density field used to generate ionization field:\n        0. real space top hat filter\n        1. k-space top hat filter\n        2. gaussian filter\n    INITIAL_REDSHIFT : float\n        Used to perturb field\n    CRIT_DENS_TRANSITION : float\n        A transition value for the interpolation tables for calculating the number of ionising\n        photons produced given the input parameters. Log sampling is desired, however the numerical\n        accuracy near the critical density for collapse (i.e. 1.69) broke down. Therefore, below the\n        value for `CRIT_DENS_TRANSITION` log sampling of the density values is used, whereas above\n        this value linear sampling is used.\n    MIN_DENSITY_LOW_LIMIT : float\n        Required for using the interpolation tables for the number of ionising photons. This is a\n        lower limit for the density values that is slightly larger than -1. Defined as a density\n        contrast.\n    RecombPhotonCons : int\n        Whether or not to use the recombination term when calculating the filling factor for\n        performing the photon non-conservation correction.\n    PhotonConsStart : float\n        A starting value for the neutral fraction where the photon non-conservation correction is\n        performed exactly. Any value larger than this the photon non-conservation correction is not\n        performed (i.e. the algorithm is perfectly photon conserving).\n    PhotonConsEnd : float\n        An end-point for where the photon non-conservation correction is performed exactly. This is\n        required to remove undesired numerical artifacts in the resultant neutral fraction histories.\n    PhotonConsAsymptoteTo : float\n        Beyond `PhotonConsEnd` the photon non-conservation correction is extrapolated to yield\n        smooth reionisation histories. This sets the lowest neutral fraction value that the photon\n        non-conservation correction will be applied to.\n    HEAT_FILTER : int\n        Filter used for smoothing the linear density field to obtain the collapsed fraction:\n            0: real space top hat filter\n            1: sharp k-space filter\n            2: gaussian filter\n    CLUMPING_FACTOR : float\n        Sub grid scale. If you want to run-down from a very high redshift (>50), you should\n        set this to one.\n    Z_HEAT_MAX : float\n        Maximum redshift used in the Tk and x_e evolution equations.\n        Temperature and x_e are assumed to be homogeneous at higher redshifts.\n        Lower values will increase performance.\n    R_XLy_MAX : float\n        Maximum radius of influence for computing X-ray and Lya pumping in cMpc. This\n        should be larger than the mean free path of the relevant photons.\n    NUM_FILTER_STEPS_FOR_Ts : int\n        Number of spherical annuli used to compute df_coll/dz\' in the simulation box.\n        The spherical annuli are evenly spaced in logR, ranging from the cell size to the box\n        size. :func:`~wrapper.spin_temp` will create this many boxes of size `HII_DIM`,\n        so be wary of memory usage if values are high.\n    ZPRIME_STEP_FACTOR : float\n        Logarithmic redshift step-size used in the z\' integral.  Logarithmic dz.\n        Decreasing (closer to unity) increases total simulation time for lightcones,\n        and for Ts calculations.\n    TK_at_Z_HEAT_MAX : float\n        If positive, then overwrite default boundary conditions for the evolution\n        equations with this value. The default is to use the value obtained from RECFAST.\n        See also `XION_at_Z_HEAT_MAX`.\n    XION_at_Z_HEAT_MAX : float\n        If positive, then overwrite default boundary conditions for the evolution\n        equations with this value. The default is to use the value obtained from RECFAST.\n        See also `TK_at_Z_HEAT_MAX`.\n    Pop : int\n        Stellar Population responsible for early heating (2 or 3)\n    Pop2_ion : float\n        Number of ionizing photons per baryon for population 2 stellar species.\n    Pop3_ion : float\n        Number of ionizing photons per baryon for population 3 stellar species.\n    NU_X_BAND_MAX : float\n        This is the upper limit of the soft X-ray band (0.5 - 2 keV) used for normalising\n        the X-ray SED to observational limits set by the X-ray luminosity. Used for performing\n        the heating rate integrals.\n    NU_X_MAX : float\n        An upper limit (must be set beyond `NU_X_BAND_MAX`) for performing the rate integrals.\n        Given the X-ray SED is modelled as a power-law, this removes the potential of divergent\n        behaviour for the heating rates. Chosen purely for numerical convenience though it is\n        motivated by the fact that observed X-ray SEDs apprear to turn-over around 10-100 keV\n        (Lehmer et al. 2013, 2015)\n    NBINS_LF : int\n        Number of bins for the luminosity function calculation.\n    P_CUTOFF : bool\n        Turn on Warm-Dark-matter power suppression.\n    M_WDM : float\n        Mass of WDM particle in keV. Ignored if `P_CUTOFF` is False.\n    g_x : float\n        Degrees of freedom of WDM particles; 1.5 for fermions.\n    OMn : float\n        Relative density of neutrinos in the universe.\n    OMk : float\n        Relative density of curvature.\n    OMr : float\n        Relative density of radiation.\n    OMtot : float\n        Fractional density of the universe with respect to critical density. Set to\n        unity for a flat universe.\n    Y_He : float\n        Helium fraction.\n    wl : float\n        Dark energy equation of state parameter (wl = -1 for vacuum )\n    SHETH_b : float\n        Sheth-Tormen parameter for ellipsoidal collapse (for HMF).\n\n        .. note:: The best fit b and c ST params for these 3D realisations have a redshift,\n                  and a ``DELTA_R_FACTOR`` dependence, as shown\n                  in Mesinger+. For converged mass functions at z~5-10, set `DELTA_R_FACTOR=1.1`\n                  and `SHETH_b=0.15` and `SHETH_c~0.05`.\n\n                  For most purposes, a larger step size is quite sufficient and provides an\n                  excellent match to N-body and smoother mass functions, though the b and c\n                  parameters should be changed to make up for some "stepping-over" massive\n                  collapsed halos (see Mesinger, Perna, Haiman (2005) and Mesinger et al.,\n                  in preparation).\n\n                  For example, at z~7-10, one can set `DELTA_R_FACTOR=1.3` and `SHETH_b=0.15`\n                   and `SHETH_c=0.25`, to increase the speed of the halo finder.\n    SHETH_c : float\n        Sheth-Tormen parameter for ellipsoidal collapse (for HMF). See notes for `SHETH_b`.\n    Zreion_HeII : float\n        Redshift of helium reionization, currently only used for tau_e\n    FILTER : int, {0, 1}\n        Filter to use for smoothing.\n        0. tophat\n        1. gaussian\n    external_table_path : str\n        The system path to find external tables for calculation speedups. DO NOT MODIFY.\n    '

    def __init__(self, wrapped, ffi):
        super().__init__(wrapped, ffi)
        EXTERNALTABLES = ffi.new('char[]', path.join(path.expanduser('~'), '.21cmfast').encode())
        self.external_table_path = EXTERNALTABLES

    @contextlib.contextmanager
    def use(self, **kwargs):
        """Set given parameters for a certain context.

        .. note:: Keywords are *not* case-sensitive.

        Examples
        --------
        >>> from py21cmfast import global_params, run_lightcone
        >>> with global_params.use(zprime_step_factor=1.1, Sheth_c=0.06):
        >>>     run_lightcone(redshift=7)
        """
        prev = {}
        this_attr_upper = {k.upper():k for k in self.keys()}
        for k, val in kwargs.items():
            if k.upper() not in this_attr_upper:
                raise ValueError('{} is not a valid parameter of global_params'.format(k))
            else:
                key = this_attr_upper[k.upper()]
                prev[key] = getattr(self, key)
                setattr(self, key, val)

        yield
        for k, v in prev.items():
            setattr(self, k, v)


global_params = GlobalParams(lib.global_params, ffi)

class CosmoParams(StructWithDefaults):
    __doc__ = '\n    Cosmological parameters (with defaults) which translates to a C struct.\n\n    To see default values for each parameter, use ``CosmoParams._defaults_``.\n    All parameters passed in the constructor are also saved as instance attributes which should\n    be considered read-only. This is true of all input-parameter classes.\n\n    Parameters\n    ----------\n    SIGMA_8 : float, optional\n        RMS mass variance (power spectrum normalisation).\n    hlittle : float, optional\n        The hubble parameter, H_0/100.\n    OMm : float, optional\n        Omega matter.\n    OMb : float, optional\n        Omega baryon, the baryon component.\n    POWER_INDEX : float, optional\n        Spectral index of the power spectrum.\n    '
    _ffi = ffi
    _defaults_ = {'SIGMA_8':0.82, 
     'hlittle':Planck15.h, 
     'OMm':Planck15.Om0, 
     'OMb':Planck15.Ob0, 
     'POWER_INDEX':0.97}

    @property
    def OMl(self):
        """Omega lambda, dark energy density."""
        return 1 - self.OMm

    @property
    def cosmo(self):
        """Return an astropy cosmology object for this cosmology."""
        return Planck15.clone(H0=(self.hlittle * 100), Om0=(self.OMm), Ob0=(self.OMb))


class UserParams(StructWithDefaults):
    __doc__ = '\n    Structure containing user parameters (with defaults).\n\n    To see default values for each parameter, use ``UserParams._defaults_``.\n    All parameters passed in the constructor are also saved as instance attributes which should\n    be considered read-only. This is true of all input-parameter classes.\n\n    Parameters\n    ----------\n    HII_DIM : int, optional\n        Number of cells for the low-res box. Default 50.\n    DIM : int,optional\n        Number of cells for the high-res box (sampling ICs) along a principal axis. To avoid\n        sampling issues, DIM should be at least 3 or 4 times HII_DIM, and an integer multiple.\n        By default, it is set to 4*HII_DIM.\n    BOX_LEN : float, optional\n        Length of the box, in Mpc. Default 150.\n    HMF: int or str, optional\n        Determines which halo mass function to be used for the normalisation of the\n        collapsed fraction (default Sheth-Tormen). If string should be one of the\n        following codes:\n        0: PS (Press-Schechter)\n        1: ST (Sheth-Tormen)\n        2: Watson (Watson FOF)\n        3: Watson-z (Watson FOF-z)\n    USE_RELATIVE_VELOCITIES: int, optional\n        Flag to decide whether to use relative velocities.\n        If True, POWER_SPECTRUM is automatically set to 5. Default False.\n    POWER_SPECTRUM: int or str, optional\n        Determines which power spectrum to use, default EH (unless `USE_RELATIVE_VELOCITIES`\n        is True). If string, use the following codes:\n        0: EH\n        1: BBKS\n        2: EFSTATHIOU\n        3: PEEBLES\n        4: WHITE\n        5: CLASS (single cosmology)\n    '
    _ffi = ffi
    _defaults_ = {'BOX_LEN':150.0, 
     'DIM':None, 
     'HII_DIM':50, 
     'USE_FFTW_WISDOM':False, 
     'HMF':1, 
     'USE_RELATIVE_VELOCITIES':False, 
     'POWER_SPECTRUM':0}
    _hmf_models = [
     'PS', 'ST', 'WATSON', 'WATSON-Z']
    _power_models = ['EH', 'BBKS', 'EFSTATHIOU', 'PEEBLES', 'WHITE', 'CLASS']

    @property
    def DIM(self):
        """Number of cells for the high-res box (sampling ICs) along a principal axis."""
        return self._DIM or 4 * self.HII_DIM

    @property
    def tot_fft_num_pixels(self):
        """Total number of pixels in the high-res box."""
        return self.DIM ** 3

    @property
    def HII_tot_num_pixels(self):
        """Total number of pixels in the low-res box."""
        return self.HII_DIM ** 3

    @property
    def POWER_SPECTRUM(self):
        """
        The power spectrum generator to use, as an integer.

        See :func:`power_spectrum_model` for a string representation.
        """
        if self.USE_RELATIVE_VELOCITIES and not self._POWER_SPECTRUM != 5:
            if isinstance(self._POWER_SPECTRUM, str):
                if self._POWER_SPECTRUM.upper() != 'CLASS':
                    logger.warning('Automatically setting POWER_SPECTRUM to 5 (CLASS) as you are using relative velocities')
            else:
                return 5
                if isinstance(self._POWER_SPECTRUM, str):
                    val = self._power_models.index(self._POWER_SPECTRUM.upper())
                else:
                    val = self._POWER_SPECTRUM
            if not 0 <= val < len(self._power_models):
                raise ValueError('Power spectrum must be between 0 and {}'.format(len(self._power_models) - 1))
        return val

    @property
    def HMF(self):
        """The HMF to use (an int, mapping to a given form).

        See hmf_model for a string representation.
        """
        if isinstance(self._HMF, str):
            val = self._hmf_models.index(self._HMF.upper())
        else:
            val = self._HMF
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise ValueError('Invalid value for HMF')

        if not 0 <= val < len(self._hmf_models):
            raise ValueError('HMF must be an int between 0 and {}'.format(len(self._hmf_models) - 1))
        return val

    @property
    def hmf_model(self):
        """String representation of the HMF model used."""
        return self._hmf_models[self.HMF]

    @property
    def power_spectrum_model(self):
        """String representation of the power spectrum model used."""
        return self._power_models[self.POWER_SPECTRUM]


class FlagOptions(StructWithDefaults):
    __doc__ = '\n    Flag-style options for the ionization routines.\n\n    To see default values for each parameter, use ``FlagOptions._defaults_``.\n    All parameters passed in the constructor are also saved as instance attributes\n    which should be considered read-only. This is true of all input-parameter classes.\n\n    Note that all flags are set to False by default, giving the simplest "vanilla"\n    version of 21cmFAST.\n\n    Parameters\n    ----------\n    USE_MASS_DEPENDENT_ZETA : bool, optional\n        Set to True if using new parameterization. Setting to True will automatically\n        set `M_MIN_in_Mass` to True.\n    SUBCELL_RSDS : bool, optional\n        Add sub-cell redshift-space-distortions (cf Sec 2.2 of Greig+2018).\n        Will only be effective if `USE_TS_FLUCT` is True.\n    INHOMO_RECO : bool, optional\n        Whether to perform inhomogeneous recombinations. Increases the computation\n        time.\n    USE_TS_FLUCT : bool, optional\n        Whether to perform IGM spin temperature fluctuations (i.e. X-ray heating).\n        Dramatically increases the computation time.\n    M_MIN_in_Mass : bool, optional\n        Whether the minimum halo mass (for ionization) is defined by\n        mass or virial temperature. Automatically True if `USE_MASS_DEPENDENT_ZETA`\n        is True.\n    PHOTON_CONS : bool, optional\n        Whether to perform a small correction to account for the inherent\n        photon non-conservation.\n    '
    _ffi = ffi
    _defaults_ = {'USE_MASS_DEPENDENT_ZETA':False, 
     'SUBCELL_RSD':False, 
     'INHOMO_RECO':False, 
     'USE_TS_FLUCT':False, 
     'M_MIN_in_Mass':False, 
     'PHOTON_CONS':False}

    @property
    def M_MIN_in_Mass(self):
        """Whether minimum halo mass is defined in mass or virial temperature."""
        if self.USE_MASS_DEPENDENT_ZETA:
            return True
        return self._M_MIN_in_Mass


class AstroParams(StructWithDefaults):
    __doc__ = '\n    Astrophysical parameters.\n\n    To see default values for each parameter, use ``AstroParams._defaults_``.\n    All parameters passed in the constructor are also saved as instance attributes which should\n    be considered read-only. This is true of all input-parameter classes.\n\n    Parameters\n    ----------\n    INHOMO_RECO : bool, optional\n        Whether inhomogeneous recombinations are being calculated. This is not a part of the\n        astro parameters structure, but is required by this class to set some default behaviour.\n    HII_EFF_FACTOR : float, optional\n        The ionizing efficiency of high-z galaxies (zeta, from Eq. 2 of Greig+2015).\n        Higher values tend to speed up reionization.\n    F_STAR10 : float, optional\n        The fraction of galactic gas in stars for 10^10 solar mass haloes.\n        Only used in the "new" parameterization,\n        i.e. when `USE_MASS_DEPENDENT_ZETA` is set to True (in :class:`FlagOptions`).\n        If so, this is used along with `F_ESC10` to determine `HII_EFF_FACTOR` (which\n        is then unused). See Eq. 11 of Greig+2018 and Sec 2.1 of Park+2018.\n        Given in log10 units.\n    ALPHA_STAR : float, optional\n        Power-law index of fraction of galactic gas in stars as a function of halo mass.\n        See Sec 2.1 of Park+2018.\n    F_ESC10 : float, optional\n        The "escape fraction", i.e. the fraction of ionizing photons escaping into the\n        IGM, for 10^10 solar mass haloes. Only used in the "new" parameterization,\n        i.e. when `USE_MASS_DEPENDENT_ZETA` is set to True (in :class:`FlagOptions`).\n        If so, this is used along with `F_STAR10` to determine `HII_EFF_FACTOR` (which\n        is then unused). See Eq. 11 of Greig+2018 and Sec 2.1 of Park+2018.\n    ALPHA_ESC : float, optional\n        Power-law index of escape fraction as a function of halo mass. See Sec 2.1 of\n        Park+2018.\n    M_TURN : float, optional\n        Turnover mass (in log10 solar mass units) for quenching of star formation in\n        halos, due to SNe or photo-heating feedback, or inefficient gas accretion. Only\n        used if `USE_MASS_DEPENDENT_ZETA` is set to True in :class:`FlagOptions`.\n        See Sec 2.1 of Park+2018.\n    R_BUBBLE_MAX : float, optional\n        Mean free path in Mpc of ionizing photons within ionizing regions (Sec. 2.1.2 of\n        Greig+2015). Default is 50 if `INHOMO_RECO` is True, or 15.0 if not.\n    ION_Tvir_MIN : float, optional\n        Minimum virial temperature of star-forming haloes (Sec 2.1.3 of Greig+2015).\n        Given in log10 units.\n    L_X : float, optional\n        The specific X-ray luminosity per unit star formation escaping host galaxies.\n        Cf. Eq. 6 of Greig+2018. Given in log10 units.\n    NU_X_THRESH : float, optional\n        X-ray energy threshold for self-absorption by host galaxies (in eV). Also called\n        E_0 (cf. Sec 4.1 of Greig+2018). Typical range is (100, 1500).\n    X_RAY_SPEC_INDEX : float, optional\n        X-ray spectral energy index (cf. Sec 4.1 of Greig+2018). Typical range is\n        (-1, 3).\n    X_RAY_Tvir_MIN : float, optional\n        Minimum halo virial temperature in which X-rays are produced. Given in log10\n        units. Default is `ION_Tvir_MIN`.\n    t_STAR : float, optional\n        Fractional characteristic time-scale (fraction of hubble time) defining the\n        star-formation rate of galaxies. Only used if `USE_MASS_DEPENDENT_ZETA` is set\n        to True in :class:`FlagOptions`. See Sec 2.1, Eq. 3 of Park+2018.\n    N_RSD_STEPS : int, optional\n        Number of steps used in redshift-space-distortion algorithm. NOT A PHYSICAL\n        PARAMETER.\n    '
    _ffi = ffi
    _defaults_ = {'HII_EFF_FACTOR':30.0, 
     'F_STAR10':-1.3, 
     'ALPHA_STAR':0.5, 
     'F_ESC10':-1.0, 
     'ALPHA_ESC':-0.5, 
     'M_TURN':8.7, 
     'R_BUBBLE_MAX':None, 
     'ION_Tvir_MIN':4.69897, 
     'L_X':40.0, 
     'NU_X_THRESH':500.0, 
     'X_RAY_SPEC_INDEX':1.0, 
     'X_RAY_Tvir_MIN':None, 
     't_STAR':0.5, 
     'N_RSD_STEPS':20}

    def __init__(self, *args, INHOMO_RECO=FlagOptions._defaults_['INHOMO_RECO'], **kwargs):
        self.INHOMO_RECO = INHOMO_RECO
        (super().__init__)(*args, **kwargs)

    def convert(self, key, val):
        """Convert a given attribute before saving it the instance."""
        if key in ('F_STAR10', 'F_ESC10', 'M_TURN', 'ION_Tvir_MIN', 'L_X', 'X_RAY_Tvir_MIN'):
            return 10 ** val
        return val

    @property
    def R_BUBBLE_MAX(self):
        """Maximum radius of bubbles to be searched. Set dynamically."""
        if not self._R_BUBBLE_MAX:
            if self.INHOMO_RECO:
                return 50.0
            return 15.0
        if self.INHOMO_RECO:
            if self._R_BUBBLE_MAX != 50:
                logger.warning('You are setting R_BUBBLE_MAX != 50 when INHOMO_RECO=True. This is non-standard (but allowed), and usually occurs upon manual update of INHOMO_RECO')
        return self._R_BUBBLE_MAX

    @property
    def X_RAY_Tvir_MIN(self):
        """Minimum virial temperature of X-ray emitting sources (unlogged and set dynamically)."""
        if self._X_RAY_Tvir_MIN:
            return self._X_RAY_Tvir_MIN
        return self.ION_Tvir_MIN