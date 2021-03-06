# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/transit_search/transit_search.py
# Compiled at: 2020-02-27 21:44:51
# Size of source mod 2**32: 9949 bytes
"""
Created on Fri Feb 14 17:55:39 2020

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
import os, numpy as np
import matplotlib.pyplot as plt
from transitleastsquares import transitleastsquares as tls
from transitleastsquares import transit_mask, cleaned_array, catalog_info
try:
    from exoworlds.tess import tessio
except:
    pass

def mask(time, flux, period, duration, T0):
    intransit = transit_mask(time, period, duration, T0)
    time = time[(~intransit)]
    flux = flux[(~intransit)]
    time, flux = cleaned_array(time, flux)
    return (time, flux)


def tls_search(time, flux, flux_err, SNR_threshold=5.0, known_transits=None, R_star=1.0, R_star_min=0.13, R_star_max=3.5, M_star=1.0, M_star_min=0.1, M_star_max=1.0, show_plot=False, save_plot=False, outdir=''):
    """
    Summary:
    -------
    This runs TLS on these data with the given infos
    
    Inputs:
    -------
    time : array of flaot
        time stamps of observations
    flux : array of flaot
        normalized flux
    flux_err : array of flaot
        error of normalized flux
        
        
    Optional Inputs:
    ----------------
    SNR_threshold : float
        the SNR threshold at which to stop the TLS search
    known_transits : None or dict
        if dict and one transit is already known: 
            known_transits = {'period':[1.3], 'duration':[2.1], 'epoch':[245800.0]}
        if dict and multiple transits are already known: 
            known_transits = {'period':[1.3, 21.0], 'duration':[2.1, 4.1], 'epoch':[245800.0, 245801.0]}
        'period' is the period of the transit
        'duration' must be the total duration, i.e. from first ingress point to last egrees point, in days
        'epoch' is the epoch of the transit
    R_star : float
        radius of the star (e.g. median)
        default 1 R_sun (from TLS)
    R_star_min : float
        minimum radius of the star (e.g. 1st percentile)
        default 0.13 R_sun (from TLS)
    R_star_max : float
        maximum radius of the star (e.g. 99th percentile)
        default 3.5 R_sun (from TLS)
    M_star : float
        mass of the star (e.g. median)
        default 1. M_sun (from TLS)
    M_star_min : float
        minimum mass of the star (e.g. 1st percentile)
        default 0.1 M_sun (from TLS)
    M_star_max : float
        maximum mass of the star (e.g. 99th percentile)
        default 1. M_sun (from TLS)         
    show_plot : bool
        show a plot of each phase-folded transit candidate and TLS model in the terminal 
    show_plot : bool
        save a plot of each phase-folded transit candidate and TLS model into outdir
    outdir : string
        if None, use the current working directory
        
    Returns:
    -------
    List of all TLS results
    """
    SNR = 1000000000000.0
    FOUND_SIGNAL = False
    results_all = []
    if len(outdir) > 0:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    if known_transits is not None:
        for period, duration, T0 in zip(known_transits['period'], known_transits['duration'], known_transits['epoch']):
            time, flux = mask(time, flux, period, duration, T0)

    i = 0
    while SNR >= SNR_threshold:
        if FOUND_SIGNAL == False:
            model = tls(time, flux)
            results = model.power(R_star=R_star, R_star_min=R_star_min, R_star_max=R_star_max, M_star=M_star,
              M_star_min=M_star_min,
              M_star_max=M_star_max,
              n_transits_min=1,
              quiet=True,
              show_progress_bar=False)
            if results.snr >= SNR_threshold:
                time, flux = mask(time, flux, results.period, 2 * results.duration, results.T0)
                results_all.append(results)
                if show_plot or save_plot:
                    fig, ax = plt.subplots()
                    ax.plot(results['folded_phase'], results['folded_y'], 'b.')
                    ax.plot((results['model_folded_phase']), (results['model_folded_model']), 'r-', lw=2)
                    ax.text(1.02, 0.95, ('P = ' + np.format_float_positional(results['period'], 4) + ' d'), ha='left', va='center', transform=(ax.transAxes))
                    ax.text(1.02, 0.85, ('Depth = ' + np.format_float_positional(1000.0 * (1.0 - results['depth']), 4) + ' ppt'), ha='left', va='center', transform=(ax.transAxes))
                    ax.text(1.02, 0.75, ('Duration = ' + np.format_float_positional(1440 * (1.0 - results['duration']), 4) + ' ppt'), ha='left', va='center', transform=(ax.transAxes))
                    ax.text(1.02, 0.65, ('T_0 = ' + np.format_float_positional(results['T0'], 4) + ' d'), ha='left', va='center', transform=(ax.transAxes))
                    ax.text(1.02, 0.55, ('SNR = ' + np.format_float_positional(results['snr'], 4)), ha='left', va='center', transform=(ax.transAxes))
                    if save_plot:
                        fig.savefig((os.path.join(outdir, 'tls_signal_' + str(i))), bbox_inches='tight')
                    if show_plot:
                        plt.show(fig)
        else:
            plt.close(fig)
        SNR = results.snr
        i += 1

    return results_all


def tls_search_by_tic(tic_id, time=None, flux=None, flux_err=None, SNR_threshold=5.0, known_transits=None, show_plot=False, save_plot=False, outdir=''):
    """
    Inputs:
    -------
    tic_id : str
        TIC ID
        
    Optional Inputs:
    ----------------
    time : array of flaot
        time stamps of observations (to overwrite the SPOC PDC SAP lightcurve)
    flux : array of flaot
        normalized flux (to overwrite the SPOC PDC SAP lightcurve)
    flux_err : array of flaot
        error of normalized flux (to overwrite the SPOC PDC SAP lightcurve)
    SNR_threshold : float
        the SNR threshold at which to stop the TLS search
    known_transits : None or dict
        if dict and one transit is already known: 
            known_transits = {'period':[1.3], 'duration':[2.1], 'epoch':[245800.0]}
        if dict and multiple transits are already known: 
            known_transits = {'period':[1.3, 21.0], 'duration':[2.1, 4.1], 'epoch':[245800.0, 245801.0]}
        'period' is the period of the transit
        'duration' must be the total duration, i.e. from first ingress point to last egrees point, in days
        'epoch' is the epoch of the transit
        
    Summary:
    -------
        - retrieves the SPOC PDC-SAP lightcurve
        - retrieves all TIC catalog information from MAST
        - runs TLS on these data and infos
    
    Returns:
    -------
        - list of all TLS results
    """
    tic_id = str(int(tic_id))
    dic = tessio.get(tic_id, pipeline='spoc', PDC=True)
    if time is None:
        time = dic['time']
    if flux is None:
        flux = dic['flux']
    if flux_err is None:
        flux_err = dic['flux_err']
    ab, R_star, R_star_lerr, R_star_uerr, M_star, M_star_lerr, M_star_uerr = catalog_info(TIC_ID=(int(tic_id)))
    print('TICv8 info:')
    print('Quadratic limb darkening a, b', ab[0], ab[1])
    print('Stellar radius', R_star, '+', R_star_lerr, '-', R_star_uerr)
    print('Stellar mass', M_star, '+', M_star_lerr, '-', M_star_uerr)
    return tls_search(time, flux, flux_err, R_star=R_star,
      R_star_min=(R_star - R_star_lerr),
      R_star_max=(R_star + R_star_uerr),
      M_star=M_star,
      M_star_min=(M_star - M_star_lerr),
      M_star_max=(M_star + M_star_uerr),
      known_transits=known_transits,
      show_plot=show_plot,
      save_plot=save_plot,
      outdir=outdir)


if __name__ == '__main__':
    pass