# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/nested_sampling.py
# Compiled at: 2018-12-10 04:49:04
"""
Created on Fri Oct  5 01:05:28 2018

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
import numpy as np, os, dynesty
from scipy.special import ndtri
from scipy.stats import truncnorm
from multiprocessing import Pool
from contextlib import closing
import gzip
try:
    import cPickle as pickle
except:
    import pickle

from time import time as timer
import warnings
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
warnings.filterwarnings('ignore', category=np.RankWarning)
from . import config
from .computer import update_params, calculate_lnlike
from .general_output import show_initial_guess, logprint

def ns_lnlike(theta):
    params = update_params(theta)
    lnlike = 0
    for inst in config.BASEMENT.settings['inst_phot']:
        lnlike += calculate_lnlike(params, inst, 'flux')

    for inst in config.BASEMENT.settings['inst_rv']:
        lnlike += calculate_lnlike(params, inst, 'rv')

    if np.isnan(lnlike) or np.isinf(lnlike):
        lnlike = -np.inf
    return lnlike


def ns_prior_transform(utheta):
    theta = np.zeros_like(utheta) * np.nan
    for i in range(len(theta)):
        if config.BASEMENT.bounds[i][0] == 'uniform':
            theta[i] = utheta[i] * (config.BASEMENT.bounds[i][2] - config.BASEMENT.bounds[i][1]) + config.BASEMENT.bounds[i][1]
        elif config.BASEMENT.bounds[i][0] == 'normal':
            theta[i] = config.BASEMENT.bounds[i][1] + config.BASEMENT.bounds[i][2] * ndtri(utheta[i])
        elif config.BASEMENT.bounds[i][0] == 'trunc_normal':
            theta[i] = my_truncnorm_isf(utheta[i], config.BASEMENT.bounds[i][1], config.BASEMENT.bounds[i][2], config.BASEMENT.bounds[i][3], config.BASEMENT.bounds[i][4])
        else:
            raise ValueError('Bounds have to be "uniform", "normal" and "trunc_normal". Input from "params.csv" was "' + config.BASEMENT.bounds[i][0] + '".')

    return theta


def my_truncnorm_isf(q, a, b, mean, std):
    a_scipy = 1.0 * (a - mean) / std
    b_scipy = 1.0 * (b - mean) / std
    return truncnorm.isf(q, a_scipy, b_scipy, loc=mean, scale=std)


def ns_fit(datadir):
    config.init(datadir)
    show_initial_guess()
    nlive = config.BASEMENT.settings['ns_nlive']
    bound = config.BASEMENT.settings['ns_bound']
    ndim = config.BASEMENT.ndim
    sample = config.BASEMENT.settings['ns_sample']
    tol = config.BASEMENT.settings['ns_tol']
    if config.BASEMENT.settings['ns_modus'] == 'static':
        logprint('\nRunning Static Nested Sampler...')
        logprint('--------------------------')
        t0 = timer()
        if config.BASEMENT.settings['multiprocess']:
            with closing(Pool(processes=config.BASEMENT.settings['multiprocess_cores'])) as (pool):
                logprint('\nRunning on', config.BASEMENT.settings['multiprocess_cores'], 'CPUs.')
                sampler = dynesty.NestedSampler(ns_lnlike, ns_prior_transform, ndim, pool=pool, queue_size=config.BASEMENT.settings['multiprocess_cores'], bound=bound, sample=sample, nlive=nlive)
                sampler.run_nested(dlogz=tol, print_progress=config.BASEMENT.settings['print_progress'])
        else:
            sampler = dynesty.NestedSampler(ns_lnlike, ns_prior_transform, ndim, bound=bound, sample=sample, nlive=nlive)
            sampler.run_nested(dlogz=tol, print_progress=config.BASEMENT.settings['print_progress'])
        t1 = timer()
        timedynesty = t1 - t0
        logprint(("\nTime taken to run 'dynesty' (in static mode) is {} hours").format(int(timedynesty / 60.0 / 60.0)))
    elif config.BASEMENT.settings['ns_modus'] == 'dynamic':
        logprint('\nRunning Dynamic Nested Sampler...')
        logprint('--------------------------')
        t0 = timer()
        if config.BASEMENT.settings['multiprocess']:
            with closing(Pool(processes=config.BASEMENT.settings['multiprocess_cores'])) as (pool):
                logprint('\nRunning on', config.BASEMENT.settings['multiprocess_cores'], 'CPUs.')
                sampler = dynesty.DynamicNestedSampler(ns_lnlike, ns_prior_transform, ndim, pool=pool, queue_size=config.BASEMENT.settings['multiprocess_cores'], bound=bound, sample=sample)
                sampler.run_nested(nlive_init=nlive, dlogz_init=tol, print_progress=config.BASEMENT.settings['print_progress'])
        else:
            sampler = dynesty.DynamicNestedSampler(ns_lnlike, ns_prior_transform, ndim, bound=bound, sample=sample)
            sampler.run_nested(nlive_init=nlive, print_progress=config.BASEMENT.settings['print_progress'])
        t1 = timer()
        timedynestydynamic = t1 - t0
        logprint(("\nTime taken to run 'dynesty' (in dynamic mode) is {:.2f} hours").format(timedynestydynamic / 60.0 / 60.0))
    results = sampler.results
    f = gzip.GzipFile(os.path.join(config.BASEMENT.outdir, 'save_ns.pickle.gz'), 'wb')
    pickle.dump(results, f)
    f.close()