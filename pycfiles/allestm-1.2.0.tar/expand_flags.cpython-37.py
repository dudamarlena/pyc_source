# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/exoworlds/lightcurves/expand_flags.py
# Compiled at: 2018-11-07 16:09:23
# Size of source mod 2**32: 860 bytes
__doc__ = '\nCreated on Thu Oct 11 19:51:37 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research,\nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109,\nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import numpy as np

def expand_flags(flag, n=4):
    maskleft = np.where(flag > 0)[0]
    flag_new = np.zeros((len(flag)), dtype=bool)
    for i in range(-n, n + 1):
        thismask = maskleft + i
        for t in thismask:
            if t < len(flag_new):
                flag_new[t] = 1

    return flag_new