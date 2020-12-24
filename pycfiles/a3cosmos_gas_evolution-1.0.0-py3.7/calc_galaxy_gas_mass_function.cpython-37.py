# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_galaxy_gas_mass_function.py
# Compiled at: 2019-07-18 22:30:15
# Size of source mod 2**32: 3687 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
from numpy import log, log10, power, sum, sqrt, pi, exp
pow = power
lg = log10
ln = log
from scipy.interpolate import InterpolatedUnivariateSpline, interp1d
if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import apply_cosmology
cosmo = apply_cosmology.cosmo
if sys.version_info.major >= 3:
    long = int
else:

    def Schechter_Function(lgM, phi, lg_M0, alpha):
        lgx = lgM - lg_M0
        Phi_Schechter = phi * 10 ** (lgx * (alpha + 1)) * np.exp(-10 ** lgx) * ln(10)
        return Phi_Schechter


    def calc_CO10_LF_Saintonge2017(lgMgas=None, input_type=1):
        if lgMgas is None:
            lgMgas_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
        else:
            lgMgas_grid = lgMgas
        tb = Table.read((os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables/datatables_GMF/datatable_Saintonge2017_CO10_LF_%s.txt' % input_type), format='ascii')
        GMF_zmin = np.min(tb['zLo'])
        GMF_zmax = np.max(tb['zHi'])
        GMF_lgMchar = tb['lgLchar'][0]
        GMF_phi_1 = tb['Phi_1'][0]
        GMF_alpha_1 = tb['alpha_1'][0]
        GMF_Phi_L_Prime_CO10 = Schechter_Function(lgMgas_grid, GMF_phi_1, GMF_lgMchar, GMF_alpha_1)
        lgPhiMgas_grid = np.log10(GMF_Phi_L_Prime_CO10)
        lgPhiMgas_grid[np.isnan(lgPhiMgas_grid)] = -100
        lgPhiMgas_grid[lgPhiMgas_grid < -100] = -100
        if lgMgas is None:
            return (
             lgMgas_grid, lgPhiMgas_grid)
        return lgPhiMgas_grid


    def calc_CO10_LF_Saintonge2017_updated(lgMgas=None, input_type=1):
        if lgMgas is None:
            lgMgas_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
        else:
            lgMgas_grid = lgMgas
        tb = Table.read((os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables/datatables_GMF/datatable_Saintonge2017_CO10_LF_%s_updated.txt' % input_type), format='ascii')
        GMF_zmin = np.min(tb['zLo'])
        GMF_zmax = np.max(tb['zHi'])
        GMF_lgMchar = tb['lgLchar'][0]
        GMF_phi_1 = tb['Phi_1'][0]
        GMF_alpha_1 = tb['alpha_1'][0]
        GMF_Phi_L_Prime_CO10 = Schechter_Function(lgMgas_grid, GMF_phi_1, GMF_lgMchar, GMF_alpha_1)
        lgPhiMgas_grid = np.log10(GMF_Phi_L_Prime_CO10)
        lgPhiMgas_grid[np.isnan(lgPhiMgas_grid)] = -100
        lgPhiMgas_grid[lgPhiMgas_grid < -100] = -100
        if lgMgas is None:
            return (
             lgMgas_grid, lgPhiMgas_grid)
        return lgPhiMgas_grid