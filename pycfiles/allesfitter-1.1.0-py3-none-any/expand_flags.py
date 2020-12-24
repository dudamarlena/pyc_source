# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/exoworlds/lightcurves/expand_flags.py
# Compiled at: 2018-11-07 16:09:23
"""
Created on Thu Oct 11 19:51:37 2018

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
import numpy as np

def expand_flags(flag, n=4):
    maskleft = np.where(flag > 0)[0]
    flag_new = np.zeros(len(flag), dtype=bool)
    for i in range(-n, n + 1):
        thismask = maskleft + i
        for t in thismask:
            if t < len(flag_new):
                flag_new[t] = 1

    return flag_new