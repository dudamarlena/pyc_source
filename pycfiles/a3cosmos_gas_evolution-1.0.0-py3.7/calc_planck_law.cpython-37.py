# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_planck_law.py
# Compiled at: 2019-07-18 22:30:15
# Size of source mod 2**32: 1052 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy import units as u
from astropy import constants as const
from astropy.modeling.blackbody import blackbody_lambda, blackbody_nu
if sys.version_info.major >= 3:
    long = int
else:
    if __name__ == '__main__':
        if len(sys.argv) <= 1:
            print('Usage: ')
            print('calc_planck_law.py lambda_um T_dust[=25.0K]')
            print('')
            sys.exit()
        else:
            lambda_um = float(sys.argv[1])
            if len(sys.argv) > 2:
                T_dust = float(sys.argv[2])
            else:
                T_dust = 25.0
        print('T_dust = %s [K]' % T_dust)
        cal_Lv_obs_erg_s_Hz = blackbody_nu(lambda_um * u.um, T_dust * u.K)
        print(cal_Lv_obs_erg_s_Hz)