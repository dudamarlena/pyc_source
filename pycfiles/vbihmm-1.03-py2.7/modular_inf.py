# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/modular_inf.py
# Compiled at: 2013-12-18 03:16:06
"""
Created on Oct 17, 2013

@author: James McInerney
"""
from numpy import *

def infer(latents, visuals=None, thres=1e-06, itr=0, max_itr=200, min_itr=10, VERBOSE=0, startEstep=0, showThres=1.0, presetLatents=0):
    diff = 9999.0
    while itr < min_itr or itr < max_itr and diff > thres:
        prev_ln_obs_lik = latents.ln_obs_lik().copy()
        if itr > 0 or startEstep == 0:
            latents.m()
        latents.e()
        if visuals is not None:
            visuals.update(itr, showThres)
        diff = latents.diff()
        ks, = where(latents.expZ().sum(axis=0) > 0.5)
        print 'itr,diff,NK', itr, diff, len(ks)
        itr += 1

    return itr