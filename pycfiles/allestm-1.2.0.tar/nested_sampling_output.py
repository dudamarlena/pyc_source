# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/nested_sampling_output.py
# Compiled at: 2019-01-24 17:28:15
__doc__ = '\nCreated on Fri Oct  5 14:28:55 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, matplotlib.pyplot as plt, os, gzip
try:
    import cPickle as pickle
except:
    import pickle

from dynesty import utils as dyutils
from dynesty import plotting as dyplot
from . import config
from . import deriver
from .general_output import afplot, save_table, save_latex_table, logprint, get_params_from_samples
from .utils.colormaputil import truncate_colormap
from .utils.latex_printer import round_tex

def draw_ns_posterior_samples(results, Nsamples=None):
    """
    ! posterior samples are drawn as resampled weighted samples !
    ! do not confuse posterior_samples (weighted, resampled) with results['samples'] (unweighted) !
    """
    weights = np.exp(results['logwt'] - results['logz'][(-1)])
    posterior_samples = dyutils.resample_equal(results['samples'], weights)
    if Nsamples:
        posterior_samples = posterior_samples[np.random.randint(len(posterior_samples), size=Nsamples)]
    return posterior_samples


def ns_output(datadir):
    """
    Inputs:
    -------
    datadir : str
        the working directory for allesfitter
        must contain all the data files
        output directories and files will also be created inside datadir
            
    Outputs:
    --------
    This will output information into the console, and create a output files 
    into datadir/results/ (or datadir/QL/ if QL==True)    
    """
    config.init(datadir)
    if os.path.exists(os.path.join(config.BASEMENT.outdir, 'ns_table.csv')):
        overwrite = str(input('Nested Sampling output files already exists in ' + config.BASEMENT.outdir + '.\n' + 'What do you want to do?\n' + '1 : overwrite the output files\n' + '2 : abort\n'))
        if overwrite == '1':
            pass
        else:
            raise ValueError('User aborted operation.')
    f = gzip.GzipFile(os.path.join(config.BASEMENT.outdir, 'save_ns.pickle.gz'), 'rb')
    results = pickle.load(f)
    f.close()
    posterior_samples_for_plot = draw_ns_posterior_samples(results, Nsamples=20)
    for companion in config.BASEMENT.settings['companions_all']:
        fig, axes = afplot(posterior_samples_for_plot, companion)
        fig.savefig(os.path.join(config.BASEMENT.outdir, 'ns_fit_' + companion + '.pdf'), bbox_inches='tight')
        f = gzip.GzipFile(os.path.join(config.BASEMENT.outdir, 'ns_fit.pickle.gz'), 'wb')
        pickle.dump((fig, axes), f)
        f.close()
        plt.close(fig)

    posterior_samples = draw_ns_posterior_samples(results)
    params_median, params_ll, params_ul = get_params_from_samples(posterior_samples)
    logprint('\nResults:')
    logprint('--------------------------')
    logZdynesty = results.logz[(-1)]
    logZerrdynesty = results.logzerr[(-1)]
    logprint(('log(Z) = {} +- {}').format(logZdynesty, logZerrdynesty))
    logprint(('Nr. of posterior samples: {}').format(len(posterior_samples)))
    labels, units = [], []
    for i, l in enumerate(config.BASEMENT.fitlabels):
        labels.append(str(config.BASEMENT.fitlabels[i]))
        units.append(str(config.BASEMENT.fitunits[i]))

    results2 = results.copy()
    posterior_samples2 = draw_ns_posterior_samples(results2)
    params_median2, params_ll2, params_ul2 = get_params_from_samples(posterior_samples2)
    for companion in config.BASEMENT.settings['companions_all']:
        if companion + '_epoch' in config.BASEMENT.fitkeys:
            ind = np.where(config.BASEMENT.fitkeys == companion + '_epoch')[0][0]
            results2['samples'][:, ind] -= int(params_median[(companion + '_epoch')])
            units[ind] = str(units[ind] + '-' + str(int(params_median[(companion + '_epoch')])) + 'd')
            config.BASEMENT.fittruths[ind] -= int(params_median[(companion + '_epoch')])

    for i, l in enumerate(labels):
        if units[i] != '':
            labels[i] = str(labels[i] + ' (' + units[i] + ')')

    cmap = truncate_colormap('Greys', minval=0.2, maxval=0.8, n=256)
    tfig, taxes = dyplot.traceplot(results2, labels=labels, truths=config.BASEMENT.fittruths, post_color='grey', trace_cmap=[cmap] * config.BASEMENT.ndim)
    plt.tight_layout()
    cfig, caxes = dyplot.cornerplot(results2, labels=labels, truths=config.BASEMENT.fittruths, hist_kwargs={'alpha': 0.25, 'linewidth': 0, 'histtype': 'stepfilled'})
    for i, key in enumerate(config.BASEMENT.fitkeys):
        value = round_tex(params_median2[key], params_ll2[key], params_ul2[key])
        ttitle = '' + labels[i] + '$=' + value + '$'
        ctitle = '' + labels[i] + '\n' + '$=' + value + '$'
        if len(config.BASEMENT.fitkeys) > 1:
            caxes[(i, i)].set_title(ctitle)
            taxes[(i, 1)].set_title(ttitle)
            for i in range(caxes.shape[0]):
                for j in range(caxes.shape[1]):
                    caxes[(i, j)].xaxis.set_label_coords(0.5, -0.5)
                    caxes[(i, j)].yaxis.set_label_coords(-0.5, 0.5)

        else:
            caxes.set_title(ctitle)
            taxes[1].set_title(ttitle)
            caxes.xaxis.set_label_coords(0.5, -0.5)
            caxes.yaxis.set_label_coords(-0.5, 0.5)

    tfig.savefig(os.path.join(config.BASEMENT.outdir, 'ns_trace.pdf'), bbox_inches='tight')
    plt.close(tfig)
    cfig.savefig(os.path.join(config.BASEMENT.outdir, 'ns_corner.pdf'), bbox_inches='tight')
    plt.close(cfig)
    save_table(posterior_samples, 'ns')
    save_latex_table(posterior_samples, 'ns')
    if os.path.exists(os.path.join(config.BASEMENT.datadir, 'params_star.csv')):
        deriver.derive(posterior_samples, 'ns')
    else:
        print('File "params_star.csv" not found. Cannot derive final parameters.')
    logprint('Done. For all outputs, see', config.BASEMENT.outdir)


def get_ns_posterior_samples(datadir, Nsamples=None, as_type='dic'):
    config.init(datadir)
    try:
        f = gzip.GzipFile(os.path.join(datadir, 'results', 'save_ns.pickle.gz'), 'rb')
        results = pickle.load(f)
        f.close()
    except:
        with open(os.path.join(datadir, 'results', 'save_ns.pickle'), 'rb') as (f):
            results = pickle.load(f)

    posterior_samples = draw_ns_posterior_samples(results, Nsamples=Nsamples)
    if as_type == '2d_array':
        return posterior_samples
    if as_type == 'dic':
        posterior_samples_dic = {}
        for key in config.BASEMENT.fitkeys:
            ind = np.where(config.BASEMENT.fitkeys == key)[0]
            posterior_samples_dic[key] = posterior_samples[:, ind].flatten()

        return posterior_samples_dic