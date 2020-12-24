# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_galaxy_size_evolution.py
# Compiled at: 2019-07-18 22:30:15
# Size of source mod 2**32: 816 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
from numpy import log10, power as pow
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:

    def calc_galaxy_size_Tacconi2018(z, Mstar):
        Re0 = 8.9 * (1.0 + z) ** (-0.75) * (Mstar / 50000000000.0) ** 0.23
        return Re0