# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_galaxy_stellar_mass_function.py
# Compiled at: 2019-10-24 23:34:24
# Size of source mod 2**32: 25467 bytes
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


    def calc_SMF_Davidzon2017(z, lgMstar=None, galaxy_type='SFG'):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        if type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
        else:
            if galaxy_type not in ('ALL', 'SFG', 'QG'):
                raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
            else:
                if lgMstar is None:
                    lgMstar_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
                else:
                    lgMstar_grid = lgMstar
                tb_SMF = Table.read((os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables/datatables_SMF/datatable_Davidzon2017_SMF_' + galaxy_type + '.txt'), format='ascii')
                SMF_zmin = np.min(tb_SMF['zLo'])
                SMF_zmax = np.max(tb_SMF['zHi'])
                if not z < SMF_zmin:
                    if z > SMF_zmax:
                        raise ValueError('calc_SMF_Davidzon2017: The input redshift is out of the allowed range of %s -- %s!' % (SMF_zmin, SMF_zmax))
                    lgPhiMstar_matrix = []
                    for k in range(len(tb_SMF)):
                        SMF_z = (tb_SMF['zLo'][k] + tb_SMF['zHi'][k]) / 2.0
                        SMF_phi_1 = tb_SMF['Phi_1'][k]
                        SMF_phi_2 = tb_SMF['Phi_2'][k]
                        SMF_alpha_1 = tb_SMF['alpha_1'][k]
                        SMF_alpha_2 = tb_SMF['alpha_2'][k]
                        SMF_lgMchar = tb_SMF['lgMchar'][k]
                        SMF_PhiMstar = Schechter_Function(lgMstar_grid, SMF_phi_1, SMF_lgMchar, SMF_alpha_1) + Schechter_Function(lgMstar_grid, SMF_phi_2, SMF_lgMchar, SMF_alpha_2)
                        lgPhiMstar_grid = np.log10(SMF_PhiMstar)
                        lgPhiMstar_matrix.append(copy(lgPhiMstar_grid))

                    SMF_z = (tb_SMF['zLo'].data + tb_SMF['zHi'].data) / 2.0
                    lgPhiMstar_matrix = np.array(lgPhiMstar_matrix)
                    if z <= np.min(SMF_z):
                        lgPhiMstar_grid = lgPhiMstar_matrix[0]
                elif z >= np.max(SMF_z):
                    lgPhiMstar_grid = lgPhiMstar_matrix[(-1)]
                else:
                    lgPhiMstar_grid = interp1d(SMF_z, lgPhiMstar_matrix, axis=0, kind='linear')(z)
            lgPhiMstar_grid[np.isnan(lgPhiMstar_grid)] = -100
            lgPhiMstar_grid[lgPhiMstar_grid < -100] = -100
            if lgMstar is None:
                return (
                 lgMstar_grid, lgPhiMstar_grid)
            return lgPhiMstar_grid


    def calc_SMF_Ilbert2013(z, lgMstar=None, galaxy_type='SFG'):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        if type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL" or "SFG" as the galaxy_type!')
        else:
            if galaxy_type not in ('ALL', 'SFG', 'QG'):
                raise ValueError('Please input either "ALL" or "SFG" as the galaxy_type!')
            else:
                if lgMstar is None:
                    lgMstar_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
                else:
                    lgMstar_grid = lgMstar
                tb_SMF = Table.read((os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables/datatables_SMF/datatable_Ilbert2013_SMF_' + galaxy_type + '.txt'), format='ascii')
                SMF_zmin = np.min(tb_SMF['zLo'])
                SMF_zmax = np.max(tb_SMF['zHi'])
                if not z < SMF_zmin:
                    if z > SMF_zmax:
                        raise ValueError('calc_SMF_Ilbert2013: The input redshift is out of the allowed range of %s -- %s!' % (SMF_zmin, SMF_zmax))
                    lgPhiMstar_matrix = []
                    for k in range(len(tb_SMF)):
                        SMF_z = (tb_SMF['zLo'][k] + tb_SMF['zHi'][k]) / 2.0
                        SMF_phi_1 = tb_SMF['Phi_1'][k]
                        SMF_phi_2 = tb_SMF['Phi_2'][k]
                        SMF_alpha_1 = tb_SMF['alpha_1'][k]
                        SMF_alpha_2 = tb_SMF['alpha_2'][k]
                        SMF_lgMchar = tb_SMF['lgMchar'][k]
                        SMF_PhiMstar = Schechter_Function(lgMstar_grid, SMF_phi_1, SMF_lgMchar, SMF_alpha_1) + Schechter_Function(lgMstar_grid, SMF_phi_2, SMF_lgMchar, SMF_alpha_2)
                        lgPhiMstar_grid = np.log10(SMF_PhiMstar)
                        lgPhiMstar_matrix.append(copy(lgPhiMstar_grid))

                    SMF_z = (tb_SMF['zLo'].data + tb_SMF['zHi'].data) / 2.0
                    lgPhiMstar_matrix = np.array(lgPhiMstar_matrix)
                    if z <= np.min(SMF_z):
                        lgPhiMstar_grid = lgPhiMstar_matrix[0]
                elif z >= np.max(SMF_z):
                    lgPhiMstar_grid = lgPhiMstar_matrix[(-1)]
                else:
                    lgPhiMstar_grid = interp1d(SMF_z, lgPhiMstar_matrix, axis=0, kind='linear')(z)
            lgPhiMstar_grid[np.isnan(lgPhiMstar_grid)] = -100
            lgPhiMstar_grid[lgPhiMstar_grid < -100] = -100
            if lgMstar is None:
                return (
                 lgMstar_grid, lgPhiMstar_grid)
            return lgPhiMstar_grid


    def calc_SMF_Peng2010(z, lgMstar=None, galaxy_type='SFG'):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        elif type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
        else:
            if galaxy_type not in ('SFG', 'QG'):
                raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
            elif lgMstar is None:
                lgMstar_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
            else:
                lgMstar_grid = lgMstar
            tb_SMF = Table.read((os.path.dirname(os.path.dirname(__file__)) + os.sep + 'Data_Tables/datatables_SMF/datatable_PengYingjie2010_SMF_' + galaxy_type + '.txt'), format='ascii')
            SMF_zmin = np.min(tb_SMF['zLo'])
            SMF_zmax = np.max(tb_SMF['zHi'])
            if not z < SMF_zmin:
                if z > SMF_zmax:
                    raise ValueError('calc_SMF_Peng2010: The input redshift is out of the allowed range of %s -- %s!' % (SMF_zmin, SMF_zmax))
                SMF_z = (tb_SMF['zLo'].data + tb_SMF['zHi'].data) / 2.0
                SMF_phi_1 = tb_SMF['Phi_1'].data
                SMF_alpha_1 = tb_SMF['alpha_1'].data
                SMF_lgMchar = tb_SMF['lgMchar'].data
                SMF_PhiMstar = Schechter_Function(lgMstar_grid, SMF_phi_1, SMF_lgMchar, SMF_alpha_1)
                if galaxy_type == 'SFG':
                    SMF_PhiMstar_SFG = copy(SMF_PhiMstar)
            else:
                SMF_phi_2 = tb_SMF['Phi_2'].data
            SMF_alpha_2 = tb_SMF['alpha_2'].data
            SMF_PhiMstar_SFG = copy(SMF_PhiMstar)
            SMF_PhiMstar_QG = SMF_PhiMstar_SFG + Schechter_Function(lgMstar_grid, SMF_phi_2, SMF_lgMchar, SMF_alpha_2)
            SMF_PhiMstar_ALL = SMF_PhiMstar_QG + SMF_PhiMstar_SFG
        if galaxy_type == 'SFG':
            lgPhiMstar_grid = np.log10(SMF_PhiMstar_SFG)
        else:
            if galaxy_type == 'QG':
                lgPhiMstar_grid = np.log10(SMF_PhiMstar_QG)
            else:
                if galaxy_type == 'ALL':
                    lgPhiMstar_grid = np.log10(SMF_PhiMstar_ALL)
                if lgMstar is None:
                    return (
                     lgMstar_grid, lgPhiMstar_grid)
                return lgPhiMstar_grid


    def calc_SMF_Wright2018_single_component(z, lgMstar=None):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        elif lgMstar is None:
            lgMstar_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
        else:
            lgMstar_grid = lgMstar
        SMF_lgMchar = 10.791 + 0.558 * z + -0.102 * z ** 2
        SMF_alpha = -1.16 + -0.274 * z + 0.028 * z ** 2
        SMF_phi = 10 ** (-2.455 + -0.883 * z + 0.093 * z ** 2)
        SMF_PhiMstar = Schechter_Function(lgMstar_grid, SMF_phi, SMF_lgMchar, SMF_alpha)
        lgPhiMstar_grid = np.log10(SMF_PhiMstar)
        if lgMstar is None:
            return (
             lgMstar_grid, lgPhiMstar_grid)
        return lgPhiMstar_grid


    def calc_SMF_Wright2018_double_component(z, lgMstar=None):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        elif lgMstar is None:
            lgMstar_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
        else:
            lgMstar_grid = lgMstar
        SMF_lgMchar = 10.831 + 0.153 * z + -0.033 * z ** 2
        SMF_alpha_1 = -0.579 + 0.048 * z + 0.022 * z ** 2
        SMF_alpha_2 = -1.489 + -0.087 * z + 0.016 * z ** 2
        SMF_phi_1 = 10 ** (-2.312 + -0.658 * z + 0.016 * z ** 2)
        SMF_phi_2 = 10 ** (-3.326 + -0.158 * z + -0.002 * z ** 2)
        SMF_PhiMstar = Schechter_Function(lgMstar_grid, SMF_phi_1, SMF_lgMchar, SMF_alpha_1) + Schechter_Function(lgMstar_grid, SMF_phi_2, SMF_lgMchar, SMF_alpha_2)
        lgPhiMstar_grid = np.log10(SMF_PhiMstar)
        if lgMstar is None:
            return (
             lgMstar_grid, lgPhiMstar_grid)
        return lgPhiMstar_grid


    def calc_Gladders2013_CSFRD(z, t0, tau):
        Gladders2013_t_age = cosmo.age(z).value
        Gladders2013_t0 = float(t0)
        Gladders2013_tau = float(tau)
        Gladders2013_SFR_1 = 1.0 / (Gladders2013_t_age * sqrt(2 * pi * Gladders2013_tau ** 2))
        Gladders2013_SFR_2 = exp(-(ln(Gladders2013_t_age) - Gladders2013_t0) ** 2 / (2 * Gladders2013_tau ** 2))
        Gladders2013_SFR = Gladders2013_SFR_1 * Gladders2013_SFR_2
        Gladders2013_SFR = Gladders2013_SFR / 1.64
        return Gladders2013_SFR


    def calc_MadauDickinson2014_CSFRD(z):
        if type(z) is list:
            z = np.array(z)
        rho_SFR = 0.015 * (1 + z) ** 2.7 / (1.0 + ((1 + z) / 2.9) ** 5.6) / 1.64
        return rho_SFR


    def calc_Mstar_integrating_CSFRD_dzliu2018(z):
        opz_list = np.logspace((np.log10(1.0)), (np.log10(11.75)), num=200, endpoint=True)
        opz_list = opz_list[::-1]
        z_list = opz_list - 1.0
        t_list = cosmo.age(z_list).value
        CSFRD = calc_MadauDickinson2014_CSFRD(z_list)
        Mstar_cumulated = 0.0
        CSFRD_z_list = [z_list[0]]
        CSFRD_Mstar_list = [1e-30]
        for i in range(len(z_list) - 1):
            t_bin = t_list[(i + 1)]
            time_bin = t_list[(i + 1)] - t_list[i]
            mass_loss_time_scale = 0.3
            Mstar_formed = (CSFRD[i] + CSFRD[(i + 1)]) / 2.0 * time_bin * 1000000000.0
            Mstar_loss_frac = 0.05 * ln(1.0 + t_bin / (mass_loss_time_scale * 0.001))
            Mstar_cumulated += Mstar_formed * (1.0 - Mstar_loss_frac)
            CSFRD_z_list.append(z_list[(i + 1)])
            CSFRD_Mstar_list.append(Mstar_cumulated)

        CSFRD_z_list = np.array(CSFRD_z_list)[::-1]
        CSFRD_Mstar_list = np.array(CSFRD_Mstar_list)[::-1]
        Mstar_cumulated_at_z = 10 ** InterpolatedUnivariateSpline(CSFRD_z_list, (np.log10(CSFRD_Mstar_list)), k=1)(z)
        return Mstar_cumulated_at_z


    def calc_SMF_dzliu2018(z=None, lgMstar=None, galaxy_type='SFG', z_list=None, tuning_params='', verbose=True):
        if z is not None:
            if not np.isscalar(z):
                if type(z) is list:
                    z = np.array(z)
                z_is_vector = True
            else:
                z_is_vector = False
        if type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
        else:
            if galaxy_type not in ('SFG', 'QG', 'ALL'):
                raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
            else:
                if lgMstar is None:
                    lgMstar_grid = np.linspace(6.0, 13.0, num=1000, endpoint=True)
                else:
                    lgMstar_grid = lgMstar
                if z_list is None:
                    z_list = np.arange(10.75, 1.0, -0.5).tolist()
                    z_list.extend([1.0, 0.75, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0])
                SMF_z_list = []
                SMF_Phi_list = []
                Mstar_cumulated_list = calc_Mstar_integrating_CSFRD_dzliu2018(z_list)
                for i in range(len(z_list) - 1):
                    z_bin = (z_list[i] + z_list[(i + 1)]) / 2.0
                    t_bin = cosmo.age(z_bin).value
                    Schechter_M = 10 ** lgMstar_grid
                    Schechter_Mstep = lgMstar_grid[1] - lgMstar_grid[0]
                    do_renorm_by_CSFRD_cumulated_Mstar = True
                    if z_bin < 0.02:
                        Schechter_P_QG = 10 ** calc_SMF_Peng2010(0.02, lgMstar=lgMstar_grid, galaxy_type='QG')
                        Schechter_P_SFG = 10 ** calc_SMF_Peng2010(0.02, lgMstar=lgMstar_grid, galaxy_type='SFG')
                    else:
                        if z_bin < 0.085:
                            Schechter_P_QG = 10 ** calc_SMF_Peng2010(z_bin, lgMstar=lgMstar_grid, galaxy_type='QG')
                            Schechter_P_SFG = 10 ** calc_SMF_Peng2010(z_bin, lgMstar=lgMstar_grid, galaxy_type='SFG')
                        else:
                            if z_bin < 0.2:
                                Schechter_P_QG = 10 ** calc_SMF_Peng2010(0.085, lgMstar=lgMstar_grid, galaxy_type='QG') * (1.0 - (0.115 - (0.2 - z_bin)) / 0.115) + 10 ** calc_SMF_Davidzon2017(0.2, lgMstar=lgMstar_grid, galaxy_type='QG') * (0.0 + (0.115 - (0.2 - z_bin)) / 0.115)
                                Schechter_P_SFG = 10 ** calc_SMF_Peng2010(0.085, lgMstar=lgMstar_grid, galaxy_type='SFG') * (1.0 - (0.115 - (0.2 - z_bin)) / 0.115) + 10 ** calc_SMF_Davidzon2017(0.2, lgMstar=lgMstar_grid, galaxy_type='SFG') * (0.0 + (0.115 - (0.2 - z_bin)) / 0.115)
                            else:
                                if z_bin < 4.0:
                                    Schechter_P_QG = 10 ** calc_SMF_Davidzon2017(z_bin, lgMstar=lgMstar_grid, galaxy_type='QG')
                                    Schechter_P_SFG = 10 ** calc_SMF_Davidzon2017(z_bin, lgMstar=lgMstar_grid, galaxy_type='SFG')
                                    if tuning_params is not None:
                                        if tuning_params.find('D17-no-renorm') >= 0:
                                            do_renorm_by_CSFRD_cumulated_Mstar = False
                                        else:
                                            Schechter_P_QG = 10 ** calc_SMF_Davidzon2017(4.0, lgMstar=lgMstar_grid, galaxy_type='QG')
                                            Schechter_P_SFG = 10 ** calc_SMF_Davidzon2017(4.0, lgMstar=lgMstar_grid, galaxy_type='SFG')
                                else:
                                    Mstar_cumulated = Mstar_cumulated_list[(i + 1)]
                                    if do_renorm_by_CSFRD_cumulated_Mstar:
                                        Schechter_M_total = sum((Schechter_P_QG + Schechter_P_SFG) * Schechter_M * Schechter_Mstep)
                                        renorm_factor = Mstar_cumulated / Schechter_M_total
                                        Schechter_P_SFG = Schechter_P_SFG * renorm_factor
                                        Schechter_P_QG = Schechter_P_QG * renorm_factor
                                    else:
                                        Schechter_P_ALL = Schechter_P_SFG + Schechter_P_QG
                                        if verbose:
                                            print('z = %.04f, lgMstar_CSFRD = %0.2f, lgMstar_SMF = %0.2f, renorm = %s' % (z_bin, np.log10(Mstar_cumulated), np.log10(Schechter_M_total), renorm_factor))
                                        SMF_z_list.append(z_list[(i + 1)])
                                        if galaxy_type == 'SFG':
                                            SMF_Phi_list.append(Schechter_P_SFG)
                                    if galaxy_type == 'QG':
                                        SMF_Phi_list.append(Schechter_P_QG)
                    if galaxy_type == 'ALL':
                        SMF_Phi_list.append(Schechter_P_ALL)

                SMF_z_list = np.array(SMF_z_list)[::-1]
                SMF_Phi_list = np.array(SMF_Phi_list)[::-1].T
                if z is None:
                    lgPhiMstar_matrix = np.log10(SMF_Phi_list.T)
                    return (SMF_z_list, lgMstar_grid, lgPhiMstar_matrix)
                    if z_is_vector:
                        lgPhiMstar_grid = interp1d(SMF_z_list, (np.log10(SMF_Phi_list)), kind='cubic')(z)
                else:
                    lgPhiMstar_grid = interp1d(SMF_z_list, (np.log10(SMF_Phi_list)), kind='cubic')(z)
            if lgMstar is None:
                return (
                 lgMstar_grid, lgPhiMstar_grid)
            return lgPhiMstar_grid