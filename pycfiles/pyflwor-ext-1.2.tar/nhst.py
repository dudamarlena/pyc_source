# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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