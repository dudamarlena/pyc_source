# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/torchani/units.py
# Compiled at: 2020-04-29 02:37:56
# Size of source mod 2**32: 5973 bytes
"""Unit conversion factors used in torchani

The torchani networks themselves works internally entirely in Hartrees
(energy), Angstroms (distance) and AMU (mass). In some example code and scripts
we convert to other more commonly used units. Our conversion factors are
consistent with `CODATA 2014 recommendations`_, which is also consistent with
the `units used in ASE`_. (However, take into account that ASE uses
electronvolt as its base energy unit, so the appropriate conversion factors
should always be applied when converting from ASE to torchani) Joule-to-kcal
conversion taken from the `IUPAC Goldbook`_.  All the conversion factors we use
are defined in this module, and convenience functions to convert between
different units are provided.

.. _units used in ASE:
    https://wiki.fysik.dtu.dk/ase/ase/units.html#units

.. _CODATA 2014 recommendations:
    https://arxiv.org/pdf/1507.07956.pdf

.. _IUPAC Goldbook:
    https://goldbook.iupac.org/terms/view/C00784

"""
import math
HARTREE_TO_EV = 27.211386024367243
EV_TO_JOULE = 1.6021766208e-19
JOULE_TO_KCAL = 0.0002390057361376673
HARTREE_TO_JOULE = HARTREE_TO_EV * EV_TO_JOULE
AVOGADROS_NUMBER = 6.022140857e+23
SPEED_OF_LIGHT = 299792458.0
AMU_TO_KG = 1.66053904e-27
ANGSTROM_TO_METER = 1e-10
NEWTON_TO_MILLIDYNE = 100000000.0
HARTREE_TO_KCALMOL = HARTREE_TO_JOULE * JOULE_TO_KCAL * AVOGADROS_NUMBER
HARTREE_TO_KJOULEMOL = HARTREE_TO_JOULE * AVOGADROS_NUMBER / 1000
EV_TO_KCALMOL = EV_TO_JOULE * JOULE_TO_KCAL * AVOGADROS_NUMBER
EV_TO_KJOULEMOL = EV_TO_JOULE * AVOGADROS_NUMBER / 1000
INVCM_TO_EV = 0.0001239841973964072
SQRT_MHESSIAN_TO_INVCM = math.sqrt(HARTREE_TO_JOULE / AMU_TO_KG) / ANGSTROM_TO_METER / SPEED_OF_LIGHT / 100
SQRT_MHESSIAN_TO_MILLIEV = SQRT_MHESSIAN_TO_INVCM * INVCM_TO_EV * 1000
MHESSIAN_TO_FCONST = HARTREE_TO_JOULE * NEWTON_TO_MILLIDYNE / ANGSTROM_TO_METER

def sqrt_mhessian2invcm(x):
    """Converts sqrt(mass-scaled hessian units) into cm^-1

    Converts form units of sqrt(Hartree / (amu * Angstrom^2))
    which are sqrt(units of the mass-scaled hessian matrix)
    into units of inverse centimeters.

    Take into account that to convert the actual eigenvalues of the hessian
    into wavenumbers it is necessary to multiply by an extra factor of 1 / (2 *
    pi)"""
    return x * SQRT_MHESSIAN_TO_INVCM


def sqrt_mhessian2milliev(x):
    """Converts sqrt(mass-scaled hessian units) into meV

    Converts form units of sqrt(Hartree / (amu * Angstrom^2))
    which are sqrt(units of the mass-scaled hessian matrix)
    into units of milli-electronvolts.

    Take into account that to convert the actual eigenvalues of the hessian
    into wavenumbers it is necessary to multiply by an extra factor of 1 / (2 *
    pi)"""
    return x * SQRT_MHESSIAN_TO_MILLIEV


def mhessian2fconst(x):
    """Converts mass-scaled hessian units into mDyne/Angstrom

    Converts from units of mass-scaled hessian (Hartree / (amu * Angstrom^2)
    into force constant units (mDyne/Angstom), where 1 N = 1 * 10^8 mDyne"""
    return x * MHESSIAN_TO_FCONST


def hartree2ev(x):
    """Hartree to eV conversion factor from 2014 CODATA"""
    return x * HARTREE_TO_EV


def ev2kjoulemol(x):
    """Electronvolt to kJ/mol conversion factor from CODATA 2014"""
    return x * EV_TO_KJOULEMOL


def ev2kcalmol(x):
    """Electronvolt to kcal/mol conversion factor from CODATA 2014"""
    return x * EV_TO_KCALMOL


def hartree2kjoulemol(x):
    """Hartree to kJ/mol conversion factor from CODATA 2014"""
    return x * HARTREE_TO_KJOULEMOL


def hartree2kcalmol(x):
    """Hartree to kJ/mol conversion factor from CODATA 2014"""
    return x * HARTREE_TO_KCALMOL


hartree2ev.__doc__ = str(hartree2ev.__doc__) + f"\n\n1 Hartree = {hartree2ev(1)} eV"
hartree2kcalmol.__doc__ = str(hartree2kcalmol.__doc__) + f"\n\n1 Hartree = {hartree2kcalmol(1)} kcal/mol"
hartree2kjoulemol.__doc__ = str(hartree2kjoulemol) + f"\n\n1 Hartree = {hartree2kjoulemol(1)} kJ/mol"
ev2kjoulemol.__doc__ = str(ev2kjoulemol.__doc__) + f"\n\n1 eV = {ev2kjoulemol(1)} kJ/mol"
ev2kcalmol.__doc__ = str(ev2kcalmol.__doc__) + f"\n\n1 eV = {ev2kcalmol(1)} kcal/mol"
mhessian2fconst.__doc__ = str(mhessian2fconst.__doc__) + f"\n\n1 Hartree / (AMU * Angstrom^2) = {ev2kcalmol(1)} mDyne/Angstrom"
sqrt_mhessian2milliev.__doc__ = str(sqrt_mhessian2milliev.__doc__) + f"\n\n1 sqrt(Hartree / (AMU * Angstrom^2)) = {sqrt_mhessian2milliev(1)} meV"
sqrt_mhessian2invcm.__doc__ = str(sqrt_mhessian2invcm.__doc__) + f"\n\n1 sqrt(Hartree / (AMU * Angstrom^2)) = {sqrt_mhessian2invcm(1)} cm^-1"