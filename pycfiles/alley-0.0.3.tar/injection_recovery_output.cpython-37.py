# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/transit_search/injection_recovery_output.py
# Compiled at: 2020-02-17 11:23:19
# Size of source mod 2**32: 8791 bytes
__doc__ = '\nCreated on Thu May  9 10:01:30 2019\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
import warnings

def is_multiple_of(a, b, tolerance=0.05):
    a = np.float(a)
    b = np.float(b)
    result = a % b
    return abs(result / b) <= tolerance or 


def is_detected(inj_period, tls_period):
    right_period = is_multiple_of(tls_period, inj_period / 2.0)
    if right_period:
        return True
    return False


def is_detected_list(inj_periods, tls_periods):
    detected = []
    for i in range(len(inj_periods)):
        detected.append(is_detected(inj_periods[i], tls_periods[i]))

    return np.array(detected)


def irplot(fname, period_bins=None, rplanet_bins=None, outdir=None):
    results = np.genfromtxt(fname, delimiter=',', dtype=None, names=True)
    inj_periods = results['inj_period']
    inj_rplanets = results['inj_rplanet']
    tls_periods = results['tls_period']
    detected = is_detected_list(inj_periods, tls_periods)
    period = []
    rplanet = []
    found = []
    for p in np.unique(inj_periods):
        for r in np.unique(inj_rplanets):
            period.append(p)
            rplanet.append(r)
            ind = np.where((inj_periods == p) & (inj_rplanets == r))[0]
            f = any(detected[ind])
            found.append(f)

    period = np.array(period)
    rplanet = np.array(rplanet)
    found = np.array(found)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(period, rplanet, c=found, s=100, cmap='Blues_r', edgecolors='b')
    ax.set(xlabel='Period (days)', ylabel='Radius $(R_\\oplus)$')
    ax.text(0.5, 1.05, 'filled: not recovered | unfilled: recovered', ha='center', va='center', transform=(ax.transAxes))
    fig.savefig('injection_recovery_test_scatter.pdf', bbox_inches='tight')
    if len(np.unique(inj_periods)) * len(np.unique(inj_periods)) < 100:
        print('\n!-- WARNING: not enough samples to create a 2D histogram plot. --!\n')
    else:
        if period_bins is not None and rplanet_bins is not None:
            bins = [
             period_bins, rplanet_bins]
        else:
            bins = [
             np.histogram_bin_edges(period, bins='auto'), np.histogram_bin_edges(rplanet, bins='auto')]
        h1, x, y = np.histogram2d((period[(found == 1)]), (rplanet[(found == 1)]), bins=bins)
        h2, x, y = np.histogram2d((period[(found == 0)]), (rplanet[(found == 0)]), bins=bins)
        normed_hist = 100.0 * h1 / (h1 + h2)
        fig, ax = plt.subplots(figsize=(6.5, 5))
        im = plt.imshow((normed_hist.T), origin='lower', extent=(x[0], x[(-1)], y[0], y[(-1)]), interpolation='none', aspect='auto', cmap='Blues_r', vmin=0, vmax=100, rasterized=True)
        plt.colorbar(im, label='Recovery rate (%)')
        plt.xlabel('Injected period (days)')
        plt.ylabel('Injected radius (R$_\\oplus$)')
        fig.savefig('injection_recovery_test_hist2d.pdf', bbox_inches='tight')