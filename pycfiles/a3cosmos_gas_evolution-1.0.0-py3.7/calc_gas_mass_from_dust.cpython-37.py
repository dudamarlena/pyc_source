# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/Common_Python_Code/calc_gas_mass_from_dust.py
# Compiled at: 2019-10-25 11:04:02
# Size of source mod 2**32: 22050 bytes
from __future__ import print_function
import os, sys, re, json, time, astropy, numpy as np
from astropy.table import Table, Column, hstack
from copy import copy
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.27, Tcmb0=2.725)
if sys.version_info.major >= 3:
    long = int
else:

    def calc_Lv_from_flux_density(obs_flux_mJy, obs_wavelength_um, redshift):
        lumdist_Mpc = cosmo.luminosity_distance(redshift).value
        Lv = 4 * np.pi * lumdist_Mpc ** 2 * obs_flux_mJy / (1.0 + redshift) / 40.3197 / 1000000000.0
        Lv = Lv * 3.839e+33
        return Lv


    def calc_Lv_850um_from_RF_850um(RF_850um_mJy, redshift):
        lumdist_Mpc = cosmo.luminosity_distance(redshift).value
        vLv_850um = 4 * np.pi * lumdist_Mpc ** 2 * RF_850um_mJy / 40.3197 * 352.69700941176467
        Lv_850um = vLv_850um * 3.839e+33 / 352697009411.76465
        Lv_850um_2 = 1.19e+27 * (RF_850um_mJy / 1000.0) / (1.0 + redshift) * lumdist_Mpc ** 2
        print(Lv_850um, Lv_850um_2)
        return Lv_850um


    def calc_M_mol_Hughes2017(S_850um_mJy, redshift):
        Lv_850um_erg_s_Hz = calc_Lv_from_flux_density(S_850um_mJy, 850.0 * (1.0 + redshift), redshift)
        M_mol_Msun = np.power(10.0, np.log10(Lv_850um_erg_s_Hz) * 0.93 - 17.74)
        return M_mol_Msun


    def calc_M_total_gas_Hughes2017(S_850um_mJy, redshift):
        Lv_850um_erg_s_Hz = calc_Lv_from_flux_density(S_850um_mJy, 850.0 * (1.0 + redshift), redshift)
        M_total_gas_Msun = np.power(10.0, np.log10(Lv_850um_erg_s_Hz) * 0.86 - 15.38)
        return M_total_gas_Msun


    def calc_M_mol_Groves2015(obs_flux_mJy, obs_wavelength_um, redshift):
        Brent_W = np.array([70.0, 100.0, 160.0, 250.0, 350.0, 500.0])
        Brent_A = np.array([4.6, 3.27, 1.91, 1.17, 1.17, 1.44])
        Brent_B = np.array([0.5, 0.63, 0.78, 0.9, 0.9, 0.99])
        rest_wavelength_um = obs_wavelength_um / (1.0 + redshift)
        dL = cosmo.luminosity_distance(redshift).value
        Brent_log_M_mol_Msun = np.zeros((len(obs_flux_mJy), len(Brent_W)))
        for i in range(len(Brent_W)):
            A = Brent_A[i]
            B = Brent_B[i]
            vLv = 299792.458 / obs_wavelength_um * obs_flux_mJy * (4 * np.pi * dL ** 2) / 40.3197
            log_M_ISM_Msun = A + B * np.log10(vLv)
            Brent_log_M_mol_Msun[:, i] = log_M_ISM_Msun

        log_M_mol_Msun = []
        for i in range(len(obs_flux_mJy)):
            if rest_wavelength_um[i] >= np.min(Brent_W) and rest_wavelength_um[i] <= np.max(Brent_W):
                Brent_Interp = scipy.interpolate.interp1d(np.log10(Brent_W), Brent_log_M_mol_Msun[i, :])
                log_M_mol_Msun.append(Brent_Interp(np.log10(rest_wavelength_um[i])))
            else:
                log_M_mol_Msun.append(np.nan)

        M_mol_Msun = 10 ** np.array(log_M_mol_Msun)
        Schinnerer2016_A = 1.57 - 0.0008 * (rest_wavelength_um - 250.0)
        Schinnerer2016_B = 0.86 + 0.0006 * (rest_wavelength_um - 250.0)
        lgMH2_Schinnerer2016 = Schinnerer2016_A + Schinnerer2016_B * np.log10(vLv)
        return M_mol_Msun


    def calc_M_total_gas_Groves2015(obs_flux_mJy, obs_wavelength_um, redshift):
        Brent_W = np.array([70.0, 100.0, 160.0, 250.0, 350.0, 500.0])
        Brent_A = np.array([4.15, 3.62, 3.52, 3.17, 3.08, 3.19])
        Brent_B = np.array([0.55, 0.6, 0.61, 0.69, 0.74, 0.78])
        rest_wavelength_um = obs_wavelength_um / (1.0 + redshift)
        dL = cosmo.luminosity_distance(redshift).value
        Brent_log_M_mol_Msun = np.zeros((len(obs_flux_mJy), len(Brent_W)))
        for i in range(len(Brent_W)):
            A = Brent_A[i]
            B = Brent_B[i]
            vLv = 299792.458 / obs_wavelength_um * obs_flux_mJy * (4 * np.pi * dL ** 2) / 40.3197
            log_M_ISM_Msun = A + B * np.log10(vLv)
            Brent_log_M_mol_Msun[:, i] = log_M_ISM_Msun

        log_M_mol_Msun = []
        for i in range(len(obs_flux_mJy)):
            if rest_wavelength_um[i] >= np.min(Brent_W) and rest_wavelength_um[i] <= np.max(Brent_W):
                Brent_Interp = scipy.interpolate.interp1d(np.log10(Brent_W), Brent_log_M_mol_Msun[i, :])
                log_M_mol_Msun.append(Brent_Interp(np.log10(rest_wavelength_um[i])))
            else:
                log_M_mol_Msun.append(np.nan)

        M_mol_Msun = 10 ** np.array(log_M_mol_Msun)
        return M_mol_Msun


    def calc_M_mol_Scoville2017_RF(S_850um_mJy, redshift):
        Lv_850um_erg_s_Hz = calc_Lv_from_flux_density(S_850um_mJy, 850.0 * (1.0 + redshift), redshift)
        M_mol_Msun = Lv_850um_erg_s_Hz / 6.7e+19
        return M_mol_Msun


    def calc_M_mol_Scoville2017(obs_flux_mJy, obs_wavelength_um, redshift):
        Lv_obs_erg_s_Hz = calc_Lv_from_flux_density(obs_flux_mJy, obs_wavelength_um, redshift)
        beta = 1.8
        Tdust = 25.0
        cal_Lv_obs_erg_s_Hz = blackbody_nu(obs_wavelength_um / (1.0 + redshift) * u.um, Tdust * u.K) * np.power(299792.458 / (obs_wavelength_um / (1.0 + redshift)), beta)
        cal_Lv_850um_erg_s_Hz = blackbody_nu(850.0 * u.um, 25.0 * u.K) * np.power(352.69700941176467, beta)
        Lv_850um_erg_s_Hz = Lv_obs_erg_s_Hz * (cal_Lv_850um_erg_s_Hz / cal_Lv_obs_erg_s_Hz)
        M_mol_Msun = Lv_850um_erg_s_Hz / 6.7e+19
        return M_mol_Msun


    def calc_gas_mass_from_dust_continuum(obs_wavelength_um, obs_flux_mJy, SED_flux_at_obs_wavelength=None, SED_flux_at_rest_850um=None, z=None, method='Hughes2017'):
        if obs_wavelength_um is None:
            raise ValueError("Error! Please input 'obs_wavelength_um' for calc_gas_mass_from_dust_continuum_with_band_conversion()!")
        elif obs_flux_mJy is None:
            raise ValueError("Error! Please input 'obs_flux_mJy' for calc_gas_mass_from_dust_continuum_with_band_conversion()!")
        elif z is None:
            raise ValueError("Error! Please input 'z' for calc_gas_mass_from_dust_continuum_with_band_conversion()!")
        else:
            allowed_methods = ['Hughes2017', 'Groves2015', 'Scoville2017']
            if method == 'Hughes2017' and not SED_flux_at_obs_wavelength is None:
                if SED_flux_at_rest_850um is None:
                    raise ValueError('Error! Please input \'SED_flux_at_obs_wavelength\' and \'SED_flux_at_rest_850um\' for calc_gas_mass_from_dust_continuum_with_band_conversion() with method "Hughes2017"!')
                M_mol_gas = calc_M_mol_Hughes2017(SED_flux_at_rest_850um / SED_flux_at_obs_wavelength * obs_flux_mJy, z)
            else:
                if method == 'Groves2015':
                    M_mol_gas = calc_M_mol_Groves2015(obs_flux_mJy, obs_wavelength_um, z)
                else:
                    if method == 'Scoville2017':
                        M_mol_gas = calc_M_mol_Scoville2017(obs_flux_mJy, obs_wavelength_um, z)
                    else:
                        raise NotImplementedError('Sorry! The gas mass calibration has not been implemented for the method "%s"! We have following methods: %s' % (method, allowed_methods))
        return (
         M_mol_gas, method)


    def calc_molecular_hydrogen_fraction(metalZOH, U_MW=None, method='Krumholz2009'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.append(script_dir)
        else:
            import inspect
            allowed_methods = [
             'Krumholz2009', 'Dave2016', 'Popping2014']
            if re.match('.*\\bKrumholz2009\\b.*', method, re.IGNORECASE):
                if 'calc_fmol_from_metalZ_following_Krumholz2009' not in dir():
                    from calc_fmol import calc_fmol_from_metalZ_following_Krumholz2009
                f_mol = calc_fmol_from_metalZ_following_Krumholz2009(metalZOH)
            else:
                if re.match('.*\\bDave2016\\b.*', method, re.IGNORECASE):
                    if 'calc_fmol_from_metalZ_following_Dave2016' not in dir():
                        from calc_fmol import calc_fmol_from_metalZ_following_Dave2016
                    f_mol = calc_fmol_from_metalZ_following_Dave2016(metalZOH)
                else:
                    if re.match('.*\\bPopping2014\\b.*', method, re.IGNORECASE):
                        if 'calc_fmol_from_metalZ_following_Popping2014' not in dir():
                            from calc_fmol import calc_fmol_from_metalZ_following_Popping2014
                        f_mol = calc_fmol_from_metalZ_following_Popping2014(metalZOH, U_MW=U_MW)
                    else:
                        raise NotImplementedError('Sorry! The molecular hydrogen fraction calculation has not been implemented for the method "%s"! We have following methods: %s' % (method, allowed_methods))
        return f_mol


    def calc_gas_mass_from_dust_mass(M_dust, M_star=None, SFR=None, metallicity=None, GDR=None, z=None, method=''):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.append(script_dir)
        M_total_gas = None
        M_mol_gas = None
        allowed_methods = [
         'Magdis2012', 'Genzel2015a', 'Genzel2015b', 'GDR']
        if method == '' and GDR is not None:
            method = 'GDR'
        else:
            if method == '':
                method = 'default'
            elif re.match('.*\\bMagdis2012\\b.*', method, re.IGNORECASE):
                if metallicity is None:
                    if M_star is None or SFR is None:
                        raise ValueError('Error! Please input \'M_star\' and \'SFR\' or \'metallicity\' for calc_gas_mass_from_dust_mass() with the method "Magdis2012"!')
                    else:
                        if 'calc_metalZ_from_FMR_following_Mannucci2010' not in dir():
                            from calc_metal_Z import calc_metalZ_from_FMR_following_Mannucci2010
                        metallicity = calc_metalZ_from_FMR_following_Mannucci2010(M_star, SFR)
                        method += ', lgMstar=%.2f, SFR=%g, [Mannucci2010] metallicity=%.2f' % (np.log10(M_star), SFR, metallicity)
                else:
                    method += ', metallicity=%.2f' % metallicity
                if GDR is None:
                    if 'calc_deltaGD_from_metalZ_following_Magdis2012' not in dir():
                        from calc_delta_GD import calc_deltaGD_from_metalZ_following_Magdis2012
                    GDR = calc_deltaGD_from_metalZ_following_Magdis2012(metallicity)
                    method += ', [Magdis2012] GDR=%.2f' % GDR
                else:
                    method += ', GDR=%.2f' % GDR
                M_mol_gas = M_dust * GDR
                if method.find('+') >= 0:
                    f_mol = calc_molecular_hydrogen_fraction(metallicity, method=method)
                    M_total_gas = M_mol_gas
                    M_mol_gas = M_total_gas * f_mol
            elif re.match('.*\\bGenzel2015a\\b.*', method, re.IGNORECASE):
                if metallicity is None:
                    if not M_star is None:
                        if SFR is None or z is None:
                            raise ValueError('Error! Please input (\'M_star\' and \'SFR\' and \'z\') or \'metallicity\' for calc_gas_mass_from_dust_mass() with the method "Genzel2015a"!')
                    else:
                        if 'calc_metalZ_from_FMR_following_Genzel2015a' not in dir():
                            from calc_metal_Z import calc_metalZ_from_FMR_following_Genzel2015a
                        metallicity = calc_metalZ_from_FMR_following_Genzel2015a(M_star, SFR, z)
                        method += ', lgMstar=%.2f, SFR=%g, z=%g, [Genzel2015a] metallicity=%.2f' % (np.log10(M_star), SFR, z, metallicity)
                else:
                    method += ', metallicity=%.2f' % metallicity
                if GDR is None:
                    if 'calc_deltaGD_from_metalZ_following_Genzel2015' not in dir():
                        from calc_delta_GD import calc_deltaGD_from_metalZ_following_Genzel2015
                    GDR = calc_deltaGD_from_metalZ_following_Genzel2015(metallicity)
                    method += ', [Genzel2015] GDR=%.2f' % GDR
                else:
                    method += ', GDR=%.2f' % GDR
                M_mol_gas = M_dust * GDR
                if method.find('+') >= 0:
                    f_mol = calc_molecular_hydrogen_fraction(metallicity, method=method)
                    M_total_gas = M_mol_gas
                    M_mol_gas = M_total_gas * f_mol
            else:
                if re.match('.*\\b(Genzel2015b|Genzel2015)\\b.*', method, re.IGNORECASE):
                    if metallicity is None:
                        if M_star is None or SFR is None:
                            raise ValueError('Error! Please input (\'M_star\' and \'SFR\') or \'metallicity\' for calc_gas_mass_from_dust_mass() with the method "Genzel2015b"!')
                else:
                    if 'calc_metalZ_from_FMR_following_Genzel2015b' not in dir():
                        from calc_metal_Z import calc_metalZ_from_FMR_following_Genzel2015b
                    metallicity = calc_metalZ_from_FMR_following_Genzel2015b(M_star, SFR)
                    method += ', lgMstar=%.2f, SFR=%g, [Genzel2015b] metallicity=%.2f' % (np.log10(M_star), SFR, metallicity)
                if GDR is None:
                    if 'calc_deltaGD_from_metalZ_following_Genzel2015' not in dir():
                        from calc_delta_GD import calc_deltaGD_from_metalZ_following_Genzel2015
                    GDR = calc_deltaGD_from_metalZ_following_Genzel2015(metallicity)
                    method += ', [Genzel2015] GDR=%.2f' % GDR
                else:
                    method += ', GDR=%.2f' % GDR
                M_mol_gas = M_dust * GDR
                if method.find('+') >= 0:
                    f_mol = calc_molecular_hydrogen_fraction(metallicity, method=method)
                    M_total_gas = M_mol_gas
                    M_mol_gas = M_total_gas * f_mol
                else:
                    if re.match('.*\\b(default)\\b.*', method, re.IGNORECASE):
                        if metallicity is None:
                            if not M_star is None:
                                if SFR is None or z is None:
                                    raise ValueError('Error! Please input (\'M_star\' and \'SFR\' and \'z\') or \'metallicity\' for calc_gas_mass_from_dust_mass() with the method "default"!')
                            else:
                                if 'calc_metalZ_from_FMR_following_Genzel2015ab_combined_by_dzliu' not in dir():
                                    from calc_metal_Z import calc_metalZ_from_FMR_following_Genzel2015ab_combined_by_dzliu
                                metallicity = calc_metalZ_from_FMR_following_Genzel2015ab_combined_by_dzliu(M_star, SFR, z)
                                method += ', lgMstar=%.2f, SFR=%g, [Genzel2015abcomb] metallicity=%.2f' % (np.log10(M_star), SFR, metallicity)
                        else:
                            method += ', metallicity=%.2f' % metallicity
                        if GDR is None:
                            if 'calc_deltaGD_from_metalZ_following_RemyRuyer2014b' not in dir():
                                from calc_delta_GD import calc_deltaGD_from_metalZ_following_RemyRuyer2014b
                            GDR = calc_deltaGD_from_metalZ_following_RemyRuyer2014b(metallicity)
                            method += ', [RemyRuyer2014b] GDR=%.2f' % GDR
                        else:
                            method += ', GDR=%.2f' % GDR
                        M_mol_gas = M_dust * GDR
                        if method.find('+') >= 0:
                            f_mol = calc_molecular_hydrogen_fraction(metallicity, method=method)
                            M_total_gas = M_mol_gas
                            M_mol_gas = M_total_gas * f_mol
                    elif re.match('.*\\bGDR\\b.*', method, re.IGNORECASE):
                        if GDR is None:
                            raise ValueError('Error! Please input \'GDR\' for calc_gas_mass_from_dust_mass() with the method "GDR"!')
                        else:
                            method += ', GDR=%.2f' % GDR
                        M_mol_gas = M_dust * GDR
                        if method.find('+') >= 0:
                            f_mol = calc_molecular_hydrogen_fraction(metallicity, method=method)
                            M_total_gas = M_mol_gas
                            M_mol_gas = M_total_gas * f_mol
                    else:
                        raise NotImplementedError('Sorry! The gas mass calibration has not been implemented for the method "%s"! We have following methods: %s' % (method, allowed_methods))
            if M_total_gas is None:
                return (
                 M_mol_gas, method)
            return (M_mol_gas, M_total_gas, method)