# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/priors/transform_priors.py
# Compiled at: 2018-11-07 16:44:32
"""
Created on Tue Oct  2 22:10:28 2018

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
import numpy as np
from .simulate_PDF import simulate_PDF as spdf

def get_cosi_from_i(i, Nsamples=10000):
    i = spdf(i[0], i[1], i[2], size=Nsamples, plot=False)
    cosi = np.cos(np.deg2rad(i))
    ll, median, ul = np.percentile(cosi, [16, 50, 84])
    return (median, median - ll, ul - median)


def get_Rsuma_from_a_over_Rstar(a_over_Rstar, Rp_over_Rstar, Nsamples=10000):
    a_over_Rstar = spdf(a_over_Rstar[0], a_over_Rstar[1], a_over_Rstar[2], size=Nsamples, plot=False)
    Rstar_over_a = 1.0 / a_over_Rstar
    Rp_over_Rstar = spdf(Rp_over_Rstar[0], Rp_over_Rstar[1], Rp_over_Rstar[2], size=Nsamples, plot=False)
    Rsuma = Rstar_over_a * (1.0 + Rp_over_Rstar)
    ll, median, ul = np.percentile(Rsuma, [16, 50, 84])
    return (median, median - ll, ul - median)


def get_Rsuma_from_Rstar_over_a(Rstar_over_a, Rp_over_Rstar, Nsamples=10000):
    Rstar_over_a = spdf(Rstar_over_a[0], Rstar_over_a[1], Rstar_over_a[2], size=Nsamples, plot=False)
    Rp_over_Rstar = spdf(Rp_over_Rstar[0], Rp_over_Rstar[1], Rp_over_Rstar[2], size=Nsamples, plot=False)
    Rsuma = Rstar_over_a * (1.0 + Rp_over_Rstar)
    ll, median, ul = np.percentile(Rsuma, [16, 50, 84])
    return (median, median - ll, ul - median)