# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ast2000tools/constants.py
# Compiled at: 2019-11-12 17:41:01
"""Module defining common physical and mathematical constants."""
from __future__ import absolute_import
import numpy as np
pi = np.pi
day = 86400
yr = day * 365.24
AU = 149597870700.0
c = 299792458.0
c_km_pr_s = c * 0.001
c_AU_pr_s = c / AU
c_AU_pr_yr = c * yr / AU
m_sun = 1.9891e+30
G = 6.67408e-11
G_sol = 4 * pi ** 2
k_B = 1.381e-23
sigma = 5.67e-08
N_A = 6.02214179e+23
m_p = 1.673e-27
m_H2 = 0.00201588 / N_A