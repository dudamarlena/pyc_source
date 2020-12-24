# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/exoworlds/rvs/estimate_jitter.py
# Compiled at: 2018-11-07 16:06:49
# Size of source mod 2**32: 10198 bytes
"""
Created on Tue Sep 11 17:32:25 2018

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
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from datetime import datetime
import emcee, corner
from multiprocessing import Pool, cpu_count
from contextlib import closing
np.random.seed(21)

def log_probability(params):
    """
    works on X, Y
    """
    try:
        ll = log_likelihood(params)
        lp = external_log_prior(params)
    except:
        return -np.inf
        if not np.isfinite(lp):
            return -np.inf
        return ll + lp


def external_log_prior(params):
    log_jitter = params
    lp = 0
    if not -23 < log_jitter < 0:
        lp = -np.inf
    return lp


def log_likelihood(theta):
    log_jitter = theta
    jitter = np.exp(log_jitter)
    yerr = np.sqrt(WHITE_NOISE ** 2 + jitter ** 2)
    inv_sigma2_w = 1.0 / yerr ** 2
    return -0.5 * np.nansum(Y ** 2 * inv_sigma2_w - np.log(inv_sigma2_w))


def estimate_jitter(x, y, white_noise, jitter_guess=None, mean=0.0, nwalkers=50, thin_by=50, burn_steps=2500, total_steps=5000, bin_width=None, xlabel='x', ylabel='y', ydetr_label='ydetr', outdir='jitter_fit', fname=None, fname_summary=None, multiprocess=False, multiprocess_cores=None):
    """
    Required Input:
    ---------------
    x : array of float
        x-values of the data set
    y : array of float
        y-values of the data set
    white_noise : array of float / float
        white_noise on y-values of the data set
        
    Optional Input:
    ---------------
    mean : float (default 0.)
        mean of the data set
        the default is 1., assuming usually y will be normalized flux
    nwalkers : int
        number of MCMC walkers
    thin_by : int
        thinning the MCMC chain by how much
    burn_steps : int
        how many steps to burn in the MCMC
    total_steps : int
        total MCMC steps (including burn_steps)
    xlabel : str
        x axis label (for plots)
    ylabel : str
        y axis label (for plots)       
    ydetr_label : str
        y_detr axis label (for plots)    
    outdir : str
        name of the output directory
    fname : str
        prefix of the output files (e.g. a planet name)
    multiprocess : bool (default False)
        run MCMC on multiprocess_cores cores        
    multiprocess_cores : bool (default None)
        run MCMC on many cores        
    """
    global MEAN
    global WHITE_NOISE
    global X
    global Y
    X = x
    Y = y
    WHITE_NOISE = white_noise
    MEAN = mean
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    else:
        now = datetime.now().isoformat()

        def logprint(*text):
            print(*text)
            original = sys.stdout
            with open(os.path.join(outdir, fname + 'logfile_' + now + '.log'), 'a') as (f):
                sys.stdout = f
                print(*text)
            sys.stdout = original

        if fname is not None:
            fname += '_jitter_fit_'
        else:
            fname = 'jitter_fit_'
    names = [
     '$\\log{(y_\\mathrm{err})}$']
    discard = int(1.0 * burn_steps / thin_by)
    logprint('\nStarting...')
    yerr = np.nanstd(Y) * np.ones_like(Y)
    if jitter_guess is None:
        jitter_guess = np.nanmedian(np.log(np.sqrt(yerr ** 2 - white_noise ** 2)))
    fig, ax = plt.subplots()
    ax.errorbar(x, y, yerr=white_noise, fmt='.b', capsize=0)
    ax.set(xlabel=xlabel, ylabel=ylabel, title='Original data')
    fig.savefig((os.path.join(outdir, fname + 'data.jpg')), dpi=100, bbox_inches='tight')
    plt.close(fig)
    if multiprocess:
        if not multiprocess_cores:
            multiprocess_cores = cpu_count() - 1
    logprint('\nRunning MCMC fit...')
    if multiprocess:
        logprint('\tRunning on', multiprocess_cores, 'CPUs.')
    initial = np.array([jitter_guess])
    ndim = len(initial)
    backend = emcee.backends.HDFBackend(os.path.join(outdir, fname + 'mcmc_save.h5'))
    backend.reset(nwalkers, ndim)

    def run_mcmc(sampler):
        p0 = initial + 1e-08 * np.random.randn(nwalkers, ndim)
        sampler.run_mcmc(p0, (total_steps / thin_by), thin_by=thin_by, progress=True)

    if multiprocess:
        with closing(Pool(processes=multiprocess_cores)) as (pool):
            sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, pool=pool, backend=backend)
            run_mcmc(sampler)
    else:
        sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, backend=backend)
        run_mcmc(sampler)
    logprint('\nAcceptance fractions:')
    logprint(sampler.acceptance_fraction)
    tau = sampler.get_autocorr_time(discard=discard, c=5, tol=10, quiet=True) * thin_by
    logprint('\nAutocorrelation times:')
    logprint('\t', '{0: <30}'.format('parameter'), '{0: <20}'.format('tau (in steps)'), '{0: <20}'.format('Chain length (in multiples of tau)'))
    for i, key in enumerate(names):
        logprint('\t', '{0: <30}'.format(key), '{0: <20}'.format(tau[i]), '{0: <20}'.format((total_steps - burn_steps) / tau[i]))

    def get_params_from_samples(samples, names):
        """
        read MCMC results and update params
        """
        buf = map(lambda v: (v[1], v[2] - v[1], v[1] - v[0]), zip(*np.percentile(samples, [16, 50, 84], axis=0)))
        theta_median = [item[0] for item in buf]
        theta_ul = [item[1] for item in buf]
        theta_ll = [item[2] for item in buf]
        params_median = {n:t for n, t in zip(names, theta_median)}
        params_ul = {n:t for n, t in zip(names, theta_ul)}
        params_ll = {n:t for n, t in zip(names, theta_ll)}
        return (
         params_median, params_ll, params_ul)

    samples = sampler.get_chain(flat=True, discard=discard)
    params, params_ll, params_ul = get_params_from_samples(samples, names)
    with open(os.path.join(outdir, fname + 'table.csv'), 'wb') as (f):
        f.write('name,median,ll,ul\n')
        for i, key in enumerate(names):
            f.write(key + ',' + str(params[key]) + ',' + str(params_ll[key]) + ',' + str(params_ul[key]) + '\n')

    if fname_summary is not None:
        with open(fname_summary, 'ab') as (f):
            f.write(fname[0:-1] + ',')
            for i, key in enumerate(names):
                f.write(str(params[key]) + ',' + str(params_ll[key]) + ',' + str(params_ul[key]))
                if i < len(names) - 1:
                    f.write(',')
                else:
                    f.write('\n')

    fig, axes = plt.subplots((ndim + 1), 1, figsize=(6, 4 * (ndim + 1)))
    steps = np.arange(0, total_steps, thin_by)
    for j in range(nwalkers):
        axes[0].plot(steps, sampler.get_log_prob()[:, j], '-')

    axes[0].set(ylabel='lnprob', xlabel='steps')
    for i in range(ndim):
        ax = axes[(i + 1)]
        ax.set(ylabel=(names[i]), xlabel='steps')
        for j in range(nwalkers):
            ax.plot(steps, sampler.chain[j, :, i], '-')

        ax.axvline(burn_steps, color='k', linestyle='--')

    plt.tight_layout()
    fig.savefig((os.path.join(outdir, fname + 'mcmc_chains.jpg')), dpi=100, bbox_inches='tight')
    plt.close(fig)
    fig = corner.corner(samples, labels=names,
      show_titles=True,
      title_kwargs={'fontsize': 12})
    fig.savefig((os.path.join(outdir, fname + 'mcmc_corner.jpg')), dpi=100, bbox_inches='tight')
    plt.close(fig)
    logprint('\nDone. All output files are in ' + outdir)


if __name__ == '__main__':
    pass