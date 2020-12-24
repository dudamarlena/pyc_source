# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/general_output.py
# Compiled at: 2019-01-24 13:45:24
__doc__ = '\nCreated on Fri Oct  5 01:10:51 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction': 'in', 'ytick.direction': 'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, matplotlib.pyplot as plt, os, sys, warnings
from astropy.time import Time
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
warnings.filterwarnings('ignore', category=np.RankWarning)
from exoworlds.lightcurves import lightcurve_tools as lct
from . import config
from .utils import latex_printer
from .computer import update_params, calculate_model, rv_fct, flux_fct, calculate_baseline, calculate_yerr_w

def logprint(*text):
    print(*text)
    original = sys.stdout
    with open(os.path.join(config.BASEMENT.outdir, 'logfile_' + config.BASEMENT.now + '.log'), 'a') as (f):
        sys.stdout = f
        print(*text)
    sys.stdout = original


def draw_initial_guess_samples(Nsamples=1):
    if Nsamples == 1:
        samples = np.array([config.BASEMENT.theta_0])
    else:
        samples = config.BASEMENT.theta_0 + config.BASEMENT.init_err * np.random.randn(Nsamples, len(config.BASEMENT.theta_0))
    return samples


def plot_panel(datadir):
    config.init(datadir)
    fig, axes = plt.subplots(2, 1, figsize=(20, 10))
    for inst in config.BASEMENT.settings['inst_phot']:
        axes[0].plot(config.BASEMENT.data[inst]['time'], config.BASEMENT.data[inst]['flux'], marker='.', ls='none', label=inst)

    for inst in config.BASEMENT.settings['inst_rv']:
        axes[1].plot(config.BASEMENT.data[inst]['time'], config.BASEMENT.data[inst]['rv'], marker='.', ls='none', label=inst)

    axes[0].legend()
    axes[1].legend()
    return (
     fig, axes)


def afplot(samples, companion):
    """
    Inputs:
    -------
    samples : array
        samples from the initial guess, or from the MCMC / Nested Sampling posteriors
    """
    N_inst = len(config.BASEMENT.settings['inst_all'])
    if 'do_not_phase_fold' in config.BASEMENT.settings and config.BASEMENT.settings['do_not_phase_fold']:
        fig, axes = plt.subplots(N_inst, 1, figsize=(6, 4 * N_inst))
        styles = ['full']
    else:
        if config.BASEMENT.settings['phase_variations']:
            fig, axes = plt.subplots(N_inst, 5, figsize=(30, 4 * N_inst))
            styles = ['full', 'phase', 'phase_variation', 'phasezoom', 'phasezoom_occ']
        elif config.BASEMENT.settings['secondary_eclipse']:
            fig, axes = plt.subplots(N_inst, 4, figsize=(24, 4 * N_inst))
            styles = ['full', 'phase', 'phasezoom', 'phasezoom_occ']
        else:
            fig, axes = plt.subplots(N_inst, 3, figsize=(18, 4 * N_inst))
            styles = ['full', 'phase', 'phasezoom']
        axes = np.atleast_2d(axes)
        for i, inst in enumerate(config.BASEMENT.settings['inst_all']):
            for j, style in enumerate(styles):
                if ('zoom' in style) & (inst in config.BASEMENT.settings['inst_rv']):
                    axes[(i, j)].axis('off')
                elif (inst in config.BASEMENT.settings['inst_phot']) & (companion not in config.BASEMENT.settings['companions_phot']):
                    axes[(i, j)].axis('off')
                elif (inst in config.BASEMENT.settings['inst_rv']) & (companion not in config.BASEMENT.settings['companions_rv']):
                    axes[(i, j)].axis('off')
                else:
                    plot_1(axes[(i, j)], samples, inst, companion, style)

    plt.tight_layout()
    return (
     fig, axes)


def plot_1(ax, samples, inst, companion, style, timelabel='Time'):
    """
    Inputs:
    -------
    ax : matplotlib axis
    
    samples : array
        Prior or posterior samples to plot the fit from
    
    inst: str
        Name of the instrument (e.g. 'TESS')
        
    companion : None or str
        None or 'b'/'c'/etc.
        
    style:
        'full' / 'phase' / 'phasezoom'
        
    timelabel:
        'Time' / 'Time_since'
        
            
    Notes:
    ------
    yerr / epoch / period: 
        come from the initial_guess value or the MCMC median (not from individual samples)

    """
    params_median, params_ll, params_ul = get_params_from_samples(samples)
    if inst in config.BASEMENT.settings['inst_phot']:
        key = 'flux'
        ylabel = 'Relative Flux'
    elif inst in config.BASEMENT.settings['inst_rv']:
        key = 'rv'
        ylabel = 'RV (km/s)'
    else:
        raise ValueError('inst should be listed in inst_phot or inst_rv...')
    if samples.shape[0] == 1:
        alpha = 1.0
    else:
        alpha = 0.1
    if style == 'full':
        x = config.BASEMENT.data[inst]['time']
        if timelabel == 'Time_since':
            x = np.copy(x)
            objttime = Time(x, format='jd', scale='utc')
            xsave = np.copy(x)
            x -= x[0]
        y = config.BASEMENT.data[inst][key]
        yerr_w = calculate_yerr_w(params_median, inst, key)
        ax.errorbar(x, y, yerr=yerr_w, fmt='b.', capsize=0, rasterized=True)
        if config.BASEMENT.settings['color_plot']:
            ax.scatter(x, y, c=x, marker='o', rasterized=True, cmap='inferno', zorder=11)
        if timelabel == 'Time_since':
            ax.set(xlabel='Time since %s [days]' % objttime[0].isot[:10], ylabel=ylabel, title=inst)
        else:
            if timelabel == 'Time':
                ax.set(xlabel='Time (BJD)', ylabel=ylabel, title=inst)
            if x[(-1)] - x[0] < 1:
                dt = 0.0013888888888888887
            else:
                dt = 0.020833333333333332
            xx = np.arange(x[0], x[(-1)] + dt, dt)
            for i in range(samples.shape[0]):
                s = samples[i, :]
                p = update_params(s)
                model = calculate_model(p, inst, key, xx=xx)
                baseline = calculate_baseline(p, inst, key, xx=xx)
                ax.plot(xx, model + baseline, 'r-', alpha=alpha, rasterized=True, zorder=12)

        if timelabel == 'Time_since':
            x = np.copy(xsave)
    else:
        x = config.BASEMENT.data[inst]['time']
        baseline_median = calculate_baseline(params_median, inst, key)
        y = config.BASEMENT.data[inst][key] - baseline_median
        yerr_w = calculate_yerr_w(params_median, inst, key)
        if 'phasezoom' in style:
            zoomfactor = params_median[(companion + '_period')] * 24.0
        else:
            zoomfactor = 1.0
        if inst in config.BASEMENT.settings['inst_rv']:
            for other_companion in config.BASEMENT.settings['companions_rv']:
                if companion != other_companion:
                    model = rv_fct(params_median, inst, other_companion)[0]
                    y -= model

            phase_time, phase_y, phase_y_err, _, phi = lct.phase_fold(x, y, params_median[(companion + '_period')], params_median[(companion + '_epoch')], dt=0.002, ferr_type='meansig', ferr_style='sem', sigmaclip=False)
            if len(x) > 500:
                ax.plot(phi * zoomfactor, y, 'b.', color='lightgrey', rasterized=True)
                ax.errorbar(phase_time * zoomfactor, phase_y, yerr=phase_y_err, fmt='b.', capsize=0, rasterized=True, zorder=11)
            else:
                ax.errorbar(phi * zoomfactor, y, yerr=yerr_w, fmt='b.', capsize=0, rasterized=True, zorder=11)
            ax.set(xlabel='Phase', ylabel=ylabel + '- Baseline', title=inst + ', companion ' + companion + ' only')
            xx = np.linspace(-0.25, 0.75, 1000)
            for i in range(samples.shape[0]):
                s = samples[i, :]
                p = update_params(s, phased=True)
                model = rv_fct(p, inst, companion, xx=xx)[0]
                ax.plot(xx * zoomfactor, model, 'r-', alpha=alpha, rasterized=True, zorder=12)

        elif inst in config.BASEMENT.settings['inst_phot']:
            if 'phase_variation' in style:
                dt = 0.01
            else:
                dt = 0.002
            phase_time, phase_y, phase_y_err, _, phi = lct.phase_fold(x, y, params_median[(companion + '_period')], params_median[(companion + '_epoch')], dt=dt, ferr_type='meansig', ferr_style='sem', sigmaclip=False)
            if len(x) > 500:
                if 'phase_variation' not in style:
                    ax.plot(phi * zoomfactor, y, 'b.', color='lightgrey', rasterized=True)
                    ax.errorbar(phase_time * zoomfactor, phase_y, yerr=phase_y_err, fmt='b.', capsize=0, rasterized=True, zorder=11)
                else:
                    ax.plot(phase_time * zoomfactor, phase_y, 'b.', rasterized=True, zorder=11)
            else:
                ax.errorbar(phi * zoomfactor, y, yerr=yerr_w, fmt='b.', capsize=0, rasterized=True, zorder=11)
                if config.BASEMENT.settings['color_plot']:
                    ax.scatter(phi * zoomfactor, y, c=x, marker='o', rasterized=True, cmap='inferno', zorder=11)
                ax.set(xlabel='Phase', ylabel=ylabel + '- Baseline', title=inst + ', companion ' + companion)
                if style == 'phasezoom':
                    xx = np.linspace(-4.0 / zoomfactor, 4.0 / zoomfactor, 1000)
                elif style == 'phasezoom_occ':
                    xx = np.linspace((-4.0 + zoomfactor / 2.0) / zoomfactor, (4.0 + zoomfactor / 2.0) / zoomfactor, 1000)
                else:
                    xx = np.linspace(-0.25, 0.75, 1000)
                for i in range(samples.shape[0]):
                    s = samples[i, :]
                    p = update_params(s, phased=True)
                    model = flux_fct(p, inst, companion, xx=xx)
                    ax.plot(xx * zoomfactor, model, 'r-', alpha=alpha, rasterized=True, zorder=12)

        if 'phasezoom' in style:
            ax.set(xlim=[-4, 4], xlabel='$\\mathrm{ T - T_0 \\ (h) }$')
        if 'phasezoom_occ' in style:
            ax.set(xlim=[-4 + zoomfactor / 2.0, 4 + zoomfactor / 2.0], ylim=[0.999, 1.0005], xlabel='$\\mathrm{ T - T_0 \\ (h) }$')
        if 'phase_variation' in style:
            ax.set(ylim=[0.9999, 1.0001])


def get_params_from_samples(samples):
    """
    read MCMC results and update params
    """
    theta_median = np.percentile(samples, 50, axis=0)
    theta_ul = np.percentile(samples, 16, axis=0)
    theta_ll = np.percentile(samples, 84, axis=0)
    params_median = update_params(theta_median)
    params_ll = update_params(theta_ll)
    params_ul = update_params(theta_ul)
    return (
     params_median, params_ll, params_ul)


def save_table(samples, mode):
    """
    Inputs:
    -------
    samples : array
        posterior samples
    mode : string
        'mcmc' or 'ns'
    """
    params, params_ll, params_ul = get_params_from_samples(samples)
    with open(os.path.join(config.BASEMENT.outdir, mode + '_table.csv'), 'w') as (f):
        f.write('############ Fitted parameters ############\n')
        for i, key in enumerate(config.BASEMENT.allkeys):
            if key not in config.BASEMENT.fitkeys:
                f.write(key + ',' + str(params[key]) + ',' + '(fixed),\n')
            else:
                f.write(key + ',' + str(params[key]) + ',' + str(params_ll[key]) + ',' + str(params_ul[key]) + '\n')


def save_latex_table(samples, mode):
    """
    Inputs:
    -------
    samples : array
        posterior samples
    mode : string
        'mcmc' or 'ns'
    """
    params_median, params_ll, params_ul = get_params_from_samples(samples)
    label = 'none'
    with open(os.path.join(config.BASEMENT.outdir, mode + '_latex_table.txt'), 'w') as (f):
        with open(os.path.join(config.BASEMENT.outdir, mode + '_latex_cmd.txt'), 'w') as (f_cmd):
            f.write('parameter & value & unit & fit/fixed \\\\ \n')
            f.write('\\hline \n')
            f.write('\\multicolumn{4}{c}{\\textit{Fitted parameters}} \\\\ \n')
            f.write('\\hline \n')
            for i, key in enumerate(config.BASEMENT.allkeys):
                if key not in config.BASEMENT.fitkeys:
                    value = str(params_median[key])
                    f.write(config.BASEMENT.labels[i] + ' & $' + value + '$ & ' + config.BASEMENT.units[i] + '& (fixed) \\\\ \n')
                    f_cmd.write('\\newcommand{\\' + key.replace('_', '') + '}{' + label + '$=' + value + '$} \n')
                else:
                    value = latex_printer.round_tex(params_median[key], params_ll[key], params_ul[key])
                    f.write(config.BASEMENT.labels[i] + ' & $' + value + '$ & ' + config.BASEMENT.units[i] + '& \\\\ \n')
                    f_cmd.write('\\newcommand{\\' + key.replace('_', '') + '}{' + label + '$=' + value + '$} \n')


def show_initial_guess(do_logprint=True, initial_guess_plot=True, return_figs=False):
    """
    Inputs:
    -------
    datadir : str
        the working directory for allesfitter
        must contain all the data files
        output directories and files will also be created inside datadir
            
    Outputs:
    --------
    This will output information into the console, 
    and create a file called datadir/results/initial_guess.pdf
    """
    if do_logprint:
        logprint('\nSettings:')
        logprint('--------------------------')
        for key in config.BASEMENT.settings:
            if config.BASEMENT.settings[key] != '':
                logprint(('{0: <30}').format(key), ('{0: <15}').format(str(config.BASEMENT.settings[key])))
            else:
                logprint(('\n{0: <30}').format(key))

        logprint('\nParameters:')
        logprint('--------------------------')
        for i, key in enumerate(config.BASEMENT.params):
            if key in config.BASEMENT.fitkeys:
                ind = np.where(config.BASEMENT.fitkeys == key)[0][0]
                logprint(('{0: <30}').format(key), ('{0: <15}').format(str(config.BASEMENT.params[key])), ('{0: <5}').format('free'), ('{0: <30}').format(str(config.BASEMENT.bounds[ind])))
            elif config.BASEMENT.params[key] != '':
                logprint(('{0: <30}').format(key), ('{0: <15}').format(str(config.BASEMENT.params[key])), ('{0: <5}').format('set'))
            else:
                logprint(('\n{0: <30}').format(key))

        logprint('\nndim:', config.BASEMENT.ndim)
    if initial_guess_plot == True:
        samples = draw_initial_guess_samples()
        if return_figs == False:
            for companion in config.BASEMENT.settings['companions_all']:
                fig, axes = afplot(samples, companion)
                fig.savefig(os.path.join(config.BASEMENT.outdir, 'initial_guess_' + companion + '.pdf'), bbox_inches='tight')
                plt.close(fig)

        else:
            fig_list = []
            for companion in config.BASEMENT.settings['companions_all']:
                fig, axes = afplot(samples, companion)
                fig_list.append(fig)

            return fig_list


def get_labels(datadir, as_type='dic'):
    config.init(datadir)
    if as_type == '2d_array':
        return config.BASEMENT.labels
    if as_type == 'dic':
        labels_dic = {}
        for key in config.BASEMENT.fitkeys:
            ind = np.where(config.BASEMENT.allkeys == key)[0]
            labels_dic[key] = config.BASEMENT.labels[ind][0]

        return labels_dic