# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_dust_opacity_kappa.py
# Compiled at: 2019-07-18 22:30:15
# Size of source mod 2**32: 845 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
if sys.version_info.major >= 3:
    long = int
else:
    if __name__ == '__main__':
        if len(sys.argv) <= 1:
            print('Usage: ')
            print('calc_dust_opacity_kappa.py lambda_um')
            print('')
            sys.exit()
        else:
            lambda_um = float(sys.argv[1])
            if lambda_um >= 700.0:
                beta = 1.68
            else:
                beta = 2.0
        kappa_ = 0.596 * (lambda_um / 700.0) ** (-beta)
        print(kappa_, '[cm^2 g^{-1}]')