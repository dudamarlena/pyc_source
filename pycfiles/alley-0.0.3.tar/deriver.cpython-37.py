# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/deriver.py
# Compiled at: 2020-03-31 07:03:35
# Size of source mod 2**32: 43243 bytes
__doc__ = '\nCreated on Fri Sep 28 15:19:30 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli institute for Astrophysics and Space Research, \nMassachusetts institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import os, numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pickle
from corner import corner
from tqdm import tqdm
from astropy.constants import M_earth, M_jup, M_sun, R_earth, R_jup, R_sun, au
import copy
from multiprocessing import Pool
from contextlib import closing
from . import config
from utils.latex_printer import round_tex
from .general_output import logprint
import priors.simulate_PDF as simulate_PDF
from .computer import update_params, calculate_model
import exoworlds_rdx.lightcurves.index_transits as index_transits
companion = None
inst = None
samples2 = None
derived_samples = None

def calculate_values_from_model_curves(arg):
    global companion
    global derived_samples
    global inst
    i, p = arg
    _depth_tr_diluted_ = np.nan
    _depth_occ_diluted_ = np.nan
    _ampl_ellipsoidal_diluted_ = np.nan
    _ampl_sbratio_diluted_ = np.nan
    _ampl_geom_albedo_diluted_ = np.nan
    _ampl_gdc_diluted_ = np.nan
    width = np.median(derived_samples[(companion + '_T_tra_tot')]) / 24.0
    xx0 = np.linspace(p[(companion + '_epoch')] - 0.25 * p[(companion + '_period')], p[(companion + '_epoch')] + 0.75 * p[(companion + '_period')], 10001)
    ind_tr, ind_out = index_transits(xx0, p[(companion + '_epoch')], p[(companion + '_period')], width)
    xx = xx0[ind_tr]
    if len(xx) > 0:
        model = calculate_model(p, inst, 'flux', xx=xx)
        _depth_tr_diluted_ = (1.0 - np.min(model)) * 1000.0
    xx = xx0[ind_out]
    if config.BASEMENT.settings['secondary_eclipse'] is True:
        if len(xx) > 0:
            model_flux = calculate_model(p, inst, 'flux', xx=xx)
            if p[(companion + '_phase_curve_beaming_' + inst)] is not None:
                model_flux -= 0.001 * p[(companion + '_phase_curve_beaming_' + inst)] * np.sin(2.0 * np.pi / p[(companion + '_period')] * (xx - p[(companion + '_epoch')]))
            if p[(companion + '_phase_curve_atmospheric_' + inst)] is not None:
                model_flux -= 0.001 * p[(companion + '_phase_curve_atmospheric_' + inst)] * np.cos(2.0 * np.pi / p[(companion + '_period')] * (xx - p[(companion + '_epoch')]))
            if p[(companion + '_phase_curve_ellipsoidal_' + inst)] is not None:
                model_flux -= 0.001 * p[(companion + '_phase_curve_ellipsoidal_' + inst)] * np.cos(4.0 * np.pi / p[(companion + '_period')] * (xx - p[(companion + '_epoch')]))
            _depth_occ_diluted_ = (np.nanmax(model_flux) - np.nanmin(model_flux)) * 1000000.0
            if _depth_occ_diluted_ < 1e-07:
                _depth_occ_diluted_ = 0.0
    return [
     _depth_tr_diluted_, _depth_occ_diluted_, _ampl_ellipsoidal_diluted_, _ampl_sbratio_diluted_, _ampl_geom_albedo_diluted_, _ampl_gdc_diluted_]


def derive(samples, mode):
    """
    Derives parameter of the system using Winn 2010
    
    Input:
    ------
    samples : array
        samples from the mcmc or nested sampling
    mode : str
        'mcmc' or 'ns'
        
    Returns:
    --------
    derived_samples : dict 
        with keys 'i', 'R1a', 'R2a', 'k', 'depth_undiluted', 'b_tra', 'b_occ', 'Ttot', 'Tfull'
        each key contains all the samples derived from the MCMC samples 
        (not mean values, but pure samples!)
        i = inclination 
        R1a = R1/a, radius companion over semiamplitude
        R2a = R2/a, radius star over semiamplitude
        Ttot = T_{1-4}, total transit width 
        Tfull = T_{2-3}, full transit width
        
    Output:
    -------
    latex table of results
    corner plot of derived values posteriors
    """
    global companion
    global derived_samples
    global inst
    global samples2
    samples2 = samples
    N_samples = samples.shape[0]
    if os.path.exists(os.path.join(config.BASEMENT.datadir, 'params_star.csv')):
        buf = np.genfromtxt((os.path.join(config.BASEMENT.datadir, 'params_star.csv')), delimiter=',', names=True, dtype=None, encoding='utf-8', comments='#')
        star = {}
        star['R_star'] = simulate_PDF((buf['R_star']), (buf['R_star_lerr']), (buf['R_star_uerr']), size=N_samples, plot=False)
        star['M_star'] = simulate_PDF((buf['M_star']), (buf['M_star_lerr']), (buf['M_star_uerr']), size=N_samples, plot=False)
        star['Teff_star'] = simulate_PDF((buf['Teff_star']), (buf['Teff_star_lerr']), (buf['Teff_star_uerr']), size=N_samples, plot=False)
    else:
        star = {'R_star':np.nan, 
         'M_star':np.nan,  'Teff_star':np.nan}
    companions = config.BASEMENT.settings['companions_all']

    def get_params(key):
        ind = np.where(config.BASEMENT.fitkeys == key)[0]
        if len(ind) == 1:
            return samples[:, ind].flatten()
        try:
            if config.BASEMENT.params[key] is None:
                return np.nan
            return config.BASEMENT.params[key]
        except KeyError:
            return np.nan

    def sin_d(alpha):
        return np.sin(np.deg2rad(alpha))

    def cos_d(alpha):
        return np.cos(np.deg2rad(alpha))

    def arcsin_d(x):
        return np.rad2deg(np.arcsin(x))

    def arccos_d(x):
        return np.rad2deg(np.arccos(x))

    derived_samples = {}
    for cc in companions:
        companion = cc
        derived_samples[companion + '_R_star/a'] = get_params(companion + '_rsuma') / (1.0 + get_params(companion + '_rr'))
        derived_samples[companion + '_a/R_star'] = (1.0 + get_params(companion + '_rr')) / get_params(companion + '_rsuma')
        derived_samples[companion + '_R_companion/a'] = get_params(companion + '_rsuma') * get_params(companion + '_rr') / (1.0 + get_params(companion + '_rr'))
        derived_samples[companion + '_R_companion_(R_earth)'] = star['R_star'] * get_params(companion + '_rr') * R_sun.value / R_earth.value
        derived_samples[companion + '_R_companion_(R_jup)'] = star['R_star'] * get_params(companion + '_rr') * R_sun.value / R_jup.value
        derived_samples[companion + '_a_(R_sun)'] = star['R_star'] / derived_samples[(companion + '_R_star/a')]
        derived_samples[companion + '_a_(AU)'] = derived_samples[(companion + '_a_(R_sun)')] * R_sun.value / au.value
        derived_samples[companion + '_i'] = arccos_d(get_params(companion + '_cosi'))
        derived_samples[companion + '_e'] = get_params(companion + '_f_s') ** 2 + get_params(companion + '_f_c') ** 2
        derived_samples[companion + '_e_sinw'] = get_params(companion + '_f_s') * np.sqrt(derived_samples[(companion + '_e')])
        derived_samples[companion + '_e_cosw'] = get_params(companion + '_f_c') * np.sqrt(derived_samples[(companion + '_e')])
        derived_samples[companion + '_w'] = np.rad2deg(np.mod(np.arctan2(get_params(companion + '_f_s'), get_params(companion + '_f_c')), 2 * np.pi))
        if np.isnan(derived_samples[(companion + '_w')]).all():
            derived_samples[companion + '_w'] = 0.0
        if companion + '_K' in config.BASEMENT.params:
            a_1 = 0.019771142 * get_params(companion + '_K') * get_params(companion + '_period') * np.sqrt(1.0 - derived_samples[(companion + '_e')] ** 2) / sin_d(derived_samples[(companion + '_i')])
            derived_samples[companion + '_q'] = 1.0 / (derived_samples[(companion + '_a_(R_sun)')] / a_1 - 1.0)
            derived_samples[companion + '_M_companion_(M_earth)'] = derived_samples[(companion + '_q')] * star['M_star'] * M_sun.value / M_earth.value
            derived_samples[companion + '_M_companion_(M_jup)'] = derived_samples[(companion + '_q')] * star['M_star'] * M_sun.value / M_jup.value
        if config.BASEMENT.settings['secondary_eclipse'] is True:
            derived_samples[companion + '_epoch_occ'] = get_params(companion + '_epoch') + get_params(companion + '_period') / 2.0 * (1.0 + 4.0 / np.pi * derived_samples[(companion + '_e')] * cos_d(derived_samples[(companion + '_w')]))
        eccentricity_correction_b_tra = (1.0 - derived_samples[(companion + '_e')] ** 2) / (1.0 + derived_samples[(companion + '_e')] * sin_d(derived_samples[(companion + '_w')]))
        derived_samples[companion + '_b_tra'] = 1.0 / derived_samples[(companion + '_R_star/a')] * get_params(companion + '_cosi') * eccentricity_correction_b_tra
        eccentricity_correction_b_occ = (1.0 - derived_samples[(companion + '_e')] ** 2) / (1.0 - derived_samples[(companion + '_e')] * sin_d(derived_samples[(companion + '_w')]))
        if config.BASEMENT.settings['secondary_eclipse'] is True:
            derived_samples[companion + '_b_occ'] = 1.0 / derived_samples[(companion + '_R_star/a')] * get_params(companion + '_cosi') * eccentricity_correction_b_occ
        eccentricity_correction_T_tra = np.sqrt(1.0 - derived_samples[(companion + '_e')] ** 2) / (1.0 + derived_samples[(companion + '_e')] * sin_d(derived_samples[(companion + '_w')]))
        derived_samples[companion + '_T_tra_tot'] = get_params(companion + '_period') / np.pi * 24.0 * np.arcsin(derived_samples[(companion + '_R_star/a')] * np.sqrt((1.0 + get_params(companion + '_rr')) ** 2 - derived_samples[(companion + '_b_tra')] ** 2) / sin_d(derived_samples[(companion + '_i')])) * eccentricity_correction_T_tra
        derived_samples[companion + '_T_tra_full'] = get_params(companion + '_period') / np.pi * 24.0 * np.arcsin(derived_samples[(companion + '_R_star/a')] * np.sqrt((1.0 - get_params(companion + '_rr')) ** 2 - derived_samples[(companion + '_b_tra')] ** 2) / sin_d(derived_samples[(companion + '_i')])) * eccentricity_correction_T_tra
        for ii in config.BASEMENT.settings['inst_phot']:
            inst = ii
            N_less_samples = 1000
            derived_samples[companion + '_depth_tr_diluted_' + inst] = np.zeros(N_less_samples) * np.nan
            derived_samples[companion + '_depth_occ_diluted_' + inst] = np.zeros(N_less_samples) * np.nan
            derived_samples[companion + '_ampl_ellipsoidal_diluted_' + inst] = np.zeros(N_less_samples) * np.nan
            derived_samples[companion + '_ampl_sbratio_diluted_' + inst] = np.zeros(N_less_samples) * np.nan
            derived_samples[companion + '_ampl_geom_albedo_diluted_' + inst] = np.zeros(N_less_samples) * np.nan
            derived_samples[companion + '_ampl_gdc_diluted_' + inst] = np.zeros(N_less_samples) * np.nan
            logprint('\n' + inst + ' ' + companion + ': deriving eclipse depths and more from model curves...')
            args = []
            for i in range(N_less_samples):
                s = samples[np.random.randint(low=0, high=(samples2.shape[0])), :]
                p = update_params(s)
                args.append((i, p))

            with closing(Pool(processes=(config.BASEMENT.settings['multiprocess_cores']))) as (pool):
                results = list(tqdm((pool.imap(calculate_values_from_model_curves, args)), total=N_less_samples))
            for i in range(N_less_samples):
                derived_samples[(companion + '_depth_tr_diluted_' + inst)][i] = results[i][0]
                derived_samples[(companion + '_depth_occ_diluted_' + inst)][i] = results[i][1]
                derived_samples[(companion + '_ampl_ellipsoidal_diluted_' + inst)][i] = results[i][2]
                derived_samples[(companion + '_ampl_sbratio_diluted_' + inst)][i] = results[i][3]
                derived_samples[(companion + '_ampl_geom_albedo_diluted_' + inst)][i] = results[i][4]
                derived_samples[(companion + '_ampl_gdc_diluted_' + inst)][i] = results[i][5]

            derived_samples[companion + '_depth_tr_diluted_' + inst] = np.resize(derived_samples[(companion + '_depth_tr_diluted_' + inst)], N_samples)
            derived_samples[companion + '_depth_occ_diluted_' + inst] = np.resize(derived_samples[(companion + '_depth_occ_diluted_' + inst)], N_samples)
            derived_samples[companion + '_ampl_ellipsoidal_diluted_' + inst] = np.resize(derived_samples[(companion + '_ampl_ellipsoidal_diluted_' + inst)], N_samples)
            derived_samples[companion + '_ampl_sbratio_diluted_' + inst] = np.resize(derived_samples[(companion + '_ampl_sbratio_diluted_' + inst)], N_samples)
            derived_samples[companion + '_ampl_geom_albedo_diluted_' + inst] = np.resize(derived_samples[(companion + '_ampl_geom_albedo_diluted_' + inst)], N_samples)
            derived_samples[companion + '_ampl_gdc_diluted_' + inst] = np.resize(derived_samples[(companion + '_ampl_gdc_diluted_' + inst)], N_samples)

        for inst in config.BASEMENT.settings['inst_phot']:
            dil = get_params('light_3_' + inst)
            if np.isnan(dil):
                dil = 0
            derived_samples[companion + '_depth_tr_undiluted_' + inst] = derived_samples[(companion + '_depth_tr_diluted_' + inst)] / (1.0 - dil)
            derived_samples[companion + '_depth_occ_undiluted_' + inst] = derived_samples[(companion + '_depth_occ_diluted_' + inst)] / (1.0 - dil)
            derived_samples[companion + '_ampl_ellipsoidal_undiluted_' + inst] = derived_samples[(companion + '_ampl_ellipsoidal_diluted_' + inst)] / (1.0 - dil)
            derived_samples[companion + '_ampl_sbratio_undiluted_' + inst] = derived_samples[(companion + '_ampl_sbratio_diluted_' + inst)] / (1.0 - dil)
            derived_samples[companion + '_ampl_geom_albedo_undiluted_' + inst] = derived_samples[(companion + '_ampl_geom_albedo_diluted_' + inst)] / (1.0 - dil)
            derived_samples[companion + '_ampl_gdc_undiluted_' + inst] = derived_samples[(companion + '_ampl_gdc_diluted_' + inst)] / (1.0 - dil)

        albedo = 0.3
        emissivity = 1.0
        derived_samples[companion + '_Teq'] = star['Teff_star'] * ((1.0 - albedo) / emissivity) ** 0.25 * np.sqrt(derived_samples[(companion + '_R_star/a')] / 2.0)
        if companion in config.BASEMENT.settings['companions_phot']:
            derived_samples[companion + '_host_density'] = 3.0 * np.pi * (1.0 / derived_samples[(companion + '_R_star/a')]) ** 3.0 / (get_params(companion + '_period') * 86400.0) ** 2 / 6.67408e-08
        derived_samples[companion + '_density'] = (derived_samples[(companion + '_M_companion_(M_earth)')] * M_earth / (1.3333333333333333 * np.pi * (derived_samples[(companion + '_R_companion_(R_earth)')] * R_earth) ** 3)).cgs.value
        try:
            derived_samples[companion + '_surface_gravity'] = 2.0 * np.pi / (get_params(companion + '_period') * 86400.0) * np.sqrt(1.0 - derived_samples[(companion + '_e')] ** 2) * (get_params(companion + '_K') * 100000.0) / derived_samples[(companion + '_R_companion/a')] ** 2 / sin_d(derived_samples[(companion + '_i')])
        except:
            pass

        if len(companions) > 1:
            for other_companion in companions:
                if other_companion is not companion:
                    derived_samples[companion + '_period/' + other_companion + '_period'] = get_params(companion + '_period') / get_params(other_companion + '_period')

        for inst in config.BASEMENT.settings['inst_all']:
            if config.BASEMENT.settings[('host_ld_law_' + inst)] is None:
                continue
            if config.BASEMENT.settings[('host_ld_law_' + inst)] == 'lin':
                derived_samples['host_ldc_u1_' + inst] = get_params('host_ldc_q1_' + inst)
            elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'quad':
                derived_samples['host_ldc_u1_' + inst] = 2 * np.sqrt(get_params('host_ldc_q1_' + inst)) * get_params('host_ldc_q2_' + inst)
                derived_samples['host_ldc_u2_' + inst] = np.sqrt(get_params('host_ldc_q1_' + inst)) * (1.0 - 2.0 * get_params('host_ldc_q2_' + inst))
            elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'sing':
                raise ValueError('Sorry, I have not yet implemented the Sing limb darkening law.')
            else:
                print(config.BASEMENT.settings[('host_ld_law_' + inst)])
                raise ValueError("Currently only 'none', 'lin', 'quad' and 'sing' limb darkening are supported.")

    derived_samples['combined_host_density'] = []
    for companion in config.BASEMENT.settings['companions_phot']:
        derived_samples['combined_host_density'] = np.append(derived_samples['combined_host_density'], derived_samples[(companion + '_host_density')])

    names = []
    labels = []
    for companion in companions:
        names.append(companion + '_R_star/a')
        labels.append('$R_\\star/a_\\mathrm{' + companion + '}$')
        names.append(companion + '_a/R_star')
        labels.append('$a_\\mathrm{' + companion + '}/R_\\star$')
        names.append(companion + '_R_companion/a')
        labels.append('$R_\\mathrm{' + companion + '}/a_\\mathrm{' + companion + '}$')
        names.append(companion + '_R_companion_(R_earth)')
        labels.append('$R_\\mathrm{' + companion + '}$ ($\\mathrm{R_{\\oplus}}$)')
        names.append(companion + '_R_companion_(R_jup)')
        labels.append('$R_\\mathrm{' + companion + '}$ ($\\mathrm{R_{jup}}$)')
        names.append(companion + '_a_(R_sun)')
        labels.append('$a_\\mathrm{' + companion + '}$ ($\\mathrm{R_{\\odot}}$)')
        names.append(companion + '_a_(AU)')
        labels.append('$a_\\mathrm{' + companion + '}$ (AU)')
        names.append(companion + '_i')
        labels.append('$i_\\mathrm{' + companion + '}$ (deg)')
        names.append(companion + '_e')
        labels.append('$e_\\mathrm{' + companion + '}$')
        names.append(companion + '_w')
        labels.append('$w_\\mathrm{' + companion + '}$ (deg)')
        names.append(companion + '_M_companion_(M_earth)')
        labels.append('$M_\\mathrm{' + companion + '}$ ($\\mathrm{M_{\\oplus}}$)')
        names.append(companion + '_M_companion_(M_jup)')
        labels.append('$M_\\mathrm{' + companion + '}$ ($\\mathrm{M_{jup}}$)')
        names.append(companion + '_b_tra')
        labels.append('$b_\\mathrm{tra;' + companion + '}$')
        names.append(companion + '_T_tra_tot')
        labels.append('$T_\\mathrm{tot;' + companion + '}$ (h)')
        names.append(companion + '_T_tra_full')
        labels.append('$T_\\mathrm{full;' + companion + '}$ (h)')
        names.append(companion + '_b_occ')
        labels.append('$b_\\mathrm{occ;' + companion + '}$')
        names.append(companion + '_epoch_occ')
        labels.append('$T_\\mathrm{0;occ;' + companion + '}$')
        names.append(companion + '_host_density')
        labels.append('$rho_\\mathrm{\\star;' + companion + '}$ (cgs)')
        names.append(companion + '_density')
        labels.append('$rho_\\mathrm{' + companion + '}$ (cgs)')
        names.append(companion + '_surface_gravity')
        labels.append('$g_\\mathrm{\\star;' + companion + '}$ (cgs)')
        names.append(companion + '_Teq')
        labels.append('$T_\\mathrm{eq;' + companion + '}$ (K)')
        for inst in config.BASEMENT.settings['inst_phot']:
            names.append(companion + '_depth_tr_undiluted_' + inst)
            labels.append('$\\delta_\\mathrm{tr; undil; ' + companion + '; ' + inst + '}$ (ppt)')
            names.append(companion + '_depth_tr_diluted_' + inst)
            labels.append('$\\delta_\\mathrm{tr; dil; ' + companion + '; ' + inst + '}$ (ppt)')
            names.append(companion + '_depth_occ_undiluted_' + inst)
            labels.append('$\\delta_\\mathrm{occ; undil; ' + companion + '; ' + inst + '}$ (ppm)')
            names.append(companion + '_depth_occ_diluted_' + inst)
            labels.append('$\\delta_\\mathrm{occ; dil; ' + companion + '; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_ellipsoidal_undiluted_' + inst)
            labels.append('$A_\\mathrm{ellipsoidal; undil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_ellipsoidal_diluted_' + inst)
            labels.append('$A_\\mathrm{ellipsoidal; dil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_sbratio_undiluted_' + inst)
            labels.append('$A_\\mathrm{sbratio; undil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_sbratio_diluted_' + inst)
            labels.append('$A_\\mathrm{sbratio; dil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_geom_albedo_undiluted_' + inst)
            labels.append('$A_\\mathrm{geom. albedo; undil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_geom_albedo_diluted_' + inst)
            labels.append('$A_\\mathrm{geom. albedo; dil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_gdc_undiluted_' + inst)
            labels.append('$A_\\mathrm{grav. dark.; undil; ' + inst + '}$ (ppm)')
            names.append(companion + '_ampl_gdc_diluted_' + inst)
            labels.append('$A_\\mathrm{grav. dark.; dil; ' + inst + '}$ (ppm)')

        if len(companions) > 1:
            for other_companion in companions:
                if other_companion is not companion:
                    names.append(companion + '_period/' + other_companion + '_period')
                    labels.append('$P_\\mathrm{' + companion + '} / P_\\mathrm{' + other_companion + '}$')

    for inst in config.BASEMENT.settings['inst_all']:
        if config.BASEMENT.settings[('host_ld_law_' + inst)] is None:
            pass
        elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'lin':
            names.append('host_ldc_u1_' + inst)
            labels.append('Limb darkening $u_\\mathrm{1; ' + inst + '}$')
        elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'quad':
            names.append('host_ldc_u1_' + inst)
            labels.append('Limb darkening $u_\\mathrm{1; ' + inst + '}$')
            names.append('host_ldc_u2_' + inst)
            labels.append('Limb darkening $u_\\mathrm{2; ' + inst + '}$')
        elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'sing':
            raise ValueError('Sorry, I have not yet implemented the Sing limb darkening law.')
        else:
            print(config.BASEMENT.settings[('host_ld_law_' + inst)])
            raise ValueError("Currently only 'none', 'lin', 'quad' and 'sing' limb darkening are supported.")
        names.append(companion + '_ampl_gdc_diluted_' + inst)
        labels.append('$A_\\mathrm{grav. dark.; dil; ' + inst + '}$ (ppm)')

    names.append('combined_host_density')
    labels.append('$rho_\\mathrm{\\star; combined}$ (cgs)')
    ind_good = []
    for i, name in enumerate(names):
        if name in derived_samples and isinstance(derived_samples[name], np.ndarray):
            any(np.isnan(derived_samples[name])) or all(np.array(derived_samples[name]) == 0) or ind_good.append(i)

    names = [names[i] for i in ind_good]
    labels = [labels[i] for i in ind_good]
    if len(names) > 0:
        pickle.dump(derived_samples, open(os.path.join(config.BASEMENT.outdir, mode + '_derived_samples.pickle'), 'wb'))
        with open(os.path.join(config.BASEMENT.outdir, mode + '_derived_table.csv'), 'w') as (outfile):
            with open(os.path.join(config.BASEMENT.outdir, mode + '_derived_latex_table.txt'), 'w') as (f):
                with open(os.path.join(config.BASEMENT.outdir, mode + '_derived_latex_cmd.txt'), 'w') as (f_cmd):
                    outfile.write('#property,value,lower_error,upper_error,source\n')
                    f.write('Property & Value & Source \\\\ \n')
                    f.write('\\hline \n')
                    f.write('\\multicolumn{4}{c}{\\textit{Derived parameters}} \\\\ \n')
                    f.write('\\hline \n')
                    for name, label in zip(names, labels):
                        ll, median, ul = np.percentile(derived_samples[name], [15.865, 50.0, 84.135])
                        outfile.write(str(label) + ',' + str(median) + ',' + str(median - ll) + ',' + str(ul - median) + ',derived\n')
                        value = round_tex(median, median - ll, ul - median)
                        f.write(label + ' & $' + value + '$ & derived \\\\ \n')
                        simplename = name.replace('_', '').replace('/', 'over').replace('(', '').replace(')', '').replace('1', 'one').replace('2', 'two')
                        f_cmd.write('\\newcommand{\\' + simplename + '}{$' + value + '$} %' + label + ' = ' + value + '\n')

        logprint('\nSaved ' + mode + '_derived_results.csv, ' + mode + '_derived_latex_table.txt, and ' + mode + '_derived_latex_cmd.txt')
        if 'combined_host_density' in names:
            names.remove('combined_host_density')
        x = np.column_stack([derived_samples[name] for name in names])
        fontsize = np.min((24.0 + 0.5 * len(names), 40))
        fig = corner(x, range=([
         0.999] * len(names)),
          labels=names,
          quantiles=[
         0.15865, 0.5, 0.84135],
          show_titles=True,
          label_kwargs={'fontsize':fontsize, 
         'rotation':45,  'horizontalalignment':'right'},
          max_n_ticks=3)
        caxes = np.reshape(np.array(fig.axes), (len(names), len(names)))
        for i, name in enumerate(names):
            ll, median, ul = np.percentile(derived_samples[name], [15.865, 50.0, 84.135])
            value = round_tex(median, median - ll, ul - median)
            ctitle = '' + labels[i] + '\n' + '$=' + value + '$'
            if len(names) > 1:
                caxes[(i, i)].set_title(ctitle, fontsize=fontsize, rotation=45, horizontalalignment='left')
                for i in range(caxes.shape[0]):
                    for j in range(caxes.shape[1]):
                        caxes[(i, j)].xaxis.set_label_coords(0.5, -0.5)
                        caxes[(i, j)].yaxis.set_label_coords(-0.5, 0.5)
                        if i == caxes.shape[0] - 1:
                            fmt = ScalarFormatter(useOffset=False)
                            caxes[(i, j)].xaxis.set_major_formatter(fmt)
                        if i > 0:
                            if j == 0:
                                fmt = ScalarFormatter(useOffset=False)
                                caxes[(i, j)].yaxis.set_major_formatter(fmt)
                        for tick in caxes[(i, j)].xaxis.get_major_ticks():
                            tick.label.set_fontsize(24)

                        for tick in caxes[(i, j)].yaxis.get_major_ticks():
                            tick.label.set_fontsize(24)

            else:
                caxes.set_title(ctitle)
                caxes.xaxis.set_label_coords(0.5, -0.5)
                caxes.yaxis.set_label_coords(-0.5, 0.5)

        dpi = np.max((100.0 - len(names), 50))
        fig.savefig((os.path.join(config.BASEMENT.outdir, mode + '_derived_corner.jpg')), dpi=dpi, bbox_inches='tight')
        plt.close(fig)
        logprint('\nSaved ' + mode + '_derived_corner.pdf')
    else:
        logprint('\nNo values available to be derived.')