# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_galaxy_luminosity_function.py
# Compiled at: 2019-09-30 21:19:34
# Size of source mod 2**32: 8623 bytes
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

    def Schechter_Function_for_LF(L, L_character, Phi_character, alpha):
        Phi_Schechter = Phi_character * (L / L_character) ** alpha * np.exp(-(L / L_character))
        return Phi_Schechter


    def Saunders_Function_for_LF(L, L_character, Phi_character, alpha, sigma):
        Phi_Saunders = Phi_character * (L / L_character) ** (1 - alpha) * np.exp(-1.0 / (2.0 * sigma ** 2) * np.log10(1.0 + L / L_character) ** 2)
        return Phi_Saunders


    def calc_radio_LF_Novak2017(z, lgL=None, galaxy_type='SFG'):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        if type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
        else:
            if galaxy_type not in ('ALL', 'SFG', 'QG'):
                raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
            elif lgL is None:
                lgL_grid = np.linspace(18.0, 25.0, num=1000, endpoint=True)
            else:
                lgL_grid = lgL
            L_grid = 10 ** lgL_grid
            L_character = 1.85e+21
            Phi_character = 0.00355
            alpha = 1.22
            sigma = 0.63
            LF_zmin = 0.0
            LF_zmax = +np.inf
            if z < LF_zmin or z > LF_zmax:
                raise ValueError('calc_radio_LF_Novak2017: The input redshift is out of the allowed range of %s -- %s!' % (LF_zmin, LF_zmax))
            alphaL = 3.16
            betaL = -0.32
            L_grid_z = L_grid / (1.0 + z) ** (alphaL + z * betaL)
            Phi = Saunders_Function_for_LF(L_grid_z, L_character, Phi_character, alpha, sigma)
            lgPhi = np.log10(Phi)
            if lgL is None:
                return (
                 lgL_grid, lgPhi)
            return lgPhi


    def calc_IR_250um_LF_Koprowski2017(z, lgL=None, galaxy_type='SFG'):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        if type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
        else:
            if galaxy_type not in ('ALL', 'SFG', 'QG'):
                raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
            elif lgL is None:
                lgL_grid = np.linspace(24.0, 27.0, num=1000, endpoint=True)
            else:
                lgL_grid = lgL
            L_grid = 10 ** lgL_grid
            table_z_lower = [
             0.5, 1.5, 2.5, 3.5]
            table_z_upper = [1.5, 2.5, 3.5, 4.5]
            table_lgL_character = [25.2, 25.4, 25.63, 25.84]
            table_lgPhi_character = [-2.88, -3.03, -3.73, -4.59]
            alpha = -0.4
            LF_zmin = table_z_lower[0]
            LF_zmax = table_z_upper[(-1)]
            if z < LF_zmin or z > LF_zmax:
                raise ValueError('calc_IR_250um_LF_Koprowski2017: The input redshift is out of the allowed range of %s -- %s!' % (LF_zmin, LF_zmax))
            Phi = None
            lgPhi = None
            for i in range(len(table_z_upper)):
                if z >= table_z_lower[i] and z <= table_z_upper[i]:
                    L_character = 10 ** table_lgL_character[i]
                    Phi_character = 10 ** table_lgPhi_character[i]
                    Phi = Schechter_Function_for_LF(L_grid, L_character, Phi_character, alpha)
                    lgPhi = np.log10(Phi)
                    break

            if lgL is None:
                return (
                 lgL_grid, lgPhi)
            return lgPhi


    def calc_IR_LF_Gruppioni2013(z, lgL=None, galaxy_type='SFG'):
        if not np.isscalar(z):
            raise ValueError('Please input a float number as the redshift!')
        if type(galaxy_type) is not str:
            raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
        else:
            if galaxy_type not in ('ALL', 'SFG', 'QG'):
                raise ValueError('Please input either "ALL", "SFG" or "QG" as the galaxy_type!')
            elif lgL is None:
                lgL_grid = np.linspace(8.0, 14.0, num=1000, endpoint=True)
            else:
                lgL_grid = lgL
            L_grid = 10 ** lgL_grid
            table_data = [
             [
              0.0, 0.3, 1.15, 0.52, 10.12, -2.29],
             [
              0.3, 0.45, 1.2, 0.5, 10.41, -2.31],
             [
              0.45, 0.6, 1.2, 0.5, 10.55, -2.35],
             [
              0.6, 0.8, 1.2, 0.5, 10.71, -2.35],
             [
              0.8, 1.0, 1.2, 0.5, 10.97, -2.4],
             [
              1.0, 1.2, 1.2, 0.5, 11.13, -2.43],
             [
              1.2, 1.7, 1.2, 0.5, 11.37, -2.7],
             [
              1.7, 2.0, 1.2, 0.5, 11.5, -3.0],
             [
              2.0, 2.5, 1.2, 0.5, 11.6, -3.01],
             [
              2.5, 3.0, 1.2, 0.5, 11.92, -3.27],
             [
              3.0, 4.2, 1.2, 0.5, 11.9, -3.74]]
            table_data = np.array(table_data).T
            table_z_lower = table_data[0]
            table_z_upper = table_data[1]
            table_alpha = table_data[2]
            table_sigma = table_data[3]
            table_lgL_character = table_data[4]
            table_lgPhi_character = table_data[5]
            LF_zmin = table_z_lower[0]
            LF_zmax = table_z_upper[(-1)]
            if z < LF_zmin or z > LF_zmax:
                raise ValueError('calc_IR_LF_Gruppioni2013: The input redshift is out of the allowed range of %s -- %s!' % (LF_zmin, LF_zmax))
            Phi = None
            lgPhi = None
            for i in range(len(table_z_upper)):
                if z >= table_z_lower[i] and z <= table_z_upper[i]:
                    L_character = 10 ** table_lgL_character[i]
                    Phi_character = 10 ** table_lgPhi_character[i]
                    alpha = table_alpha[i]
                    sigma = table_sigma[i]
                    Phi = Saunders_Function_for_LF(L_grid, L_character, Phi_character, alpha, sigma)
                    lgPhi = np.log10(Phi)
                    break

            if lgL is None:
                return (
                 lgL_grid, lgPhi)
            return lgPhi