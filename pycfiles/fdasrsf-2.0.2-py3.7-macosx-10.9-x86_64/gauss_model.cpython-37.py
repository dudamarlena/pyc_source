# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/gauss_model.py
# Compiled at: 2019-10-14 10:32:19
# Size of source mod 2**32: 268 bytes
"""
Gaussian Model of functional data

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
import numpy as np
import fdasrsf.utility_functions as uf
from scipy.integrate import cumtrapz
import fdasrsf.fPCA as fpca
import fdasrsf.geometry as geo
import collections