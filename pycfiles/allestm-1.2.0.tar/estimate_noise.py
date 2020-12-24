# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/priors/estimate_noise.py
# Compiled at: 2019-01-23 21:06:18
__doc__ = '\nCreated on Mon Nov  5 10:46:47 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import os
from exoworlds.lightcurves import gp_decor
from exoworlds.rvs import estimate_jitter
from .. import config
from ..computer import update_params, calculate_model

def estimate_noise(datadir):
    global data_minus_model
    config.init(datadir)
    params = update_params(config.BASEMENT.theta_0)
    priordir = os.path.join(datadir, 'priors')
    if not os.path.exists(priordir):
        os.makedirs(priordir)
    fname_summary = os.path.join(datadir, 'priors', 'summary_phot.csv')
    with open(fname_summary, 'w+') as (f):
        f.write('#name,gp_log_sigma_median,gp_log_sigma_ll,gp_log_sigma_ul,gp_log_rho_median,gp_log_rho_ll,gp_log_rho_ul,log_yerr_median,log_yerr_ll,log_yerr_ul\n')
    for inst in config.BASEMENT.settings['inst_phot']:
        key = 'flux'
        print('\n###############################################################################')
        print(inst + ' ' + key)
        print('###############################################################################')
        outdir = os.path.join(datadir, 'priors', inst)
        fname = inst + '_' + key
        time = config.BASEMENT.data[inst]['time']
        model = calculate_model(params, inst, key)
        data_minus_model = config.BASEMENT.data[inst][key] - model
        gp_decor(time, data_minus_model, multiprocess=config.BASEMENT.settings['multiprocess'], multiprocess_cores=config.BASEMENT.settings['multiprocess_cores'], outdir=outdir, fname=fname, fname_summary=fname_summary)

    fname_summary = os.path.join(datadir, 'priors', 'summary_rv.csv')
    with open(fname_summary, 'w+') as (f):
        f.write('#name,log_yerr_median,log_yerr_ll,log_yerr_ul\n')
    for inst in config.BASEMENT.settings['inst_rv']:
        key = 'rv'
        print('\n###############################################################################')
        print(inst + ' ' + key)
        print('###############################################################################')
        outdir = os.path.join(datadir, 'priors', inst)
        fname = inst + '_' + key
        time = config.BASEMENT.data[inst]['time']
        model = calculate_model(params, inst, key)
        data_minus_model = config.BASEMENT.data[inst][key] - model
        white_noise = config.BASEMENT.data[inst][('white_noise_' + key)]
        estimate_jitter(time, data_minus_model, white_noise, multiprocess=config.BASEMENT.settings['multiprocess'], multiprocess_cores=config.BASEMENT.settings['multiprocess_cores'], outdir=outdir, fname=fname, fname_summary=fname_summary)