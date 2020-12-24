# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/utils/niceFigure.py
# Compiled at: 2017-06-02 17:59:41
from __future__ import division, print_function, absolute_import
from builtins import range
import matplotlib.pyplot as plt
from matplotlib import rcParams

def niceFigure():
    rcParams.update({'figure.autolayout': True})
    rcParams['xtick.direction'] = 'out'
    rcParams['ytick.direction'] = 'out'