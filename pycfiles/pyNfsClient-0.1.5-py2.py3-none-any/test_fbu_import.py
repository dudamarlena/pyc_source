# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/tests/test_fbu_import.py
# Compiled at: 2018-05-17 07:25:00
from pynfold import fold
import numpy as np

def smear(xt):
    xeff = 0.3 + 0.7 / 20.0 * (xt + 10.0)
    x = np.random.rand()
    if x > xeff:
        return None
    else:
        xsmear = np.random.normal(-2.5, 0.2)
        return xt + xsmear


f = fold()
f.set_response(4, -10, 10)
for i in range(1000):
    xt = np.random.normal(0.3, 2.5)
    x = smear(xt)
    if x is not None:
        f.fill(x, xt)
    else:
        f.miss(xt)

f.data = [
 100, 150, 200, 250, 300, 350, 400, 450]