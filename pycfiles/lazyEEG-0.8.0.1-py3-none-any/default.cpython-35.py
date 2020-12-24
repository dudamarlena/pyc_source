# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Coding\py\IPython Notebooks\experiment\chunking\LazyEEG\default.py
# Compiled at: 2017-04-14 12:45:19
# Size of source mod 2**32: 1633 bytes
import numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from scipy import stats
import statsmodels, statsmodels.api as sm
from statsmodels.formula.api import ols
import permute
from permute.core import two_sample
import random, math, collections
from collections import defaultdict
from collections import OrderedDict
import itertools, re, time, warnings
ids = pd.IndexSlice
td = pd.Timedelta
warnings.filterwarnings('ignore')
tableau20 = [
 (31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
tableau10 = [
 (31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),
 (148, 103, 189), (140, 86, 75),
 (127, 127, 127), (23, 190, 207), (188, 189, 34), (227, 119, 194)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255.0, g / 255.0, b / 255.0)

for i in range(len(tableau10)):
    r, g, b = tableau10[i]
    tableau10[i] = (r / 255.0, g / 255.0, b / 255.0)