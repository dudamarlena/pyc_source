# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/sandbox/untb/test/test.py
# Compiled at: 2013-04-02 18:46:41
"""
Created on Dec 14, 2010

@author: jonathanfriedman
"""
import numpy as np
from numpy import array, arange
import matplotlib.pyplot as plt, cPickle as pickle, rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
untb = importr('untb')
site = 'Midvagina'
path = '/Users/jonathanfriedman/Documents/Alm/HMP_HGT/dawg/'
ts_file = path + 'data/hmp_' + site + '.pick'
f = open(ts_file, 'r')
abunds = pickle.load(f)
f.close()
(counts, otus, samples) = abunds.to_matrix()
c = counts[:, :-1].sum(axis=1)
print len(c[(c != 0)])
a = untb.count(c[(c != 0)])
preston = untb.preston(a)
cat = list(preston.names)
c = array(preston)
w = 0.8
plt.bar(arange(len(c)) - w / 2, c, width=w)
plt.xticks(arange(len(c)), cat, rotation=45)
plt.show()