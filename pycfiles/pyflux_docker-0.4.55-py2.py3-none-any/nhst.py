# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/tests/nhst.py
# Compiled at: 2018-02-01 11:59:15
import scipy.stats as ss

def find_p_value(z):
    p_value = 0
    if z >= 0:
        p_value += 1 - ss.norm.cdf(z, loc=0, scale=1)
        p_value += ss.norm.cdf(-z, loc=0, scale=1)
    else:
        p_value += 1 - ss.norm.cdf(-z, loc=0, scale=1)
        p_value += ss.norm.cdf(z, loc=0, scale=1)
    return p_value