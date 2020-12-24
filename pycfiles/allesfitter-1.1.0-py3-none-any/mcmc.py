# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/mcmc.py
# Compiled at: 2018-11-07 16:59:06
"""
Created on Fri Oct  5 01:03:21 2018

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
import numpy as np, os, emcee
from multiprocessing import Pool
from contextlib import closing
import warnings
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
warnings.filterwarnings('ignore', category=np.RankWarning)
from . import config
from .computer import update_params, calculate_lnlike
from .general_output import show_initial_guess, logprint
from .mcmc_output import print_autocorr

def mcmc_lnlike(theta):
    params = update_params(theta)
    lnlike = 0
    for inst in config.BASEMENT.settings['inst_phot']:
        lnlike += calculate_lnlike(params, inst, 'flux')

    for inst in config.BASEMENT.settings['inst_rv']:
        lnlike += calculate_lnlike(params, inst, 'rv')

    return lnlike


def mcmc_lnprior(theta):
    """
    bounds has to be list of len(theta), containing tuples of form
    ('none'), ('uniform', lower bound, upper bound), or ('normal', mean, std)
    """
    lnp = 0.0
    for th, b in zip(theta, config.BASEMENT.bounds):
        if b[0] == 'uniform':
            if not b[1] <= th <= b[2]:
                return -np.inf
        elif b[0] == 'normal':
            lnp += np.log(1.0 / (np.sqrt(2 * np.pi) * b[2]) * np.exp(-(th - b[1]) ** 2 / (2.0 * b[2] ** 2)))
        else:
            raise ValueError('Bounds have to be "uniform" or "normal". Input from "params.csv" was "' + b[0] + '".')

    return lnp


def mcmc_lnprob(theta):
    """
    has to be top-level for  for multiprocessing pickle
    """
    lp = mcmc_lnprior(theta)
    if not np.isfinite(lp):
        return -np.inf
    try:
        ln = mcmc_lnlike(theta)
        return lp + ln
    except:
        return -np.inf


def mcmc_fit(datadir):
    config.init(datadir)
    show_initial_guess()
    continue_old_run = False
    if os.path.exists(os.path.join(config.BASEMENT.outdir, 'mcmc_save.h5')):
        overwrite = raw_input(os.path.join(config.BASEMENT.outdir, 'mcmc_save.h5') + ' already exists.\n' + 'What do you want to do?\n' + '1 : overwrite the save file\n' + '2 : append to the save file\n' + '3 : abort\n')
        if overwrite == '1':
            continue_old_run = False
        elif overwrite == '2':
            continue_old_run = True
        else:
            raise ValueError('User aborted operation.')
    backend = emcee.backends.HDFBackend(os.path.join(config.BASEMENT.outdir, 'mcmc_save.h5'))
    if not continue_old_run:
        backend.reset(config.BASEMENT.settings['mcmc_nwalkers'], config.BASEMENT.ndim)

    def run_mcmc(sampler):
        if continue_old_run:
            p0 = backend.get_chain()[-1, :, :]
            already_completed_steps = backend.get_chain().shape[0] * config.BASEMENT.settings['mcmc_thin_by']
        else:
            p0 = config.BASEMENT.theta_0 + config.BASEMENT.init_err * np.random.randn(config.BASEMENT.settings['mcmc_nwalkers'], config.BASEMENT.ndim)
            already_completed_steps = 0
        for i, b in enumerate(config.BASEMENT.bounds):
            if b[0] == 'uniform':
                p0[:, i] = np.clip(p0[:, i], b[1], b[2])

        sampler.run_mcmc(p0, (config.BASEMENT.settings['mcmc_total_steps'] - already_completed_steps) / config.BASEMENT.settings['mcmc_thin_by'], thin_by=config.BASEMENT.settings['mcmc_thin_by'], progress=True)
        return sampler

    logprint('\nRunning MCMC...')
    logprint('--------------------------')
    if config.BASEMENT.settings['multiprocess']:
        with closing(Pool(processes=config.BASEMENT.settings['multiprocess_cores'])) as (pool):
            logprint('\nRunning on', config.BASEMENT.settings['multiprocess_cores'], 'CPUs.')
            sampler = emcee.EnsembleSampler(config.BASEMENT.settings['mcmc_nwalkers'], config.BASEMENT.ndim, mcmc_lnprob, pool=pool, backend=backend)
            sampler = run_mcmc(sampler)
    else:
        sampler = emcee.EnsembleSampler(config.BASEMENT.settings['mcmc_nwalkers'], config.BASEMENT.ndim, mcmc_lnprob, backend=backend)
        sampler = run_mcmc(sampler)
    logprint('\nAcceptance fractions:')
    logprint('--------------------------')
    logprint(sampler.acceptance_fraction)
    print_autocorr(sampler)