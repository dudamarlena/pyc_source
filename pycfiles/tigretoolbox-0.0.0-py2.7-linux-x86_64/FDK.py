# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Algorithms/FDK.py
# Compiled at: 2017-06-22 08:00:54
from __future__ import division
from __future__ import print_function
import os, sys, math, numpy as np, copy
from _Ax import Ax
from _Atb import Atb
from tigre.Utilities.filtering import filtering
import scipy.io
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path:
    sys.path.append(rootDir)

def FDK(proj, geo, angles, filter=None):
    if filter is not None:
        geo.filter = filter
    proj = proj.transpose()
    proj = proj.transpose(0, 2, 1)
    for ii in range(len(angles)):
        xv = np.arange(-geo.nDetector[0] / 2 + 0.5, 1 + geo.nDetector[0] / 2 - 0.5) * geo.dDetector[0]
        yv = np.arange(-geo.nDetector[1] / 2 + 0.5, 1 + geo.nDetector[1] / 2 - 0.5) * geo.dDetector[1]
        xx, yy = np.meshgrid(xv, yv)
        w = geo.DSD / np.sqrt(geo.DSD ** 2 + xx ** 2 + yy ** 2)
        proj[ii] = proj[ii] * w.transpose()

    proj_filt = filtering(proj.transpose(0, 2, 1), geo, angles, parker=False).transpose()
    return Atb(proj_filt, geo, angles, 'FDK')