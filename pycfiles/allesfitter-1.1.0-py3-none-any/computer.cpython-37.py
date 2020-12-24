# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/computer.py
# Compiled at: 2020-03-31 06:02:46
# Size of source mod 2**32: 76476 bytes
"""
Created on Fri Oct  5 00:41:29 2018

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research, 
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109, 
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, ellc
from scipy.optimize import minimize
from scipy.interpolate import UnivariateSpline
import numpy.polynomial.polynomial as poly
import warnings
warnings.filterwarnings('ignore', category=(np.VisibleDeprecationWarning))
warnings.filterwarnings('ignore', category=(np.RankWarning))
warnings.filterwarnings('ignore', category=RuntimeWarning)
try:
    import celerite
    from celerite import terms
except ImportError:
    warnings.warn("Cannot import package 'celerite', thus 'hybrid_GP' baseline models will not be supported.")

from . import config
from flares.aflare import aflare1
from exoworlds_rdx.lightcurves.lightcurve_tools import calc_phase
GPs = [
 'sample_GP_real', 'sample_GP_complex', 'sample_GP_Matern32', 'sample_GP_SHO']
FCTs = ['none', 'offset', 'linear', 'hybrid_offset', 'hybrid_poly_0', 'hybrid_poly_1', 'hybrid_poly_2', 'hybrid_poly_3', 'hybrid_poly_4', 'hybrid_poly_5', 'hybrid_poly_6', 'hybrid_spline', 'sample_offset', 'sample_linear']

def divide(a, b):
    if a is not None:
        return 1.0 * a / b
    return


def update_params(theta):
    params = config.BASEMENT.params.copy()
    for i, key in enumerate(config.BASEMENT.fitkeys):
        params[key] = theta[i]

    for i, key in enumerate(config.BASEMENT.allkeys):
        if isinstance(config.BASEMENT.coupled_with[i], str) and len(config.BASEMENT.coupled_with[i]) > 0:
            params[key] = params[config.BASEMENT.coupled_with[i]]

    for companion in config.BASEMENT.settings['companions_all']:
        try:
            params[companion + '_incl'] = np.arccos(params[(companion + '_cosi')]) / np.pi * 180.0
        except:
            params[companion + '_incl'] = None

    for companion in config.BASEMENT.settings['companions_all']:
        try:
            params[companion + '_radius_1'] = params[(companion + '_rsuma')] / (1.0 + params[(companion + '_rr')])
            params[companion + '_radius_2'] = params[(companion + '_radius_1')] * params[(companion + '_rr')]
        except:
            params[companion + '_radius_1'] = None
            params[companion + '_radius_2'] = None

    for inst in config.BASEMENT.settings['inst_all']:
        if config.BASEMENT.settings[('host_ld_law_' + inst)] is None:
            params['host_ldc_' + inst] = None
        else:
            if config.BASEMENT.settings[('host_ld_law_' + inst)] == 'lin':
                params['host_ldc_' + inst] = params[('host_ldc_q1_' + inst)]
            else:
                if config.BASEMENT.settings[('host_ld_law_' + inst)] == 'quad':
                    ldc_u1 = 2.0 * np.sqrt(params[('host_ldc_q1_' + inst)]) * params[('host_ldc_q2_' + inst)]
                    ldc_u2 = np.sqrt(params[('host_ldc_q1_' + inst)]) * (1.0 - 2.0 * params[('host_ldc_q2_' + inst)])
                    params['host_ldc_' + inst] = [ldc_u1, ldc_u2]
                else:
                    if config.BASEMENT.settings[('host_ld_law_' + inst)] == 'sing':
                        raise ValueError('Sorry, I have not yet implemented the Sing limb darkening law.')
                    else:
                        print(config.BASEMENT.settings[('host_ld_law_' + inst)])
                        raise ValueError("Currently only 'none', 'lin', 'quad' and 'sing' limb darkening are supported.")
        for companion in config.BASEMENT.settings['companions_all']:
            if config.BASEMENT.settings[(companion + '_ld_law_' + inst)] is None:
                params[companion + '_ldc_' + inst] = None
            elif config.BASEMENT.settings[(companion + '_ld_law_' + inst)] == 'lin':
                params[companion + '_ldc_' + inst] = params[(companion + '_ldc_q1_' + inst)]
            elif config.BASEMENT.settings[(companion + '_ld_law_' + inst)] == 'quad':
                ldc_u1 = 2.0 * np.sqrt(params[(companion + '_ldc_q1_' + inst)]) * params[(companion + '_ldc_q2_' + inst)]
                ldc_u2 = np.sqrt(params[(companion + '_ldc_q1_' + inst)]) * (1.0 - 2.0 * params[(companion + '_ldc_q2_' + inst)])
                params[companion + '_ldc_' + inst] = [ldc_u1, ldc_u2]
            elif config.BASEMENT.settings[(companion + '_ld_law_' + inst)] == 'sing':
                raise ValueError('Sorry, I have not yet implemented the Sing limb darkening law.')
            else:
                print(config.BASEMENT.settings[(companion + '_ld_law_' + inst)])
                raise ValueError("Currently only 'none', 'lin', 'quad' and 'sing' limb darkening are supported.")

    for inst in config.BASEMENT.settings['inst_phot']:
        key = 'flux'
        params['err_' + key + '_' + inst] = np.exp(params[('log_err_' + key + '_' + inst)])

    for inst in config.BASEMENT.settings['inst_rv']:
        key = 'rv'
        params['jitter_' + key + '_' + inst] = np.exp(params[('log_jitter_' + key + '_' + inst)])

    for companion in config.BASEMENT.settings['companions_all']:
        ecc = params[(companion + '_f_s')] ** 2 + params[(companion + '_f_c')] ** 2
        try:
            a_1 = 0.019771142 * params[(companion + '_K')] * params[(companion + '_period')] * np.sqrt(1.0 - ecc ** 2) / np.sin(params[(companion + '_incl')] * np.pi / 180.0)
            params[companion + '_a'] = (1.0 + 1.0 / params[(companion + '_q')]) * a_1
        except:
            params[companion + '_a'] = None

        if params[(companion + '_a')] == 0.0:
            params[companion + '_a'] = None

    for companion in config.BASEMENT.settings['companions_all']:
        for inst in config.BASEMENT.settings['inst_all']:
            if config.BASEMENT.settings[('host_N_spots_' + inst)] > 0:
                params['host_spots_' + inst] = [[params[('host_spot_' + str(i) + '_long_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1)],
                 [params[('host_spot_' + str(i) + '_lat_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1)],
                 [params[('host_spot_' + str(i) + '_size_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1)],
                 [params[('host_spot_' + str(i) + '_brightness_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1)]]
            if config.BASEMENT.settings[(companion + '_N_spots_' + inst)] > 0:
                params[companion + '_spots_' + inst] = [[params[(companion + '_spot_' + str(i) + '_long_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1)],
                 [params[(companion + '_spot_' + str(i) + '_lat_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1)],
                 [params[(companion + '_spot_' + str(i) + '_size_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1)],
                 [params[(companion + '_spot_' + str(i) + '_brightness_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1)]]

    for companion in config.BASEMENT.settings['companions_phot']:
        if params[(companion + '_rr')] is not None and params[(companion + '_rr')] > 0 and params[(companion + '_rr')] < 0.215443469:
            params[companion + '_host_density'] = 3.0 * np.pi * (1.0 / params[(companion + '_radius_1')]) ** 3.0 / (params[(companion + '_period')] * 86400.0) ** 2 / 6.67408e-08
        else:
            params[companion + '_host_density'] = None

    for i, key in enumerate(config.BASEMENT.allkeys):
        if isinstance(config.BASEMENT.coupled_with[i], str) and len(config.BASEMENT.coupled_with[i]) > 0:
            params[key] = params[config.BASEMENT.coupled_with[i]]

    return params


def flux_fct(params, inst, companion, xx=None, settings=None):
    """
    ! params must be updated via update_params() before calling this function !
    
    if phased, pass e.g. xx=np.linspace(-0.25,0.75,1000) amd t_exp_scalefactor=1./params[companion+'_period']
    """
    if settings is None:
        settings = config.BASEMENT.settings
    if settings['fit_ttvs'] == False:
        return flux_fct_full(params, inst, companion, xx=xx, settings=settings)
    return flux_fct_piecewise(params, inst, companion, xx=xx, settings=settings)


def flux_fct_full(params, inst, companion, xx=None, settings=None):
    """
    ! params must be updated via update_params() before calling this function !
    
    if phased, pass e.g. xx=np.linspace(-0.25,0.75,1000) amd t_exp_scalefactor=1./params[companion+'_period']
    """
    if settings is None:
        settings = config.BASEMENT.settings
    else:
        if xx is None:
            xx = config.BASEMENT.data[inst]['time']
            t_exp = settings[('t_exp_' + inst)]
            n_int = settings[('t_exp_n_int_' + inst)]
        else:
            t_exp = None
            n_int = None
        if params[(companion + '_rr')] is not None and params[(companion + '_rr')] > 0:
            model_flux = ellc.lc(t_obs=xx,
              radius_1=(params[(companion + '_radius_1')]),
              radius_2=(params[(companion + '_radius_2')]),
              sbratio=(params[(companion + '_sbratio_' + inst)]),
              incl=(params[(companion + '_incl')]),
              light_3=(params[('dil_' + inst)] / (1.0 - params[('dil_' + inst)])),
              t_zero=(params[(companion + '_epoch')]),
              period=(params[(companion + '_period')]),
              a=(params[(companion + '_a')]),
              q=(params[(companion + '_q')]),
              f_c=(params[(companion + '_f_c')]),
              f_s=(params[(companion + '_f_s')]),
              ldc_1=(params[('host_ldc_' + inst)]),
              ldc_2=(params[(companion + '_ldc_' + inst)]),
              gdc_1=(params[('host_gdc_' + inst)]),
              gdc_2=(params[(companion + '_gdc_' + inst)]),
              didt=(params[('didt_' + inst)]),
              domdt=(params[('domdt_' + inst)]),
              rotfac_1=(params[('host_rotfac_' + inst)]),
              rotfac_2=(params[(companion + '_rotfac_' + inst)]),
              hf_1=(params[('host_hf_' + inst)]),
              hf_2=(params[(companion + '_hf_' + inst)]),
              bfac_1=(params[('host_bfac_' + inst)]),
              bfac_2=(params[(companion + '_bfac_' + inst)]),
              heat_1=(divide(params[('host_atmo_' + inst)], 2.0)),
              heat_2=(divide(params[(companion + '_atmo_' + inst)], 2.0)),
              lambda_1=(params[('host_lambda_' + inst)]),
              lambda_2=(params[(companion + '_lambda_' + inst)]),
              vsini_1=(params['host_vsini']),
              vsini_2=(params[(companion + '_vsini')]),
              t_exp=t_exp,
              n_int=n_int,
              grid_1=(settings[('host_grid_' + inst)]),
              grid_2=(settings[(companion + '_grid_' + inst)]),
              ld_1=(settings[('host_ld_law_' + inst)]),
              ld_2=(settings[(companion + '_ld_law_' + inst)]),
              shape_1=(settings[('host_shape_' + inst)]),
              shape_2=(settings[(companion + '_shape_' + inst)]),
              spots_1=(params[('host_spots_' + inst)]),
              spots_2=(params[(companion + '_spots_' + inst)]),
              exact_grav=(config.BASEMENT.settings['exact_grav']),
              verbose=False)
            if companion + '_thermal_emission_amplitude_' + inst in params and params[(companion + '_thermal_emission_amplitude_' + inst)] > 0:
                model_flux += calc_thermal_curve(params, inst, companion, xx, t_exp, n_int)
        else:
            model_flux = np.ones_like(xx)
    if params[(companion + '_phase_curve_beaming_' + inst)] is not None:
        model_flux += 0.001 * params[(companion + '_phase_curve_beaming_' + inst)] * np.sin(2.0 * np.pi / params[(companion + '_period')] * (xx - params[(companion + '_epoch')]))
    if params[(companion + '_phase_curve_atmospheric_' + inst)] is not None:
        model_flux += 0.001 * params[(companion + '_phase_curve_atmospheric_' + inst)] * np.cos(2.0 * np.pi / params[(companion + '_period')] * (xx - params[(companion + '_epoch')]))
    if params[(companion + '_phase_curve_ellipsoidal_' + inst)] is not None:
        model_flux += 0.001 * params[(companion + '_phase_curve_ellipsoidal_' + inst)] * np.cos(4.0 * np.pi / params[(companion + '_period')] * (xx - params[(companion + '_epoch')]))
    if settings['N_flares'] > 0:
        for i in range(1, settings['N_flares'] + 1):
            model_flux += aflare1(xx, (params[('flare_tpeak_' + str(i))]), (params[('flare_fwhm_' + str(i))]), (params[('flare_ampl_' + str(i))]), upsample=True, uptime=10)

    return model_flux


def flux_fct_piecewise(params, inst, companion, xx=None, settings=None):
    """
    Go through the time series transit by transit to fit for TTVs
    
    ! params must be updated via update_params() before calling this function !
    
    if phased, pass e.g. xx=np.linspace(-0.25,0.75,1000) amd t_exp_scalefactor=1./params[companion+'_period']
    """
    if settings is None:
        settings = config.BASEMENT.settings
    elif xx is None:
        model_flux = np.ones_like(config.BASEMENT.data[inst]['time'])
    else:
        model_flux = np.ones_like(xx)
    for n_transit in range(len(config.BASEMENT.data[(companion + '_tmid_observed_transits')])):
        if xx is None:
            ind = config.BASEMENT.data[inst][(companion + '_ind_time_transit_' + str(n_transit + 1))]
            xx_piecewise = config.BASEMENT.data[inst][(companion + '_time_transit_' + str(n_transit + 1))]
            t_exp = settings[('t_exp_' + inst)]
            n_int = settings[('t_exp_n_int_' + inst)]
        else:
            tmid = config.BASEMENT.data[(companion + '_tmid_observed_transits')][n_transit]
            width = settings['fast_fit_width']
            ind = np.where((xx >= tmid - width / 2.0) & (xx <= tmid + width / 2.0))[0]
            xx_piecewise = xx[ind]
            t_exp = None
            n_int = None
        if len(xx_piecewise) > 0:
            if params[(companion + '_rr')] is not None and params[(companion + '_rr')] > 0:
                model_flux_piecewise = ellc.lc(t_obs=xx_piecewise,
                  radius_1=(params[(companion + '_radius_1')]),
                  radius_2=(params[(companion + '_radius_2')]),
                  sbratio=(params[(companion + '_sbratio_' + inst)]),
                  incl=(params[(companion + '_incl')]),
                  light_3=(params[('dil_' + inst)] / (1.0 - params[('dil_' + inst)])),
                  t_zero=(params[(companion + '_epoch')] + params[(companion + '_ttv_transit_' + str(n_transit + 1))]),
                  period=(params[(companion + '_period')]),
                  a=(params[(companion + '_a')]),
                  q=(params[(companion + '_q')]),
                  f_c=(params[(companion + '_f_c')]),
                  f_s=(params[(companion + '_f_s')]),
                  ldc_1=(params[('host_ldc_' + inst)]),
                  ldc_2=(params[(companion + '_ldc_' + inst)]),
                  gdc_1=(params[('host_gdc_' + inst)]),
                  gdc_2=(params[(companion + '_gdc_' + inst)]),
                  didt=(params[('didt_' + inst)]),
                  domdt=(params[('domdt_' + inst)]),
                  rotfac_1=(params[('host_rotfac_' + inst)]),
                  rotfac_2=(params[(companion + '_rotfac_' + inst)]),
                  hf_1=(params[('host_hf_' + inst)]),
                  hf_2=(params[(companion + '_hf_' + inst)]),
                  bfac_1=(params[('host_bfac_' + inst)]),
                  bfac_2=(params[(companion + '_bfac_' + inst)]),
                  heat_1=(divide(params[('host_atmo_' + inst)], 2.0)),
                  heat_2=(divide(params[(companion + '_atmo_' + inst)], 2.0)),
                  lambda_1=(params[('host_lambda_' + inst)]),
                  lambda_2=(params[(companion + '_lambda_' + inst)]),
                  vsini_1=(params['host_vsini']),
                  vsini_2=(params[(companion + '_vsini')]),
                  t_exp=t_exp,
                  n_int=n_int,
                  grid_1=(settings[('host_grid_' + inst)]),
                  grid_2=(settings[(companion + '_grid_' + inst)]),
                  ld_1=(settings[('host_ld_law_' + inst)]),
                  ld_2=(settings[(companion + '_ld_law_' + inst)]),
                  shape_1=(settings[('host_shape_' + inst)]),
                  shape_2=(settings[(companion + '_shape_' + inst)]),
                  spots_1=(params[('host_spots_' + inst)]),
                  spots_2=(params[(companion + '_spots_' + inst)]),
                  exact_grav=(config.BASEMENT.settings['exact_grav']),
                  verbose=False)
                if companion + '_thermal_emission_amplitude_' + inst in params and params[(companion + '_thermal_emission_amplitude_' + inst)] > 0:
                    model_flux += calc_thermal_curve(params, inst, companion, xx, t_exp, n_int)
            else:
                model_flux_piecewise = np.ones_like(xx)
            model_flux[ind] = model_flux_piecewise

    if settings['N_flares'] > 0:
        for i in range(1, settings['N_flares'] + 1):
            model_flux += aflare1(xx, (params[('flare_tpeak_' + str(i))]), (params[('flare_fwhm_' + str(i))]), (params[('flare_ampl_' + str(i))]), upsample=True, uptime=10)

    return model_flux


def calc_thermal_curve(params, inst, companion, xx, t_exp, n_int):
    if companion + '_thermal_emission_timeshift_' + inst in params:
        xx_shifted = xx - params[(companion + '_thermal_emission_timeshift_' + inst)]
    occultation = ellc.lc(t_obs=xx,
      radius_1=(params[(companion + '_radius_1')]),
      radius_2=(params[(companion + '_radius_2')]),
      sbratio=1000000000000.0,
      incl=(params[(companion + '_incl')]),
      light_3=(params[('dil_' + inst)] / (1.0 - params[('dil_' + inst)])),
      t_zero=(params[(companion + '_epoch')]),
      period=(params[(companion + '_period')]),
      a=(params[(companion + '_a')]),
      q=(params[(companion + '_q')]),
      f_c=(params[(companion + '_f_c')]),
      f_s=(params[(companion + '_f_s')]),
      ldc_1=(params[('host_ldc_' + inst)]),
      ldc_2=(params[(companion + '_ldc_' + inst)]),
      gdc_1=0,
      gdc_2=0,
      didt=(params[('didt_' + inst)]),
      domdt=(params[('domdt_' + inst)]),
      rotfac_1=(params[('host_rotfac_' + inst)]),
      rotfac_2=(params[(companion + '_rotfac_' + inst)]),
      hf_1=(params[('host_hf_' + inst)]),
      hf_2=(params[(companion + '_hf_' + inst)]),
      bfac_1=0,
      bfac_2=0,
      heat_1=0,
      heat_2=0,
      lambda_1=(params[('host_lambda_' + inst)]),
      lambda_2=(params[(companion + '_lambda_' + inst)]),
      vsini_1=(params['host_vsini']),
      vsini_2=(params[(companion + '_vsini')]),
      t_exp=t_exp,
      n_int=n_int,
      grid_1=(config.BASEMENT.settings[('host_grid_' + inst)]),
      grid_2=(config.BASEMENT.settings[(companion + '_grid_' + inst)]),
      ld_1=(config.BASEMENT.settings[('host_ld_law_' + inst)]),
      ld_2=(config.BASEMENT.settings[(companion + '_ld_law_' + inst)]),
      shape_1='sphere',
      shape_2='sphere',
      spots_1=None,
      spots_2=None,
      exact_grav=(config.BASEMENT.settings['exact_grav']),
      verbose=False)
    thermal_curve = ellc.lc(t_obs=xx_shifted,
      radius_1=(params[(companion + '_radius_1')]),
      radius_2=(params[(companion + '_radius_2')]),
      sbratio=0,
      incl=(params[(companion + '_incl')]),
      light_3=(params[('dil_' + inst)] / (1.0 - params[('dil_' + inst)])),
      t_zero=(params[(companion + '_epoch')]),
      period=(params[(companion + '_period')]),
      a=(params[(companion + '_a')]),
      q=(params[(companion + '_q')]),
      f_c=(params[(companion + '_f_c')]),
      f_s=(params[(companion + '_f_s')]),
      ldc_1=(params[('host_ldc_' + inst)]),
      ldc_2=(params[(companion + '_ldc_' + inst)]),
      gdc_1=0,
      gdc_2=0,
      didt=(params[('didt_' + inst)]),
      domdt=(params[('domdt_' + inst)]),
      rotfac_1=(params[('host_rotfac_' + inst)]),
      rotfac_2=(params[(companion + '_rotfac_' + inst)]),
      hf_1=(params[('host_hf_' + inst)]),
      hf_2=(params[(companion + '_hf_' + inst)]),
      bfac_1=0,
      bfac_2=0,
      heat_1=0,
      heat_2=0.1,
      lambda_1=(params[('host_lambda_' + inst)]),
      lambda_2=(params[(companion + '_lambda_' + inst)]),
      vsini_1=(params['host_vsini']),
      vsini_2=(params[(companion + '_vsini')]),
      t_exp=t_exp,
      n_int=n_int,
      grid_1=(config.BASEMENT.settings[('host_grid_' + inst)]),
      grid_2=(config.BASEMENT.settings[(companion + '_grid_' + inst)]),
      ld_1=(config.BASEMENT.settings[('host_ld_law_' + inst)]),
      ld_2=(config.BASEMENT.settings[(companion + '_ld_law_' + inst)]),
      shape_1='sphere',
      shape_2='sphere',
      spots_1=None,
      spots_2=None,
      exact_grav=(config.BASEMENT.ssettings['exact_grav']),
      verbose=False)
    thermal_curve_fine = ellc.lc(t_obs=(np.linspace(params[(companion + '_epoch')], params[(companion + '_epoch')] + params[(companion + '_period')], 1000)),
      radius_1=(params[(companion + '_radius_1')]),
      radius_2=(params[(companion + '_radius_2')]),
      sbratio=0,
      incl=(params[(companion + '_incl')]),
      light_3=(params[('dil_' + inst)] / (1.0 - params[('dil_' + inst)])),
      t_zero=(params[(companion + '_epoch')]),
      period=(params[(companion + '_period')]),
      a=(params[(companion + '_a')]),
      q=(params[(companion + '_q')]),
      f_c=(params[(companion + '_f_c')]),
      f_s=(params[(companion + '_f_s')]),
      ldc_1=(params[('host_ldc_' + inst)]),
      ldc_2=(params[(companion + '_ldc_' + inst)]),
      gdc_1=0,
      gdc_2=0,
      didt=(params[('didt_' + inst)]),
      domdt=(params[('domdt_' + inst)]),
      rotfac_1=(params[('host_rotfac_' + inst)]),
      rotfac_2=(params[(companion + '_rotfac_' + inst)]),
      hf_1=(params[('host_hf_' + inst)]),
      hf_2=(params[(companion + '_hf_' + inst)]),
      bfac_1=0,
      bfac_2=0,
      heat_1=0,
      heat_2=0.1,
      lambda_1=(params[('host_lambda_' + inst)]),
      lambda_2=(params[(companion + '_lambda_' + inst)]),
      vsini_1=(params['host_vsini']),
      vsini_2=(params[(companion + '_vsini')]),
      t_exp=t_exp,
      n_int=n_int,
      grid_1=(config.BASEMENT.settings[('host_grid_' + inst)]),
      grid_2=(config.BASEMENT.settings[(companion + '_grid_' + inst)]),
      ld_1=(config.BASEMENT.settings[('host_ld_law_' + inst)]),
      ld_2=(config.BASEMENT.settings[(companion + '_ld_law_' + inst)]),
      shape_1='sphere',
      shape_2='sphere',
      spots_1=None,
      spots_2=None,
      exact_grav=(config.BASEMENT.settings['exact_grav']),
      verbose=False)
    thermal_curve[thermal_curve < 1.0] = 1.0
    thermal_curve -= 1.0
    thermal_curve *= occultation
    thermal_curve /= np.max(thermal_curve_fine - 1)
    thermal_curve *= params[(companion + '_thermal_emission_amplitude_' + inst)]
    return thermal_curve


def rv_fct(params, inst, companion, xx=None, settings=None):
    """
    ! params must be updated via update_params() before calling this function !
    """
    if xx is None:
        xx = config.BASEMENT.data[inst]['time']
        t_exp = config.BASEMENT.settings[('t_exp_' + inst)]
        n_int = config.BASEMENT.settings[('t_exp_n_int_' + inst)]
    else:
        t_exp = None
        n_int = None
    if params[(companion + '_K')] is not None and params[(companion + '_K')] > 0:
        model_rv1, model_rv2 = ellc.rv(t_obs=xx,
          radius_1=(params[(companion + '_radius_1')]),
          radius_2=(params[(companion + '_radius_2')]),
          sbratio=(params[(companion + '_sbratio_' + inst)]),
          incl=(params[(companion + '_incl')]),
          t_zero=(params[(companion + '_epoch')]),
          period=(params[(companion + '_period')]),
          a=(params[(companion + '_a')]),
          q=(params[(companion + '_q')]),
          f_c=(params[(companion + '_f_c')]),
          f_s=(params[(companion + '_f_s')]),
          ldc_1=(params[('host_ldc_' + inst)]),
          ldc_2=(params[(companion + '_ldc_' + inst)]),
          gdc_1=(params[('host_gdc_' + inst)]),
          gdc_2=(params[(companion + '_gdc_' + inst)]),
          didt=(params[('didt_' + inst)]),
          domdt=(params[('domdt_' + inst)]),
          rotfac_1=(params[('host_rotfac_' + inst)]),
          rotfac_2=(params[(companion + '_rotfac_' + inst)]),
          hf_1=(params[('host_hf_' + inst)]),
          hf_2=(params[(companion + '_hf_' + inst)]),
          bfac_1=(params[('host_bfac_' + inst)]),
          bfac_2=(params[(companion + '_bfac_' + inst)]),
          heat_1=(divide(params[('host_atmo_' + inst)], 2.0)),
          heat_2=(divide(params[(companion + '_atmo_' + inst)], 2.0)),
          lambda_1=(params[('host_lambda_' + inst)]),
          lambda_2=(params[(companion + '_lambda_' + inst)]),
          vsini_1=(params['host_vsini']),
          vsini_2=(params[(companion + '_vsini')]),
          t_exp=t_exp,
          n_int=n_int,
          grid_1=(config.BASEMENT.settings[('host_grid_' + inst)]),
          grid_2=(config.BASEMENT.settings[(companion + '_grid_' + inst)]),
          ld_1=(config.BASEMENT.settings[('host_ld_law_' + inst)]),
          ld_2=(config.BASEMENT.settings[(companion + '_ld_law_' + inst)]),
          shape_1=(config.BASEMENT.settings[('host_shape_' + inst)]),
          shape_2=(config.BASEMENT.settings[(companion + '_shape_' + inst)]),
          spots_1=(params[('host_spots_' + inst)]),
          spots_2=(params[(companion + '_spots_' + inst)]),
          flux_weighted=(config.BASEMENT.settings[(companion + '_flux_weighted_' + inst)]),
          verbose=False)
    else:
        model_rv1 = np.zeros_like(xx)
        model_rv2 = np.zeros_like(xx)
    return (model_rv1, model_rv2)


def calculate_external_priors(params):
    """
    bounds has to be list of len(theta), containing tuples of form
    ('none'), ('uniform', lower bound, upper bound), or ('normal', mean, std)
    """
    lnp = 0.0
    for companion in config.BASEMENT.settings['companions_phot']:
        if config.BASEMENT.settings['use_host_density_prior'] is True and 'host_density' in config.BASEMENT.external_priors and params[(companion + '_host_density')] is not None:
            b = config.BASEMENT.external_priors['host_density']
            if b[0] == 'uniform':
                if not b[1] <= params[(companion + '_host_density')] <= b[2]:
                    return -np.inf
            elif b[0] == 'normal':
                lnp += np.log(1.0 / (np.sqrt(2 * np.pi) * b[2]) * np.exp(-(params[(companion + '_host_density')] - b[1]) ** 2 / (2.0 * b[2] ** 2)))
            else:
                raise ValueError('Bounds have to be "uniform" or "normal". Input was "' + b[0] + '".')

    for companion in config.BASEMENT.settings['companions_all']:
        if not np.abs(params[(companion + '_f_c')]) > 0.8:
            if np.abs(params[(companion + '_f_s')]) > 0.8:
                pass
            lnp = -np.inf

    for inst in config.BASEMENT.settings['inst_all']:
        if params[('dil_' + inst)] > 0.999:
            lnp = -np.inf

    return lnp


def calculate_lnlike_total(params):
    lnlike_total = 0
    lnprior_external = calculate_external_priors(params)
    lnlike_total += lnprior_external
    if np.isnan(lnlike_total) or np.isinf(lnlike_total):
        return -np.inf
    for key, key2 in zip(['flux', 'rv'], ['inst_phot', 'inst_rv']):
        if config.BASEMENT.settings[('stellar_var_' + key)] in FCTs and all([config.BASEMENT.settings[('baseline_' + key + '_' + inst)] in FCTs for inst in config.BASEMENT.settings[key2]]):
            for inst in config.BASEMENT.settings[key2]:
                model = calculate_model(params, inst, key)
                if not any(np.isnan(model)):
                    if any(np.isinf(model)):
                        return -np.inf
                    yerr_w = calculate_yerr_w(params, inst, key)
                    baseline = calculate_baseline(params, inst, key, model=model, yerr_w=yerr_w)
                    stellar_var = calculate_stellar_var(params, inst, key, model=model, baseline=baseline, yerr_w=yerr_w)
                    residuals = config.BASEMENT.data[inst][key] - model - baseline - stellar_var
                    if any(np.isnan(residuals)):
                        return -np.inf
                    inv_sigma2_w = 1.0 / yerr_w ** 2
                    lnlike_total += -0.5 * np.sum(residuals ** 2 * inv_sigma2_w - np.log(inv_sigma2_w / 2.0 / np.pi))

        elif config.BASEMENT.settings[('stellar_var_' + key)] in FCTs and any([config.BASEMENT.settings[('baseline_' + key + '_' + inst)] in GPs for inst in config.BASEMENT.settings[key2]]):
            for inst in config.BASEMENT.settings[key2]:
                model = calculate_model(params, inst, key)
                if not any(np.isnan(model)):
                    if any(np.isinf(model)):
                        return -np.inf
                    if config.BASEMENT.settings[('baseline_' + key + '_' + inst)] in FCTs:
                        yerr_w = calculate_yerr_w(params, inst, key)
                        baseline = calculate_baseline(params, inst, key, model=model, yerr_w=yerr_w)
                        stellar_var = calculate_stellar_var(params, inst, key, model=model, baseline=baseline, yerr_w=yerr_w)
                        residuals = config.BASEMENT.data[inst][key] - model - baseline - stellar_var
                        if any(np.isnan(residuals)):
                            raise ValueError('There are NaN in the residuals. Something horrible happened.')
                        inv_sigma2_w = 1.0 / yerr_w ** 2
                        lnlike_total += -0.5 * np.sum(residuals ** 2 * inv_sigma2_w - np.log(inv_sigma2_w / 2.0 / np.pi))
                    elif config.BASEMENT.settings[('baseline_' + key + '_' + inst)] in GPs:
                        yerr_w = calculate_yerr_w(params, inst, key)
                        stellar_var = calculate_stellar_var(params, inst, key, model=model, baseline=0.0, yerr_w=yerr_w)
                        x = config.BASEMENT.data[inst]['time']
                        y = config.BASEMENT.data[inst][key] - model - stellar_var
                        gp = baseline_get_gp(params, inst, key)
                        try:
                            gp.compute(x, yerr=yerr_w)
                            lnlike_total += gp.log_likelihood(y)
                        except:
                            return -np.inf

                    else:
                        raise ValueError('Kaput.')

        elif config.BASEMENT.settings[('stellar_var_' + key)] in GPs:
            y, yerr_w = [], []
            for inst in config.BASEMENT.settings[key2]:
                model_i = calculate_model(params, inst, key)
                if not any(np.isnan(model_i)):
                    if any(np.isinf(model_i)):
                        return -np.inf
                    yerr_w_i = calculate_yerr_w(params, inst, key)
                    baseline_i = calculate_baseline(params, inst, key, model=model_i, yerr_w=yerr_w_i)
                    residuals_i = config.BASEMENT.data[inst][key] - model_i - baseline_i
                    y += list(residuals_i)
                    yerr_w += list(yerr_w_i)

            ind_sort = config.BASEMENT.data[key2]['ind_sort']
            x = 1.0 * config.BASEMENT.data[key2]['time']
            y = np.array(y)[ind_sort]
            yerr = np.array(yerr_w)[ind_sort]
            gp = stellar_var_get_gp(params, key)
            try:
                gp.compute(x, yerr=yerr)
                lnlike_total += gp.log_likelihood(y)
            except:
                return -np.inf

        elif config.BASEMENT.settings[('stellar_var_' + key)] in GPs and any([config.BASEMENT.settings[('baseline_' + key + '_' + inst)] in GPs for inst in config.BASEMENT.settings[key2]]):
            raise KeyError('Currently you cannot use a GP for stellar variability and a GP for the baseline at the same time.')

    if np.isnan(lnlike_total) or np.isinf(lnlike_total):
        return -np.inf
    return lnlike_total


def calculate_yerr_w(params, inst, key):
    """
    Returns:
    --------
    yerr_w : array of float
        the weighted yerr
    """
    if inst in config.BASEMENT.settings['inst_phot']:
        yerr_w = config.BASEMENT.data[inst][('err_scales_' + key)] * params[('err_' + key + '_' + inst)]
    else:
        if inst in config.BASEMENT.settings['inst_rv']:
            yerr_w = np.sqrt(config.BASEMENT.data[inst][('white_noise_' + key)] ** 2 + params[('jitter_' + key + '_' + inst)] ** 2)
    return yerr_w


def calculate_residuals(params, inst, key):
    """
    Note:
    -----
    No 'xx' here, because residuals can only be calculated on given data
    (not on an arbitrary xx grid)
    """
    model = calculate_model(params, inst, key)
    baseline = calculate_baseline(params, inst, key, model=model)
    residuals = config.BASEMENT.data[inst][key] - model - baseline
    return residuals


def calculate_model(params, inst, key, xx=None, settings=None):
    if settings is None:
        settings = config.BASEMENT.settings
    elif key == 'flux':
        depth = 0.0
        for companion in settings['companions_phot']:
            depth += 1.0 - flux_fct(params, inst, companion, xx=xx, settings=settings)

        model_flux = 1.0 - depth
        return model_flux
        if key == 'rv':
            model_rv = 0.0
            for companion in settings['companions_rv']:
                model_rv += rv_fct(params, inst, companion, xx=xx, settings=settings)[0]

            return model_rv
        if (key == 'centdx') | (key == 'centdy'):
            raise ValueError("Fitting for 'centdx' and 'centdy' not yet implemented.")
    else:
        raise ValueError("Variable 'key' has to be 'flux', 'rv', 'centdx', or 'centdy'.")


def calculate_baseline(params, inst, key, model=None, yerr_w=None, xx=None):
    """
    Inputs:
    -------
    params : dict
        ...
    inst : str
        ...
    key : str
        ...
    model = array of float (optional; default=None)
        ...
    xx : array of float (optional; default=None)
        if given, evaluate the baseline fit on the xx values 
        (e.g. a finer time grid for plotting)
        else, it's the same as data[inst]['time']
        
    Returns: 
    --------
    baseline : array of float
        the baseline evaluate on the grid x (or xx, if xx!=None)
    """
    if model is None:
        model = calculate_model(params, inst, key, xx=None)
    if yerr_w is None:
        yerr_w = calculate_yerr_w(params, inst, key)
    x = config.BASEMENT.data[inst]['time']
    y = config.BASEMENT.data[inst][key] - model
    if xx is None:
        xx = 1.0 * x
    baseline_method = config.BASEMENT.settings[('baseline_' + key + '_' + inst)]
    return baseline_switch[baseline_method](x, y, yerr_w, xx, params, inst, key)


def baseline_hybrid_offset(*args):
    x, y, yerr_w, xx, params, inst, key = args
    yerr_weights = yerr_w / np.nanmean(yerr_w)
    weights = 1.0 / yerr_weights
    ind = np.isfinite(y)
    return np.average((y[ind]), weights=(weights[ind])) * np.ones_like(xx)


def baseline_hybrid_poly(*args):
    x, y, yerr_w, xx, params, inst, key = args
    polyorder = int(config.BASEMENT.settings[('baseline_' + key + '_' + inst)][(-1)])
    xx = (xx - x[0]) / x[(-1)]
    x = (x - x[0]) / x[(-1)]
    if polyorder >= 0:
        yerr_weights = yerr_w / np.nanmean(yerr_w)
        weights = 1.0 / yerr_weights
        ind = np.isfinite(y)
        params_poly = poly.polyfit((x[ind]), (y[ind]), polyorder, w=(weights[ind]))
        baseline = poly.polyval(xx, params_poly)
    else:
        raise ValueError("'polyorder' has to be > 0.")
    return baseline


def baseline_hybrid_spline(*args):
    x, y, yerr_w, xx, params, inst, key = args
    yerr_weights = yerr_w / np.nanmean(yerr_w)
    weights = 1.0 / yerr_weights
    ind = np.isfinite(y)
    spl = UnivariateSpline((x[ind]), (y[ind]), w=(weights[ind]), s=(np.sum(weights[ind])))
    baseline = spl(xx)
    return baseline


def baseline_hybrid_GP(*args):
    x, y, yerr_w, xx, params, inst, key = args
    kernel = terms.Matern32Term(log_sigma=1.0, log_rho=1.0)
    gp = celerite.GP(kernel, mean=(np.nanmean(y)))
    gp.compute(x, yerr=yerr_w)

    def neg_log_like(gp_params, y, gp):
        gp.set_parameter_vector(gp_params)
        return -gp.log_likelihood(y)

    def grad_neg_log_like(gp_params, y, gp):
        gp.set_parameter_vector(gp_params)
        return -gp.grad_log_likelihood(y)[1]

    initial_params = gp.get_parameter_vector()
    bounds = gp.get_parameter_bounds()
    soln = minimize(neg_log_like, initial_params, jac=grad_neg_log_like, method='L-BFGS-B',
      bounds=bounds,
      args=(y, gp))
    gp.set_parameter_vector(soln.x)
    baseline = gp_predict_in_chunks(gp, y, xx)[0]
    return baseline


def baseline_sample_offset(*args):
    x, y, yerr_w, xx, params, inst, key = args
    return params[('baseline_offset_' + key + '_' + inst)] * np.ones_like(xx)


def baseline_sample_linear(*args):
    x, y, yerr_w, xx, params, inst, key = args
    xx_norm = (xx - x[0]) / (x[(-1)] - x[0])
    return params[('baseline_slope_' + key + '_' + inst)] * xx_norm + params[('baseline_offset_' + key + '_' + inst)]


def baseline_sample_GP(*args):
    x, y, yerr_w, xx, params, inst, key = args
    gp = baseline_get_gp(params, inst, key)
    gp.compute(x, yerr=yerr_w)
    baseline = gp_predict_in_chunks(gp, y, xx)[0]
    return baseline


def baseline_get_gp(params, inst, key):
    if config.BASEMENT.settings[('baseline_' + key + '_' + inst)] == 'sample_GP_real':
        kernel = terms.RealTerm(log_a=(params[('baseline_gp_real_lna_' + key + '_' + inst)]), log_c=(params[('baseline_gp_real_lnc_' + key + '_' + inst)]))
    else:
        if config.BASEMENT.settings[('baseline_' + key + '_' + inst)] == 'sample_GP_complex':
            kernel = terms.ComplexTerm(log_a=(params[('baseline_gp_complex_lna_' + key + '_' + inst)]), log_b=(params[('baseline_gp_complex_lnb_' + key + '_' + inst)]),
              log_c=(params[('baseline_gp_complex_lnc_' + key + '_' + inst)]),
              log_d=(params[('baseline_gp_complex_lnd_' + key + '_' + inst)]))
        else:
            if config.BASEMENT.settings[('baseline_' + key + '_' + inst)] == 'sample_GP_Matern32':
                kernel = terms.Matern32Term(log_sigma=(params[('baseline_gp_matern32_lnsigma_' + key + '_' + inst)]), log_rho=(params[('baseline_gp_matern32_lnrho_' + key + '_' + inst)]))
            else:
                if config.BASEMENT.settings[('baseline_' + key + '_' + inst)] == 'sample_GP_SHO':
                    kernel = terms.SHOTerm(log_S0=(params[('baseline_gp_sho_lnS0_' + key + '_' + inst)]), log_Q=(params[('baseline_gp_sho_lnQ_' + key + '_' + inst)]),
                      log_omega0=(params[('baseline_gp_sho_lnomega0_' + key + '_' + inst)]))
                else:
                    KeyError('GP settings and params do not match.')
    if 'baseline_gp_offset_' + key + '_' + inst in params:
        gp = celerite.GP(kernel, mean=(params[('baseline_gp_offset_' + key + '_' + inst)]), fit_mean=True)
    else:
        gp = celerite.GP(kernel, mean=0.0)
    return gp


def baseline_none(*args):
    x, y, yerr_w, xx, params, inst, key = args
    return np.zeros_like(xx)


def baseline_raise_error(*args):
    x, y, yerr_w, xx, params, inst, key = args
    raise ValueError('Setting baseline_' + key + '_' + inst + ' has to be sample_offset / sample_linear / sample_GP / hybrid_offset / hybrid_poly_1 / hybrid_poly_2 / hybrid_poly_3 / hybrid_pol_4 / hybrid_spline / hybrid_GP, ' + '\nbut is:' + config.BASEMENT.settings[('baseline_' + key + '_' + inst)])


baseline_switch = {'hybrid_offset':baseline_hybrid_offset, 
 'hybrid_poly_0':baseline_hybrid_poly, 
 'hybrid_poly_1':baseline_hybrid_poly, 
 'hybrid_poly_2':baseline_hybrid_poly, 
 'hybrid_poly_3':baseline_hybrid_poly, 
 'hybrid_poly_4':baseline_hybrid_poly, 
 'hybrid_poly_5':baseline_hybrid_poly, 
 'hybrid_poly_6':baseline_hybrid_poly, 
 'hybrid_spline':baseline_hybrid_spline, 
 'hybrid_GP':baseline_hybrid_GP, 
 'sample_offset':baseline_sample_offset, 
 'sample_linear':baseline_sample_linear, 
 'sample_GP_real':baseline_sample_GP, 
 'sample_GP_complex':baseline_sample_GP, 
 'sample_GP_Matern32':baseline_sample_GP, 
 'sample_GP_SHO':baseline_sample_GP, 
 'none':baseline_none}

def gp_predict_in_chunks(gp, y, x, chunk_size=5000):
    mu = []
    var = []
    for i in range(int(1.0 * len(x) / chunk_size) + 1):
        m, v = gp.predict(y, (x[i * chunk_size:(i + 1) * chunk_size]), return_var=True)
        mu += list(m)
        var += list(v)

    return (
     np.array(mu), np.array(var))


def calculate_stellar_var(params, inst, key, model=None, baseline=None, yerr_w=None, xx=None):
    stellar_var_method = config.BASEMENT.settings[('stellar_var_' + key)]
    if stellar_var_method not in ('none', ):
        if key == 'flux':
            key2 = 'inst_phot'
        else:
            if key == 'rv':
                key2 = 'inst_rv'
            else:
                KeyError('Kaput.')
        if inst == 'all':
            insts = config.BASEMENT.settings[key2]
        else:
            insts = [
             inst]
        y_list, yerr_w_list = [], []
        for inst in insts:
            if model is None:
                model_i = calculate_model(params, inst, key)
            else:
                model_i = model
            if baseline is None:
                baseline_i = calculate_baseline(params, inst, key, model=model)
            else:
                baseline_i = baseline
            residuals = config.BASEMENT.data[inst][key] - model_i - baseline_i
            y_list += list(residuals)
            if yerr_w is None:
                yerr_w_list += list(calculate_yerr_w(params, inst, key))
            else:
                yerr_w_list += list(yerr_w)

        if inst == 'all':
            ind_sort = config.BASEMENT.data[key2]['ind_sort']
        else:
            ind_sort = slice(None)
        x = 1.0 * config.BASEMENT.data[key2]['time']
        y = np.array(y_list)[ind_sort]
        yerr_w = np.array(yerr_w_list)[ind_sort]
        if xx is None:
            xx = 1.0 * x
        return stellar_var_switch[stellar_var_method](x, y, yerr_w, xx, params, key)
    return 0.0


def stellar_var_get_gp(params, key):
    if config.BASEMENT.settings[('stellar_var_' + key)] == 'sample_GP_real':
        kernel = terms.RealTerm(log_a=(params[('stellar_var_gp_real_lna_' + key)]), log_c=(params[('stellar_var_gp_real_lnc_' + key)]))
    else:
        if config.BASEMENT.settings[('stellar_var_' + key)] == 'sample_GP_complex':
            kernel = terms.ComplexTerm(log_a=(params[('stellar_var_gp_complex_lna_' + key)]), log_b=(params[('stellar_var_gp_complex_lnb_' + key)]),
              log_c=(params[('stellar_var_gp_complex_lnc_' + key)]),
              log_d=(params[('stellar_var_gp_complex_lnd_' + key)]))
        else:
            if config.BASEMENT.settings[('stellar_var_' + key)] == 'sample_GP_Matern32':
                kernel = terms.Matern32Term(log_sigma=(params[('stellar_var_gp_matern32_lnsigma_' + key)]), log_rho=(params[('stellar_var_gp_matern32_lnrho_' + key)]))
            else:
                if config.BASEMENT.settings[('stellar_var_' + key)] == 'sample_GP_SHO':
                    kernel = terms.SHOTerm(log_S0=(params[('stellar_var_gp_sho_lnS0_' + key)]), log_Q=(params[('stellar_var_gp_sho_lnQ_' + key)]),
                      log_omega0=(params[('stellar_var_gp_sho_lnomega0_' + key)]))
                else:
                    KeyError('GP settings and params do not match.')
    if 'stellar_var_gp_offset_' + key in params:
        gp = celerite.GP(kernel, mean=(params[('stellar_var_gp_offset_' + key)]), fit_mean=True)
    else:
        gp = celerite.GP(kernel, mean=0.0)
    return gp


def stellar_var_sample_GP(*args):
    x, y, yerr_w, xx, params, key = args
    gp = stellar_var_get_gp(params, key)
    gp.compute(x, yerr=yerr_w)
    stellar_var = gp_predict_in_chunks(gp, y, xx)[0]
    return stellar_var


def stellar_var_sample_linear(*args):
    x, y, yerr_w, xx, params, key = args
    if key == 'flux':
        key2 = 'inst_phot'
    else:
        if key == 'rv':
            key2 = 'inst_rv'
    x_all = 1.0 * config.BASEMENT.data[key2]['time']
    xx_norm = (xx - x_all[0]) / (x_all[(-1)] - x_all[0])
    return params[('stellar_var_slope_' + key)] * xx_norm + params[('stellar_var_offset_' + key)]


def stellar_var_none(*args):
    x, y, yerr_w, xx, params, key = args
    return np.zeros_like(xx)


stellar_var_switch = {'sample_linear':stellar_var_sample_linear, 
 'sample_GP_real':stellar_var_sample_GP, 
 'sample_GP_complex':stellar_var_sample_GP, 
 'sample_GP_Matern32':stellar_var_sample_GP, 
 'sample_GP_SHO':stellar_var_sample_GP, 
 'none':stellar_var_none}