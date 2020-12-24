# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/simulate.py
# Compiled at: 2019-10-30 10:44:51
# Size of source mod 2**32: 1992 bytes
__doc__ = '\nCreated on Tue Oct 29 17:24:48 2019\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
import os, sys, ellc
from flares.aflare import aflare1

def transit_model(time, rr=0.1, rsuma=0.1, cosi=0, epoch=0, period=1, ldc=[0.5, 0.5]):
    params = {'b_rr':rr, 
     'b_rsuma':rsuma, 
     'b_cosi':cosi, 
     'b_epoch':epoch, 
     'b_period':period}
    companion = 'b'
    params[companion + '_radius_1'] = params[(companion + '_rsuma')] / (1.0 + params[(companion + '_rr')])
    params[companion + '_radius_2'] = params[(companion + '_radius_1')] * params[(companion + '_rr')]
    params[companion + '_incl'] = np.arccos(params[(companion + '_cosi')]) / np.pi * 180.0
    model_flux = ellc.lc(t_obs=time,
      radius_1=(params[(companion + '_radius_1')]),
      radius_2=(params[(companion + '_radius_2')]),
      sbratio=0.0,
      incl=(params[(companion + '_incl')]),
      t_zero=(params[(companion + '_epoch')]),
      period=(params[(companion + '_period')]),
      ldc_1=ldc,
      ld_1='quad',
      verbose=False)
    return model_flux


def flare_model(time, tpeak, fwhm, ampl):
    return aflare1(time, tpeak, fwhm, ampl, upsample=True, uptime=10)