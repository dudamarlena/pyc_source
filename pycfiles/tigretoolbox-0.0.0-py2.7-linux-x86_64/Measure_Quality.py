# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Utilities/Measure_Quality.py
# Compiled at: 2017-06-20 08:49:49
"""
%--------------------------------------------------------------------------
% This file is part of the TIGRE Toolbox
%
% Copyright (c) 2015, University of Bath and
%                     CERN-European Organization for Nuclear Research
%                     All rights reserved.
%
% License:            Open Source under BSD.
%                     See the full license at
%                     https://github.com/CERN/TIGRE/license.txt
%
% Contact:            tigre.toolbox@gmail.com
% Codes:              https://github.com/CERN/TIGRE/
% Coded by:           MATLAB (original): Manasavee Lohvithee
                      Python: Reuben Lindroos
%--------------------------------------------------------------------------
"""
from __future__ import division
import numpy as np

def Measure_Quality(res_prev, res, QualMeasOpts):
    if QualMeasOpts == 'RMSE':
        N = len(res_prev.ravel())
        diff = res_prev - res
        return np.sqrt(sum(diff.ravel() ** 2) / N)
    if QualMeasOpts == 'CC':
        return np.corrcoef(res_prev.ravel(), res.ravel())
    if QualMeasOpts == 'MSSIM':
        N = len(res_prev.ravel())
        res_prev = res_prev.ravel()
        res = res.ravel()
        mean_res_p = res_prev.mean(axis=0)
        mean_res = res.mean(axis=0)
        if mean_res == 0 and mean_res_p == 0:
            raise ValueError('Initialising with 0 matrix not valid')
        K1 = 0.01
        d = max(res_prev) - min(res_prev)
        l = (2 * mean_res * mean_res_p + (K1 * d) ** 2) / (mean_res_p ** 2 + mean_res ** 2 + K1 * d ** 2)
        K2 = 0.02
        sres_p = res_prev.std(axis=0)
        sres = res.std(axis=0)
        c = (2 * sres_p * sres + (K2 * d) ** 2) / (sres_p ** 2 + sres ** 2 + K2 * d ** 2)
        diffres_p = res_prev - mean_res_p
        diffres = res - mean_res
        delta = 1 / (N - 1) * sum(diffres_p * diffres)
        s = (delta + (K2 * d) ** 2 / 2) / (sres_p * sres + K2 * d ** 2 / 2)
        return 1 / N * l * c * s
    if QualMeasOpts == 'UQI':
        res = res.ravel()
        res_prev = res_prev.ravel()
        N = len(res_prev)
        mean_res_p = np.mean(res_prev, dtype=np.float32)
        mean_res = np.mean(res, dtype=np.float32)
        varres_p = np.var(res_prev)
        varres = np.var(res)
        if mean_res == 0 and mean_res_p == 0:
            raise ValueError('Initialising with 0 matrix not valid')
        cova = sum(res - mean_res) * (res_prev - mean_res_p) / (N - 1)
        front = 2 * cova / (varres + varres_p)
        back = 2 * mean_res * mean_res_p / (mean_res ** 2 + mean_res_p ** 2)
        return sum(front * back)