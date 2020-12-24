# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/priors/transform_priors.py
# Compiled at: 2020-03-06 12:48:24
# Size of source mod 2**32: 7819 bytes
__doc__ = '\nCreated on Tue Oct  2 22:10:28 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
from .simulate_PDF import simulate_PDF as spdf

def get_cosi_from_i(i, Nsamples=10000):
    """
    i : float or list of form [median, lower_err, upper_err] in degree
    """
    i = spdf((i[0]), (i[1]), (i[2]), size=Nsamples, plot=False)
    ind_good = np.where((i >= 0) & (i <= 90))[0]
    i = i[ind_good]
    cosi = np.cos(np.deg2rad(i))
    ll, median, ul = np.percentile(cosi, [16, 50, 84])
    return (
     median, median - ll, ul - median)


def get_cosi_from_b(b, a_over_Rstar, Nsamples=10000):
    b = spdf((b[0]), (b[1]), (b[2]), size=Nsamples, plot=False)
    a_over_Rstar = spdf((a_over_Rstar[0]), (a_over_Rstar[1]), (a_over_Rstar[2]), size=Nsamples, plot=False)
    ind_good = np.where((b >= 0) & (a_over_Rstar > 0))[0]
    b = b[ind_good]
    a_over_Rstar = a_over_Rstar[ind_good]
    cosi = b / a_over_Rstar
    ll, median, ul = np.percentile(cosi, [16, 50, 84])
    return (
     median, median - ll, ul - median)


def get_Rsuma_from_a_over_Rstar(a_over_Rstar, Rp_over_Rstar, Nsamples=10000):
    a_over_Rstar = spdf((a_over_Rstar[0]), (a_over_Rstar[1]), (a_over_Rstar[2]), size=Nsamples, plot=False)
    Rp_over_Rstar = spdf((Rp_over_Rstar[0]), (Rp_over_Rstar[1]), (Rp_over_Rstar[2]), size=Nsamples, plot=False)
    ind_good = np.where((Rp_over_Rstar >= 0) & (a_over_Rstar > 0))[0]
    Rp_over_Rstar = Rp_over_Rstar[ind_good]
    a_over_Rstar = a_over_Rstar[ind_good]
    Rsuma = 1.0 / a_over_Rstar * (1.0 + Rp_over_Rstar)
    ll, median, ul = np.percentile(Rsuma, [16, 50, 84])
    return (
     median, median - ll, ul - median)


def get_Rsuma_from_Rstar_over_a(Rstar_over_a, Rp_over_Rstar, Nsamples=10000):
    Rstar_over_a = spdf((Rstar_over_a[0]), (Rstar_over_a[1]), (Rstar_over_a[2]), size=Nsamples, plot=False)
    Rp_over_Rstar = spdf((Rp_over_Rstar[0]), (Rp_over_Rstar[1]), (Rp_over_Rstar[2]), size=Nsamples, plot=False)
    ind_good = np.where((Rp_over_Rstar >= 0) & (Rstar_over_a > 0))[0]
    Rp_over_Rstar = Rp_over_Rstar[ind_good]
    Rstar_over_a = Rstar_over_a[ind_good]
    Rsuma = Rstar_over_a * (1.0 + Rp_over_Rstar)
    ll, median, ul = np.percentile(Rsuma, [16, 50, 84])
    return (
     median, median - ll, ul - median)


def get_sqrtesinw(e, w, Nsamples=10000):
    e = spdf((e[0]), (e[1]), (e[2]), size=Nsamples, plot=False)
    w = spdf((w[0]), (w[1]), (w[2]), size=Nsamples, plot=False)
    ind_good = np.where((e >= 0) & (w >= 0) & (w <= 360))[0]
    e = e[ind_good]
    w = w[ind_good]
    sqrtesinw = np.sqrt(e) * np.sin(np.deg2rad(w))
    ll, median, ul = np.percentile(sqrtesinw, [16, 50, 84])
    return (
     median, median - ll, ul - median)


def get_sqrtecosw(e, w, Nsamples=10000):
    e = spdf((e[0]), (e[1]), (e[2]), size=Nsamples, plot=False)
    w = spdf((w[0]), (w[1]), (w[2]), size=Nsamples, plot=False)
    ind_good = np.where((e >= 0) & (e <= 1) & (w >= 0) & (w <= 360))[0]
    e = e[ind_good]
    w = w[ind_good]
    sqrtecosw = np.sqrt(e) * np.cos(np.deg2rad(w))
    ll, median, ul = np.percentile(sqrtecosw, [16, 50, 84])
    return (
     median, median - ll, ul - median)


def get_u1u2_from_q1q2(q1, q2, Nsamples=10000):
    """
    q1, q2: float or list of form [median, lower_err, upper_err]
    """
    if type(q1) == float:
        if type(q2) == float:
            u1 = 2.0 * np.sqrt(q1) * q2
            u2 = np.sqrt(q1) * (1.0 - 2.0 * q2)
            return (
             u1, u2)
    q1 = spdf((q1[0]), (q1[1]), (q1[2]), size=Nsamples, plot=False)
    q2 = spdf((q2[0]), (q2[1]), (q2[2]), size=Nsamples, plot=False)
    ind_good = np.where((q1 >= 0) & (q1 <= 1) & (q2 >= 0) & (q2 <= 1))[0]
    q1 = q1[ind_good]
    q2 = q2[ind_good]
    u1 = 2.0 * np.sqrt(q1) * q2
    u2 = np.sqrt(q1) * (1.0 - 2.0 * q2)
    u1_ll, u1_median, u1_ul = np.percentile(u1, [16, 50, 84])
    u2_ll, u2_median, u2_ul = np.percentile(u2, [16, 50, 84])
    return (
     (
      u1_median, u1_median - u1_ll, u1_ul - u1_median), (u2_median, u2_median - u2_ll, u2_ul - u2_median))


def get_q1q2_from_u1u2(u1, u2, Nsamples=10000):
    """
    u1, u2: float or list of form [median, lower_err, upper_err]
    """
    if type(u1) == float:
        if type(u2) == float:
            q1 = (u1 + u2) ** 2
            q2 = 0.5 * u1 / (u1 + u2)
            return (
             q1, q2)
    u1 = spdf((u1[0]), (u1[1]), (u1[2]), size=Nsamples, plot=True)
    u2 = spdf((u2[0]), (u2[1]), (u2[2]), size=Nsamples, plot=True)
    ind_good = np.where((u1 >= 0) & (u1 <= 1) & (u2 >= 0) & (u2 <= 1))[0]
    u1 = u1[ind_good]
    u2 = u2[ind_good]
    q1 = (u1 + u2) ** 2
    q2 = 0.5 * u1 / (u1 + u2)
    q1_ll, q1_median, q1_ul = np.percentile(q1, [16, 50, 84])
    q2_ll, q2_median, q2_ul = np.percentile(q2, [16, 50, 84])
    return (
     (
      q1_median, q1_median - q1_ll, q1_ul - q1_median), (q2_median, q2_median - q2_ll, q2_ul - q2_median))