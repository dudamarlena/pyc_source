# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/astropysics/constants.py
# Compiled at: 2013-11-27 17:30:36
"""

=============================================================
constants -- physical constants and cosmological calculations
=============================================================

The :mod:`constants` module contains attributes storing physical constants and
conversion factors. Most of these are at the package level and should be
imported as::

    from astropysics.constants import c,G,ergperev

The following constants are included (all in cgs units):

* `G`: Newton's gravitational constant
* `mp`: proton mass
* `me`: electron mass
* `e`: electron charge
* `Ms`: solar mass
* `Mj`: jupiter mass
* `Me`: earth mass
* `Rs`: solar radius
* `Rj`: jupiter radius
* `Re`: mean earth radius
* `Rea`: equatorial earth radius (as defined by WGS84)
* `Reb`: polar earth radius (as defined by WGS84)
* `Lsun`: solar luminosity
* `kb`: boltzmann's constant
* `Rb`: gas constant
* `c`: speed of light - exact
* `h`: planck's constant
* `hbar`: reduced planck's constant
* `g0`: mean earth gravitational acceleration at sea level

The following unit conversion factors are also provided:

* `ergperev`
* `secperday`
* `secperyr`
* `secpergyr`
* `cmperpc`
* `pcpercm`
* `lyperpc`
* `pcperly`
* `cmperau`
* `aupercm`
* `asecperrad`
* `auperpc` (same as `asecperrad`)

Additional, convinience or derived values include:

* `GMskm`: Standard gravitational parameter for the sun in km^3 s^-2
* `GMsau`: Standard gravitational parameter for the sun in AU km^2 s^-2
* `GMspc`: Standard gravitational parameter for the sun in pc km^2 s^-2

The package also includes classes representing various cosmologies that are used
to derive relevant cosmological parameters. The current default is the
:class:`WMAP7Cosmology`, based on the LCDM cosmology with parameters favored by
`WMAP7 <http://lambda.gsfc.nasa.gov/product/map/dr4/parameters.cfm>`_ . 

The cosmological parameters for the builtin cosmologies are: 

* `H0`: Hubble's constant (all cosmologies)
* `h`: H0/100 (all cosmologies)
* `h7`: H0/70 (all cosmologies)
* `omega`: Total energy density as a fraction of the critical density (any FRW)
* `omegaR`: radiataion desnity (any FRW)
* `omegaM`: total matter density (any FRW)
* `omegaL`: dark energy/cosmological constant density (any FRW)
* `omegaK`: curvature density (any FRW)
* `sigma8`: rmc density fluctuation amplitude at 8 Mpc/h (WMAP)
* `omegaB`: Baryon density (WMAP)
* `omegaC`: dark/non-baryonic matter density (WMAP)
* `ns`: primordial power spectrum index (WMAP)
* `t0`: Age of universe in Gyr (WMAP)

The currently active cosmology will export it's parameters so they should be
used in other modules as::

    from astropysics.constants import H0,omega

.. todo:: examples for cosmologies, particularly :func:`rhoC`

Classes and Inheritance Structure
---------------------------------

.. inheritance-diagram:: astropysics.constants
   :parts: 1

Module API
----------

"""
from __future__ import division, with_statement
from math import pi
import numpy as np
unit_system = 'cgs'
G = 6.673e-08
mp = 1.67262171e-24
me = 9.1093897e-28
e = 4.8032068e-10
Ms = 1.9891e+33
Mj = 1.8986e+30
Me = 5.9742e+27
Rs = 69600000000.0
Rj = 7149200000.0
Re = 637100000.0
Rea = 637813700.0
Reb = Rea * (1 - 0.0033528106647474805)
Lsun = 3.839e+33
kb = 1.3807e-16
Rb = 83144720.0
c = 29979245800.0
h = 6.626068e-27
hbar = h / 2 / pi
g0 = 980.665
ergperev = 1.60217646e-12
secperday = 86400
secperyr = 365.25 * secperday
secpergyr = secperyr * 1000000000.0
cmperpc = 3.08568025e+18
pcpercm = 1.0 / cmperpc
lyperpc = 3.26
pcperly = 1.0 / lyperpc
cmperau = 14959788700000.0
aupercm = 1.0 / cmperau
asecperrad = 206264.80624709636
auperpc = asecperrad
GMskm = 132712440020.0
GMsau = GMskm * aupercm * 100000.0
GMspc = GMskm * pcpercm * 100000.0

def flambda_to_fnu_l(flambda, lamb):
    return flambda * lamb * lamb / c


def fnu_to_flambda_l(fnu, lamb):
    return fnu * c / lamb / lamb


def flambda_to_fnu_n(flambda, nu):
    return flambda * c / nu / nu


def fnu_to_flambda_n(fnu, nu):
    return fnu * nu * nu / c


class Cosmology(object):
    """
    A base class for a cosmology - intended to be subclassed, as this cosmology
    only has a hubble constant.
    
    *Subclassing*
    
    * All cosmologies should have a hubble constant (H0) in km/s/Mpc
    
    * Subclasses should also define a class variable :attr:`_params` with a list
      of strings that specify the names of the cosmological parameters for the 
      subclasses cosmology.  These will be exported to the constants module.
    
    * Error bars for parameters in :attr:`_params` can optional be specified as
      a class variable :attr:`<paramname>_err`.  These should be a tuple
      ``(lowererr,uppererr)``
      
    """
    _params = ('H0', )
    _autoupdate = False
    H0 = 0
    h = property(lambda self: self.H0 / 100.0, doc='Reduced Hubble constant: :math:`H_0/100`.')
    h7 = h70 = property(lambda self: self.H0 / 70.0, doc='Reduced Hubble constant: :math:`H_0/70`.')
    __params_cache = None

    @property
    def params(self):
        """
        Names of the cosmological parameters for this :class:`Cosmology`.
        """
        if self.__params_cache is None:
            import inspect
            pars = [ cls._params for cls in inspect.getmro(self.__class__) if hasattr(cls, '_params') ]
            s = set()
            for p in pars:
                s.update(p)

            self.__params_cache = tuple(s)
        return self.__params_cache

    def getParamWithError(self, parname):
        """
        Returns the requested parameter's value and its associated errors.
        
        :param parname: The name of the parameter to be retrieved.
        
        :returns: A tuple ``(parval,lowererr,uppererr)``
        """
        from operator import isSequenceType
        if parname not in self.params:
            raise ValueError('invalid parameter name %s' % parname)
        val = getattr(self, parname)
        if hasattr(self, parname + '_err'):
            err = getattr(self, parname + '_err')
        else:
            err = (0, 0)
        if isSequenceType(err):
            return (val, err[0], err[1])
        else:
            return (
             val, err, err)

    def _exportParams(self):
        pd = dict([ (p, getattr(self, p)) for p in self.params ])
        globals().update(pd)

    def _removeParams(self):
        from warnings import warn
        d = globals()
        for p in self.params:
            out = d.pop(p, None)
            if out is None:
                warn('Cosmological parameter %s not present despite being current cosmology' % p)

        return

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if self._autoupdate:
            self._exportParams()


class FRWCosmology(Cosmology):
    """
    A cosmology based on the FRW metric  with a global density, a matter 
    density, and a radiation density, and a comological constant as 
    specified at z=0
    
    default values are approximately LambdaCDM
    """
    _params = ('omega', 'omegaR', 'omegaM', 'omegaL')
    H0 = 72
    omega = property(lambda self: self.omegaR + self.omegaM + self.omegaL)
    omegaR = 0
    omegaM = 0.3
    omegaL = 0.7

    @property
    def omegaK(self):
        return 1 - self.omegaR - self.omegaM - self.omegaL

    def H(self, z):
        z = np.array(z)
        M, L, R = self.omegaM, self.omegaL, self.omegaR
        K = 1 - M - L - R
        a = 1 / (1 + z)
        return self.H0 * (R * a ** (-4) + M * a ** (-3) + L + K * a ** (-2)) ** 0.5

    def computeOmegaRz(self, z):
        """
        compute radiation density at arbitrary redshift
        """
        a = 1 / (1 + z)
        return self.rhoC(0) / self.rhoC(z) * self.omegaR * a ** (-4)

    def computeOmegaMz(self, z):
        """
        compute matter density at arbitrary redshift
        """
        a = 1 / (1 + z)
        return self.rhoC(0) / self.rhoC(z) * self.omegaM * a ** (-3)

    def computeOmegaLz(self, z):
        """
        compute cosmological constant density at arbitrary redshift
        """
        return self.omegaL * (self.rhoC(0) / self.rhoC(z))

    def computeOmegaKz(self, z, units='cgs'):
        """
        compute curvature density at arbitrary redshift
        """
        a = 1 / (1 + z)
        return self.rhoC(0) / self.rhoC(z) * self.omegaK * a ** (-2)

    def rhoC(self, z=0, units='cgs'):
        r"""
        Computes the critical density at a given redshift, e.g.
        
        .. math::
            \rho_c = \frac{3 H(z)^2}{8 \pi G}
        
        :param z: redshift at which to compute critical density
        :type z: scalar or array
        :param units: 
            
            * 'cgs': g/cm^3
            * 'cosmological': Msun/Mpc^3
        
        :type units: string
                    
        :returns: Critical density in the requested units
        :except ValueError: if an unrecognized `units` string is given
        
        """
        H = self.H(z) * 100000.0 * 1e-06 * pcpercm
        cgsres = 3 * H * H / (8 * pi * G)
        if units == 'cgs':
            return cgsres
        if units == 'cosmological':
            return cgsres / Ms * (1e-06 * pcpercm) ** (-3)
        raise ValueError('unrecognized units')

    def rho(self, z=0, units='cgs'):
        """
        mean density in this cosmology
        
        units can be 'cgs' or 'cosmological' (Mpc,Msun)
        """
        return self.omega * self.rhoC(z, units)

    def deltavir(self, z=0):
        """
        Virial overdensity asparamaterized in Bryan&Norman 98 for a given
        redshift.
        
        Good to 1% for omega(z) = 0.1-1, requires either omega = 1 (flat 
        universe) or omega_lambda = 0.
        """
        if self.omegaK != 0:
            if self.omegaL == 0:
                om = self.computeOmegaMz(z)
                x = om - 1
                return 18 * pi ** 2 + 60 * x - 32 * x ** 2
            raise NotImplementedError("can't compute deltavir with cosmological constant and omega!=1.0")
        else:
            om = self.computeOmegaMz(z)
            x = om - 1
            return 18 * pi ** 2 + 82 * x - 39 * x ** 2


class SCDMCosmology(FRWCosmology):
    """
    "Standard" CDM -- flat, with no cosmological constant.
    """
    omegaR = 0
    omegaM = 1.0
    omegaL = 0


class WMAP7Cosmology(FRWCosmology):
    """
    WMAP7-only (http://lambda.gsfc.nasa.gov/product/map/dr4/params/lcdm_sz_lens_wmap7.cfm)
    """
    _params = ('t0', 'sigma8', 'omegaB', 'omegaC', 'ns')
    t0 = 13.71
    t0_err = 0.13
    sigma8 = 0.801
    sigma8_err = 0.03
    ns = 0.963
    ns_err = 0.014
    H0 = 71.0
    H0_err = 2.5
    omegaB = 0.044
    omegaB_err = 0.0028
    omegaC = 0.222
    omegaC_err = 0.026
    omegaL = 0.734
    omegaL_err = 0.029
    omegaM = property(lambda self: self.omegaB + self.omegaC)
    omegaM_err = property(lambda self: self.omegaB_err + self.omegaC_err)


class WMAP7BAOH0Cosmology(FRWCosmology):
    """
    WMAP7+BAO+H0 (http://lambda.gsfc.nasa.gov/product/map/dr4/params/lcdm_sz_lens_wmap7_bao_h0.cfm)
    """
    _params = ('t0', 'sigma8', 'omegaB', 'omegaC', 'ns')
    t0 = 13.78
    t0_err = 0.11
    sigma8 = 0.809
    sigma8_err = 0.024
    ns = 0.963
    ns_err = 0.012
    H0 = 70.4
    H0_err = (1.4, 1.3)
    omegaB = 0.045
    omegaB_err = 0.0016
    omegaC = 0.227
    omegaC_err = 0.014
    omegaL = 0.728
    omegaL_err = (0.016, 0.015)
    omegaM = property(lambda self: self.omegaB + self.omegaC)
    omegaM_err = property(lambda self: self.omegaB_err + self.omegaC_err)


class WMAP5Cosmology(FRWCosmology):
    """
    WMAP5-only (http://lambda.gsfc.nasa.gov/product/map/dr3/parameters_summary.cfm)
    """
    _params = ('t0', 'sigma8', 'omegaB', 'omegaC', 'ns')
    t0 = 13.69
    t0_err = 0.13
    sigma8 = 0.796
    sigma8_err = 0.036
    ns = 0.963
    ns_err = (0.015, 0.014)
    H0 = 71.9
    H0_err = (2.7, 2.6)
    omegaB = 0.044
    omegaB_err = 0.003
    omegaC = 0.214
    omegaC_err = 0.027
    omegaL = 0.742
    omegaL_err = 0.03
    omegaM = property(lambda self: self.omegaB + self.omegaC)
    omegaM_err = property(lambda self: self.omegaB_err + self.omegaC_err)


class WMAP5BAOSNCosmology(FRWCosmology):
    """
    WMAP5+BAO+SN (http://lambda.gsfc.nasa.gov/product/map/dr3/parameters_summary.cfm)
    """
    _params = ('t0', 'sigma8', 'omegaB', 'omegaC', 'ns')
    t0 = 13.73
    t0_err = 0.12
    sigma8 = 0.817
    sigma8_err = 0.026
    ns = 0.96
    ns_err = (0.013, 0.014)
    H0 = 70.1
    H0_err = 1.3
    omegaB = 0.046
    omegaB_err = 0.0015
    omegaC = 0.233
    omegaC_err = 0.013
    omegaL = 0.721
    omegaL_err = 0.015
    omegaM = property(lambda self: self.omegaB + self.omegaC)
    omegaM_err = property(lambda self: self.omegaB_err + self.omegaC_err)


class WMAP3Cosmology(FRWCosmology):
    """
    WMAP3 only (http://lambda.gsfc.nasa.gov/product/map/dr2/params/lcdm_wmap.cfm)
    """
    _params = ('sigma8', 'omegaB', 'omegaC', 'ns')
    sigma8 = 0.761
    sigma8_err = (0.048, 0.049)
    ns = 0.958
    ns_err = 0.016
    H0 = 73.2
    H0_err = (3.2, 3.1)
    omegaB = 0.044
    omegaB_err = 0.0014
    omegaC = 0.224
    omegaC_err = 0.014
    omegaL = 0.732
    omegaL_err = 0.034
    omegaM = property(lambda self: self.omegaB + self.omegaC)
    omegaM_err = property(lambda self: self.omegaB_err + self.omegaC_err)


class WMAP3AllCosmology(FRWCosmology):
    """
    WMAP3+all (http://lambda.gsfc.nasa.gov/product/map/dr2/params/lcdm_all.cfm)
    """
    _params = ('sigma8', 'omegaB', 'omegaC', 'ns')
    sigma8 = 0.776
    sigma8_err = (0.032, 0.031)
    ns = 0.947
    ns_err = 0.015
    H0 = 70.4
    H0_err = (1.6, 1.5)
    omegaB = 0.042 + 0.0006666666666666666
    omegaB_err = 0.0013
    omegaC = 0.197 + 0.0006666666666666666
    omegaC_err = (0.0079, 0.0077)
    omegaL = 0.759 + 0.0006666666666666666
    omegaL_err = 0.018
    omegaM = property(lambda self: self.omegaB + self.omegaC)
    omegaM_err = property(lambda self: self.omegaB_err + self.omegaC_err)


__current_cosmology = WMAP7BAOH0Cosmology()
__current_cosmology._exportParams()
__cosmo_registry = {}

def register_cosmology(cosmocls, name=None):
    """
    Add the provided subclass of Cosmology to the cosmology registry
    
    if name is None, the name will be inferred from the class name, otherwise
    
    """
    if not name:
        name = cosmocls.__name__
    name = name.lower().replace('cosmology', '')
    try:
        if not issubclass(cosmocls, Cosmology):
            raise TypeError('Supplied object is not a subclass of Cosmology')
    except TypeError:
        raise TypeError('Supplied object to register is not a class')

    __cosmo_registry[name] = cosmocls


for o in locals().values():
    if type(o) == type and issubclass(o, Cosmology) and o != Cosmology:
        register_cosmology(o)

def choose_cosmology(nameorobj, autoupdate=True, args=None, kwargs=None):
    """
    Change the currently active cosmology and export its cosmological parameters
    into the package namespace.
    
    :param nameorobj: the new cosmology to use
    :type nameorobj: string or :class:`Cosmology` object
    :param autoupdate: 
        If True, the cosmology object will automatically propogate changes to
        its parameters up to the module variables. Otherwise,
        :func:`update_cosmology` must be called explicitly to have this behavior
        occur.
    :type autoupdate: bool
    :param args: 
        If `nameorobj` is a string, these are passed in as positional arguments
        to the object initializer (if not None). Otherwise it is ignored.
    :type args: sequence or None
    :param args: 
        If `nameorobj` is a string, these are passed in as keyword arguments to
        the object initializer (if not None). Otherwise it is ignored.
    :type args: dictionary or None
    
    :returns: the :class:`Cosmology` object after being assigned as current.
    """
    global __current_cosmology
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    if isinstance(nameorobj, basestring):
        c = __cosmo_registry[nameorobj.lower()](*args, **kwargs)
    else:
        if isinstance(nameorobj, Cosmology):
            c = nameorobj
            if c.__class__ not in __cosmo_registry.values():
                register_cosmology(c.__class__)
        __current_cosmology._removeParams()
        __current_cosmology._autoupdate = False
        try:
            c._exportParams()
            __current_cosmology = c
        except:
            __current_cosmology._exportParams()

    c._autoupdate = bool(autoupdate)
    return c


def get_cosmology(name=None):
    """
    If name is None, will retreive the currently in use Cosmology instance.
    Otherwise, returns the subclass of :class:`Cosmology` with the provided
    name.
    """
    if name is None:
        return __current_cosmology
    else:
        return __cosmo_registry[name]
        return


def update_cosmology():
    """
    updates the package-level variables for changes in the current Cosmology 
    object
    """
    __current_cosmology._exportParams()


def get_registry_names():
    """
    Returns the names of all cosmology types in the registry
    """
    return __cosmo_registry.keys()