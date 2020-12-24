# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/scripts/interpolate_new_asf.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1415 bytes
import numpy as np
from scipy.optimize import fmin_l_bfgs_b as optim
asf1 = np.array([0.126842, 4.708971, 1.194814, 1.558157, 1.170413, 3.239403, 4.875207, 108.506081, 0.111516, 48.292408, 1.928171])
asf2 = np.array([0.058851, 3.062918, 4.135106, 0.853742, 1.036792, 0.85252, 2.015803, 4.417941, 0.065307, 9.66971, 0.187818])

def func(asf, stl_range):
    f = np.zeros(stl_range.shape)
    for i in range(1, 6):
        f += asf[i] * np.exp(-asf[(5 + i)] * stl_range ** 2)

    f += asf[0]
    return f


stl_range = np.arange(0, 1, 0.01)
expected1 = func(asf1, stl_range)
expected2 = func(asf2, stl_range)
expected = (expected1 + expected2) / 2.0

def calculate_R2(x0, *args):
    global expected
    global stl_range
    calculated = func(x0, stl_range)
    return np.sum((calculated - expected) ** 2)


bounds = [
 (0, None),
 (None, None),
 (None, None),
 (None, None),
 (None, None),
 (None, None),
 (0.001, None),
 (0.001, None),
 (0.001, None),
 (0.001, None),
 (0.001, None)]
x0 = asf2
lastx, lastR2, info = optim(calculate_R2, x0, approx_grad=True, pgtol=1e-23, factr=2, iprint=(-1), bounds=bounds)
print(lastR2)
print('\t'.join([('%.10g' % fl).replace('.', ',') for fl in lastx]))
print(info)