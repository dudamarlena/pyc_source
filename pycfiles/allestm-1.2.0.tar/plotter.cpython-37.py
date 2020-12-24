# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/plotter.py
# Compiled at: 2020-03-25 15:21:42
# Size of source mod 2**32: 6253 bytes
__doc__ = '\nCreated on Thu Mar  5 17:22:59 2020\n\n@author: \nDr. Maximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nGitHub: https://github.com/MNGuenther\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from .translator import translate
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})

def plot_lc_full(ax, time, flux, flux_err, time_grid, model_flux_grid):
    ax.errorbar(time, flux, yerr=flux_err, fmt='b.', rasterized=True, zorder=11)
    ax.plot(time_grid, model_flux_grid, 'r-', lw=2, zorder=12)
    ax.set(xlabel='Time $\\mathrm{(BJD_{TDB})}$', ylabel='Flux')
    return ax


def plot_lc_phase(ax, phi, flux, phase, phaseflux, phaseflux_err, phase_grid, model_phaseflux_grid):
    ax.plot(phi, flux, 'k.', color='lightgrey', rasterized=True, zorder=10)
    ax.errorbar(phase, phaseflux, yerr=phaseflux_err, fmt='b.', zorder=11)
    ax.plot(phase_grid, model_phaseflux_grid, 'r-', lw=2, zorder=12)
    ax.set(xlabel='Phase', ylabel='Flux')
    return ax


def plot_lc_phasezoom(ax, phi, flux, phase, phaseflux, phaseflux_err, phase_grid, model_phaseflux_grid, zoomfactor):
    """
    zoomfactor : period * 24 * 60
    """
    ax.plot((phi * zoomfactor), flux, 'k.', color='lightgrey', rasterized=True, zorder=10)
    ax.errorbar((phase * zoomfactor), phaseflux, yerr=phaseflux_err, fmt='b.', zorder=11)
    ax.plot((phase_grid * zoomfactor), model_phaseflux_grid, 'r-', lw=2, zorder=12)
    ax.set(xlim=[-240, 240])
    ax.set(xlabel='Time (min.)', ylabel='Flux')
    return ax


def plot_rv_full(ax, time, rv, rv_err, time_grid, model_flux_grid):
    ax.errorbar(time, rv, yerr=rv_err, fmt='bo', zorder=11)
    ax.plot(time_grid, model_flux_grid, 'r-', lw=2, zorder=12)
    ax.set(xlabel='Time $\\mathrm{(BJD_{TDB})}$', ylabel='RV (km/s)')
    return ax


def plot_rv_phase(ax, phi, rv, rv_err, phase_grid, model_phaserv_grid):
    ax.errorbar(phi, rv, yerr=rv_err, fmt='bo', zorder=11)
    ax.plot(phase_grid, model_phaserv_grid, 'r-', lw=2, zorder=12)
    ax.set(xlabel='Phase', ylabel='RV (km/s)')
    return ax


def plot_info(ax, text=0, params=None, **params_kwargs):
    params = translate(params=params, quiet=True, **params_kwargs)
    ax.set_axis_off()
    if text == 0:
        ax.text(0, 0.95, ('R_comp = ' + str(params['R_companion']) + ' ' + params['R_companion_unit']), transform=(ax.transAxes))
        ax.text(0, 0.85, ('M_comp = ' + str(params['M_companion']) + ' ' + params['M_companion_unit']), transform=(ax.transAxes))
        ax.text(0, 0.75, ('R_host = ' + str(params['R_host']) + ' Rsun'), transform=(ax.transAxes))
        ax.text(0, 0.65, ('M_host = ' + str(params['M_host']) + ' Msun'), transform=(ax.transAxes))
        ax.text(0, 0.55, ('sbratio = ' + str(params['sbratio'])), transform=(ax.transAxes))
        ax.text(0, 0.45, ('epoch = ' + str(params['epoch']) + ' $\\mathrm{BJD_{TDB}}$'), transform=(ax.transAxes))
        ax.text(0, 0.35, ('period = ' + str(params['period']) + ' days'), transform=(ax.transAxes))
        ax.text(0, 0.25, ('incl = ' + str(params['incl']) + ' deg'), transform=(ax.transAxes))
        ax.text(0, 0.15, ('ecc = ' + str(params['ecc'])), transform=(ax.transAxes))
        ax.text(0, 0.05, ('omega = ' + str(params['omega']) + ' deg'), transform=(ax.transAxes))
    if text == 1:
        ax.text(0, 0.95, ('dil = ' + str(params['dil'])), transform=(ax.transAxes))
        ax.text(0, 0.85, ('R_comp/R_host = ' + np.format_float_positional(params['R_companion/R_host'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.75, ('(R_comp+R_host)/a = ' + np.format_float_positional(params['(R_host+R_companion)/a'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.65, ('R_comp/a = ' + np.format_float_positional(params['R_companion/a'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.55, ('R_host/a = ' + np.format_float_positional(params['R_host/a'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.45, ('cosi = ' + np.format_float_positional(params['cosi'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.35, ('$\\sqrt{e} \\cos{\\omega}$ = ' + np.format_float_positional(params['f_c'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.25, ('$\\sqrt{e} \\sin{\\omega}$ = ' + np.format_float_positional(params['f_s'], 5, False)), transform=(ax.transAxes))
        ax.text(0, 0.15, ('LD = ' + str(params['ldc']) + ' ' + params['ld']), transform=(ax.transAxes))
        ax.text(0, 0.05, ('LD transf = [' + ', '.join([np.format_float_positional(item, 5, False) for item in params['ldc_transformed']]) + ']'), transform=(ax.transAxes))
    return ax