# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/apply_cosmology.py
# Compiled at: 2019-10-24 23:32:14
# Size of source mod 2**32: 1451 bytes
import sys, inspect
from astropy.cosmology import FlatLambdaCDM

def apply_cosmology(Hubble_Constant_z0=70, Omega_Matter=0.27, Omega_Lambda=0.73, T_CMB_z0=2.725):
    stack = inspect.stack()
    if 'cosmo' in inspect.stack()[(-1)][0].f_globals.keys():
        cosmo = inspect.stack()[(-1)][0].f_globals['cosmo']
    elif 'cosmo' in inspect.stack()[(-1)][0].f_locals.keys():
        cosmo = inspect.stack()[(-1)][0].f_locals['cosmo']
    elif '%0.2f' % (Omega_Lambda + Omega_Matter) == '1.00':
        cosmo = FlatLambdaCDM(H0=Hubble_Constant_z0, Om0=Omega_Matter, Tcmb0=T_CMB_z0)
    else:
        raise NotImplementedError('Error! Non-flat cosmology not implemented yet! <TODO>')
    return cosmo


cosmo = apply_cosmology()