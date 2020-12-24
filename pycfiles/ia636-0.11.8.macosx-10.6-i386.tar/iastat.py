# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robertoalotufo/Library/Enthought/Canopy_32bit/User/lib/python2.7/site-packages/ia636/iastat.py
# Compiled at: 2014-08-21 22:30:04
from numpy import *

def iastat(f1, f2):
    f1_, f2_ = 1.0 * ravel(f1), 1.0 * ravel(f2)
    MSE = sum((f1_ - f2_) ** 2) / product(f1.shape[:2])
    if MSE == 0:
        PSNR = float('inf')
    else:
        PSNR = 10 * log10(255.0 / MSE)
        PSNR = 0.0007816 * PSNR ** 2 - 0.06953 * PSNR + 1.5789
    N = len(f1_)
    r1 = sum(f1_ * f2_) - sum(f1_) * sum(f2_) / N
    r2 = sqrt((sum(f1_ ** 2) - sum(f1_) ** 2 / N) * (sum(f2_ ** 2) - sum(f2_) ** 2 / N))
    PC = r1 / r2
    return (MSE, PSNR, PC)