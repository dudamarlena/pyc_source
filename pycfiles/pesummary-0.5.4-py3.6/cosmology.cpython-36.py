# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/cosmology.py
# Compiled at: 2020-04-23 12:33:50
# Size of source mod 2**32: 1565 bytes
from pesummary import conf
from astropy import cosmology as cosmo
_available_cosmologies = cosmo.parameters.available + ['Planck15_lal']
available_cosmologies = [i.lower() for i in _available_cosmologies]

def get_cosmology(cosmology=conf.cosmology):
    """Return the cosmology that is being used

    Parameters
    ----------
    cosmology: str
        name of a known cosmology
    """
    if cosmology.lower() not in [i.lower() for i in available_cosmologies]:
        raise ValueError('Unrecognised cosmology {}. Available cosmologies are {}'.format(cosmology, ', '.join(available_cosmologies)))
    if cosmology.lower() != 'planck15_lal':
        return cosmo.__dict__[cosmology]
    else:
        return cosmo.LambdaCDM(H0=67.9, Om0=0.3065, Ode0=0.6935)