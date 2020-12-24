# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/computer.py
# Compiled at: 2019-01-23 21:06:33
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
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, ellc
from scipy.optimize import minimize
from scipy.interpolate import UnivariateSpline
import numpy.polynomial.polynomial as poly, warnings
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
warnings.filterwarnings('ignore', category=np.RankWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)
try:
    import celerite
    from celerite import terms
except ImportError:
    warnings.warn("Cannot import package 'celerite', thus 'hybrid_GP' baseline models will not be supported.")

from . import config
from .flares.aflare import aflare1

def update_params(theta, phased=False):
    params = config.BASEMENT.params.copy()
    for i, key in enumerate(config.BASEMENT.fitkeys):
        params[key] = theta[i]

    for i, key in enumerate(config.BASEMENT.allkeys):
        if isinstance(config.BASEMENT.coupled_with[i], str) and len(config.BASEMENT.coupled_with[i]) > 0:
            params[key] = params[config.BASEMENT.coupled_with[i]]

    if phased:
        for companion in config.BASEMENT.settings['companions_all']:
            params[companion + '_epoch'] = 0.0
            params[companion + '_period'] = 1.0

    for companion in config.BASEMENT.settings['companions_all']:
        params[companion + '_incl'] = np.arccos(params[(companion + '_cosi')]) / np.pi * 180.0

    for companion in config.BASEMENT.settings['companions_phot']:
        for inst in config.BASEMENT.settings['inst_phot']:
            key = 'flux'
            params['err_' + key + '_' + inst] = np.exp(params[('log_err_' + key + '_' + inst)])

    for companion in config.BASEMENT.settings['companions_all']:
        for inst in config.BASEMENT.settings['inst_all']:
            try:
                params[companion + '_radius_1'] = params[(companion + '_rsuma')] / (1.0 + params[(companion + '_rr')])
                params[companion + '_radius_2'] = params[(companion + '_radius_1')] * params[(companion + '_rr')]
            except:
                params[companion + '_radius_1'] = None
                params[companion + '_radius_2'] = None

    for inst in config.BASEMENT.settings['inst_all']:
        if config.BASEMENT.settings[('host_ld_law_' + inst)] is None:
            params['host_ldc_' + inst] = None
        elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'lin':
            params['host_ldc_' + inst] = params[('host_ldc_q1_' + inst)]
        elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'quad':
            ldc_u1 = 2.0 * np.sqrt(params[('host_ldc_q1_' + inst)]) * params[('host_ldc_q2_' + inst)]
            ldc_u2 = np.sqrt(params[('host_ldc_q1_' + inst)]) * (1.0 - 2.0 * params[('host_ldc_q2_' + inst)])
            params['host_ldc_' + inst] = [ldc_u1, ldc_u2]
        elif config.BASEMENT.settings[('host_ld_law_' + inst)] == 'sing':
            raise ValueError('Sorry, I have not yet implemented the Sing limb darkening law.')
        else:
            print(config.BASEMENT.settings[('host_ld_law_' + inst)])
            raise ValueError("Currently only 'none', 'lin', 'quad' and 'sing' limb darkening are supported.")

    for companion in config.BASEMENT.settings['companions_rv']:
        for inst in config.BASEMENT.settings['inst_rv']:
            key = 'rv'
            params['jitter_' + key + '_' + inst] = np.exp(params[('log_jitter_' + key + '_' + inst)])

        ecc = params[(companion + '_f_s')] ** 2 + params[(companion + '_f_c')] ** 2
        a_1 = 0.019771142 * params[(companion + '_K')] * params[(companion + '_period')] * np.sqrt(1.0 - ecc ** 2) / np.sin(params[(companion + '_incl')] * np.pi / 180.0)
        params[companion + '_a'] = (1.0 + 1.0 / params[(companion + '_q')]) * a_1

    for i, key in enumerate(config.BASEMENT.allkeys):
        if isinstance(config.BASEMENT.coupled_with[i], str) and len(config.BASEMENT.coupled_with[i]) > 0:
            params[key] = params[config.BASEMENT.coupled_with[i]]

    for companion in config.BASEMENT.settings['companions_all']:
        for inst in config.BASEMENT.settings['inst_all']:
            if config.BASEMENT.settings[('host_N_spots_' + inst)] > 0:
                params['host_spots_' + inst] = [[ params[('host_spot_' + str(i) + '_long_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1) ], [ params[('host_spot_' + str(i) + '_lat_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1) ], [ params[('host_spot_' + str(i) + '_size_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1) ], [ params[('host_spot_' + str(i) + '_brightness_' + inst)] for i in range(1, config.BASEMENT.settings[('host_N_spots_' + inst)] + 1) ]]
            if config.BASEMENT.settings[(companion + '_N_spots_' + inst)] > 0:
                params[companion + '_spots_' + inst] = [[ params[(companion + '_spot_' + str(i) + '_long_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1) ], [ params[(companion + '_spot_' + str(i) + '_lat_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1) ], [ params[(companion + '_spot_' + str(i) + '_size_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1) ], [ params[(companion + '_spot_' + str(i) + '_brightness_' + inst)] for i in range(1, config.BASEMENT.settings[(companion + '_N_spots_' + inst)] + 1) ]]

    return params


def flux_fct(params, inst, companion, xx=None):
    """
    ! params must be updated via update_params() before calling this function !
    
    if phased, pass e.g. xx=np.linspace(-0.25,0.75,1000) amd t_exp_scalefactor=1./params[companion+'_period']
    """
    if xx is None:
        xx = config.BASEMENT.data[inst]['time'] + params[('ttv_' + inst)]
        t_exp = config.BASEMENT.settings[('t_exp_' + inst)]
        n_int = config.BASEMENT.settings[('t_exp_n_int_' + inst)]
    else:
        t_exp = None
        n_int = None
    if params[(companion + '_rr')] > 0:
        model_flux = ellc.lc(t_obs=xx, radius_1=params[(companion + '_radius_1')], radius_2=params[(companion + '_radius_2')], sbratio=params[(companion + '_sbratio_' + inst)], incl=params[(companion + '_incl')], light_3=params[('dil_' + inst)], t_zero=params[(companion + '_epoch')], period=params[(companion + '_period')], a=params[(companion + '_a')], q=params[(companion + '_q')], f_c=params[(companion + '_f_c')], f_s=params[(companion + '_f_s')], ldc_1=params[('host_ldc_' + inst)], ldc_2=params[(companion + '_ldc_' + inst)], gdc_1=params[('host_gdc_' + inst)], gdc_2=params[(companion + '_gdc_' + inst)], didt=params[('didt_' + inst)], domdt=params[('domdt_' + inst)], rotfac_1=params[('host_rotfac_' + inst)], rotfac_2=params[(companion + '_rotfac_' + inst)], hf_1=params[('host_hf_' + inst)], hf_2=params[(companion + '_hf_' + inst)], bfac_1=params[('host_bfac_' + inst)], bfac_2=params[(companion + '_bfac_' + inst)], heat_1=params[('host_geom_albedo_' + inst)] / 2.0, heat_2=params[(companion + '_geom_albedo_' + inst)] / 2.0, lambda_1=params[('host_lambda_' + inst)], lambda_2=params[(companion + '_lambda_' + inst)], vsini_1=params[('host_vsini_' + inst)], vsini_2=params[(companion + '_vsini_' + inst)], t_exp=t_exp, n_int=n_int, grid_1=config.BASEMENT.settings[('host_grid_' + inst)], grid_2=config.BASEMENT.settings[(companion + '_grid_' + inst)], ld_1=config.BASEMENT.settings[('host_ld_law_' + inst)], ld_2=config.BASEMENT.settings[(companion + '_ld_law_' + inst)], shape_1=config.BASEMENT.settings[('host_shape_' + inst)], shape_2=config.BASEMENT.settings[(companion + '_shape_' + inst)], spots_1=params[('host_spots_' + inst)], spots_2=params[(companion + '_spots_' + inst)], verbose=False)
    else:
        model_flux = np.ones_like(xx)
    if config.BASEMENT.settings['N_flares'] > 0:
        for i in range(1, config.BASEMENT.settings['N_flares'] + 1):
            model_flux += aflare1(xx, params[('flare_tpeak_' + str(i))], params[('flare_fwhm_' + str(i))], params[('flare_ampl_' + str(i))], upsample=True, uptime=10)

    return model_flux


def rv_fct(params, inst, companion, xx=None):
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
    model_rv1, model_rv2 = ellc.rv(t_obs=xx, radius_1=params[(companion + '_radius_1')], radius_2=params[(companion + '_radius_2')], sbratio=params[(companion + '_sbratio_' + inst)], incl=params[(companion + '_incl')], t_zero=params[(companion + '_epoch')], period=params[(companion + '_period')], a=params[(companion + '_a')], q=params[(companion + '_q')], f_c=params[(companion + '_f_c')], f_s=params[(companion + '_f_s')], ldc_1=params[('host_ldc_' + inst)], ldc_2=params[(companion + '_ldc_' + inst)], gdc_1=params[('host_gdc_' + inst)], gdc_2=params[(companion + '_gdc_' + inst)], didt=params[('didt_' + inst)], domdt=params[('domdt_' + inst)], rotfac_1=params[('host_rotfac_' + inst)], rotfac_2=params[(companion + '_rotfac_' + inst)], hf_1=params[('host_hf_' + inst)], hf_2=params[(companion + '_hf_' + inst)], bfac_1=params[('host_bfac_' + inst)], bfac_2=params[(companion + '_bfac_' + inst)], heat_1=params[('host_geom_albedo_' + inst)] / 2.0, heat_2=params[(companion + '_geom_albedo_' + inst)] / 2.0, lambda_1=params[('host_lambda_' + inst)], lambda_2=params[(companion + '_lambda_' + inst)], vsini_1=params[('host_vsini_' + inst)], vsini_2=params[(companion + '_vsini_' + inst)], t_exp=t_exp, n_int=n_int, grid_1=config.BASEMENT.settings[('host_grid_' + inst)], grid_2=config.BASEMENT.settings[(companion + '_grid_' + inst)], ld_1=config.BASEMENT.settings[('host_ld_law_' + inst)], ld_2=config.BASEMENT.settings[(companion + '_ld_law_' + inst)], shape_1=config.BASEMENT.settings[('host_shape_' + inst)], shape_2=config.BASEMENT.settings[(companion + '_shape_' + inst)], spots_1=params[('host_spots_' + inst)], spots_2=params[(companion + '_spots_' + inst)], flux_weighted=False, verbose=False)
    return (
     model_rv1, model_rv2)


def calculate_lnlike(params, inst, key):
    model = calculate_model(params, inst, key)
    if any(np.isnan(model)) or any(np.isinf(model)):
        return -np.inf
    else:
        if config.BASEMENT.settings[('baseline_' + key + '_' + inst)] != 'sample_GP':
            yerr_w = calculate_yerr_w(params, inst, key)
            baseline = calculate_baseline(params, inst, key, model=model, yerr_w=yerr_w)
            residuals = config.BASEMENT.data[inst][key] - model - baseline
            inv_sigma2_w = 1.0 / yerr_w ** 2
            return -0.5 * np.sum(residuals ** 2 * inv_sigma2_w - np.log(inv_sigma2_w))
        x = config.BASEMENT.data[inst]['time']
        y = config.BASEMENT.data[inst][key] - model
        yerr_w = calculate_yerr_w(params, inst, key)
        kernel = terms.Matern32Term(log_sigma=params[('baseline_gp1_' + key + '_' + inst)], log_rho=params[('baseline_gp2_' + key + '_' + inst)])
        gp = celerite.GP(kernel)
        try:
            gp.compute(x, yerr=yerr_w)
            lnlike = gp.log_likelihood(y)
        except:
            lnlike = -np.inf

        return lnlike


def calculate_yerr_w(params, inst, key):
    """
    Returns:
    --------
    yerr_w : array of float
        the weighted yerr
    """
    if inst in config.BASEMENT.settings['inst_phot']:
        yerr_w = config.BASEMENT.data[inst][('err_scales_' + key)] * params[('err_' + key + '_' + inst)]
    elif inst in config.BASEMENT.settings['inst_rv']:
        yerr_w = np.sqrt(config.BASEMENT.data[inst][('white_noise_' + key)] ** 2 + params[('jitter_' + key + '_' + inst)] ** 2)
    return yerr_w


def calculate_model(params, inst, key, xx=None):
    if key == 'flux':
        depth = 0.0
        for companion in config.BASEMENT.settings['companions_phot']:
            depth += 1.0 - flux_fct(params, inst, companion, xx=xx)

        model_flux = 1.0 - depth
        return model_flux
    if key == 'rv':
        model_rv = 0.0
        for companion in config.BASEMENT.settings['companions_rv']:
            model_rv += rv_fct(params, inst, companion, xx=xx)[0]

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
    return np.average(y[ind], weights=weights[ind]) * np.ones_like(xx)


def baseline_hybrid_poly(*args):
    x, y, yerr_w, xx, params, inst, key = args
    polyorder = int(config.BASEMENT.settings[('baseline_' + key + '_' + inst)][(-1)])
    xx = (xx - x[0]) / x[(-1)]
    x = (x - x[0]) / x[(-1)]
    if polyorder >= 0:
        yerr_weights = yerr_w / np.nanmean(yerr_w)
        weights = 1.0 / yerr_weights
        ind = np.isfinite(y)
        params_poly = poly.polyfit(x[ind], y[ind], polyorder, w=weights[ind])
        baseline = poly.polyval(xx, params_poly)
    else:
        raise ValueError("'polyorder' has to be > 0.")
    return baseline


def baseline_hybrid_spline(*args):
    x, y, yerr_w, xx, params, inst, key = args
    yerr_weights = yerr_w / np.nanmean(yerr_w)
    weights = 1.0 / yerr_weights
    ind = np.isfinite(y)
    spl = UnivariateSpline(x[ind], y[ind], w=weights[ind], s=np.sum(weights[ind]))
    baseline = spl(xx)
    return baseline


def baseline_hybrid_GP(*args):
    x, y, yerr_w, xx, params, inst, key = args
    kernel = terms.Matern32Term(log_sigma=1.0, log_rho=1.0)
    gp = celerite.GP(kernel, mean=np.nanmean(y))
    gp.compute(x, yerr=yerr_w)

    def neg_log_like(gp_params, y, gp):
        gp.set_parameter_vector(gp_params)
        return -gp.log_likelihood(y)

    def grad_neg_log_like(gp_params, y, gp):
        gp.set_parameter_vector(gp_params)
        return -gp.grad_log_likelihood(y)[1]

    initial_params = gp.get_parameter_vector()
    bounds = gp.get_parameter_bounds()
    soln = minimize(neg_log_like, initial_params, jac=grad_neg_log_like, method='L-BFGS-B', bounds=bounds, args=(y, gp))
    gp.set_parameter_vector(soln.x)
    baseline = gp_predict_in_chunks(gp, y, xx)[0]
    return baseline


def baseline_sample_offset(*args):
    x, y, yerr_w, xx, params, inst, key = args
    return params[('baseline_offset_' + key + '_' + inst)] * np.ones_like(xx)


def baseline_sample_linear(*args):
    raise ValueError('Not yet implemented.')


def baseline_sample_GP(*args):
    x, y, yerr_w, xx, params, inst, key = args
    kernel = terms.Matern32Term(log_sigma=params[('baseline_gp1_' + key + '_' + inst)], log_rho=params[('baseline_gp2_' + key + '_' + inst)])
    gp = celerite.GP(kernel)
    gp.compute(x, yerr=yerr_w)
    baseline = gp_predict_in_chunks(gp, y, xx)[0]
    return baseline


def baseline_none(*args):
    x, y, yerr_w, xx, params, inst, key = args
    return np.zeros_like(xx)


def baseline_raise_error(*args):
    x, y, yerr_w, xx, params, inst, key = args
    raise ValueError('Setting baseline_' + key + '_' + inst + ' has to be sample_offset / sample_linear / sample_GP / hybrid_offset / hybrid_poly_1 / hybrid_poly_2 / hybrid_poly_3 / hybrid_pol_4 / hybrid_spline / hybrid_GP, ' + '\nbut is:' + config.BASEMENT.settings[('baseline_' + key + '_' + inst)])


baseline_switch = {'hybrid_offset': baseline_hybrid_offset, 
   'hybrid_poly_0': baseline_hybrid_poly, 
   'hybrid_poly_1': baseline_hybrid_poly, 
   'hybrid_poly_2': baseline_hybrid_poly, 
   'hybrid_poly_3': baseline_hybrid_poly, 
   'hybrid_poly_4': baseline_hybrid_poly, 
   'hybrid_poly_5': baseline_hybrid_poly, 
   'hybrid_poly_6': baseline_hybrid_poly, 
   'hybrid_spline': baseline_hybrid_spline, 
   'hybrid_GP': baseline_hybrid_GP, 
   'sample_offset': baseline_sample_offset, 
   'sample_linear': baseline_sample_linear, 
   'sample_GP': baseline_sample_GP, 
   'none': baseline_none}

def gp_predict_in_chunks(gp, y, x, chunk_size=5000):
    mu = []
    var = []
    for i in range(int(1.0 * len(x) / chunk_size) + 1):
        m, v = gp.predict(y, x[i * chunk_size:(i + 1) * chunk_size], return_var=True)
        mu += list(m)
        var += list(v)

    return (
     np.array(mu), np.array(var))