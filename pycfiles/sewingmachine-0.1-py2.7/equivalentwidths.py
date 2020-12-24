# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sewingmachine/equivalentwidths.py
# Compiled at: 2018-01-26 12:54:57
import numpy as np
from scipy.interpolate import interp1d

def specewmeasure(spec, integration, windows, sigmaclip=True, sigma=2):
    spec_x = spec[:, 0]
    spec_y = spec[:, 1]
    norm_pix = []
    norm_lambda = []
    windowmask = np.zeros(len(spec_x), dtype=bool)
    for i in windows:
        windowmask[(spec_x < i[1]) & (spec_x > i[0])] = 1

    cont_fit = np.polyfit(spec_x[windowmask], spec_y[windowmask], 1)
    cont_poly = np.poly1d(cont_fit)
    if sigmaclip == True:
        std = sigma * np.nanstd(spec_y[windowmask])
        residual = np.fabs(spec_y[windowmask] - cont_poly(spec_x[windowmask]))
        clip = residual < std
        windowmask[windowmask][clip] = 0
        cont_fit = np.polyfit(spec_x[windowmask], spec_y[windowmask], 1)
        cont_poly = np.poly1d(cont_fit)
    intmask = np.zeros(len(spec_x), dtype=bool)
    intmask[(spec_x <= integration[1]) & (spec_x >= integration[0])] = 1
    interpol = interp1d(spec_x, spec_y, kind='linear')
    line_x = np.zeros(len(spec_x[intmask]) + 2)
    line_y = np.zeros(len(spec_x[intmask]) + 2)
    line_x[1:(-1)] = spec_x[intmask]
    line_y[1:(-1)] = spec_y[intmask]
    line_x[0] = integration[0]
    line_x[-1] = integration[1]
    line_y[0] = interpol(integration[0])
    line_y[-1] = interpol(integration[1])
    cont_y = cont_poly(line_x)
    line_y = line_y / cont_y
    contarea = max(line_x) - min(line_x)
    linearea = np.trapz(1 - line_y, x=line_x)
    return linearea