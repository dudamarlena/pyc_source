# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/plot/plotting.py
# Compiled at: 2019-11-16 18:33:01
# Size of source mod 2**32: 1537 bytes
"""Functions for plotting curves."""
import matplotlib.pyplot as plt
import numpy as np, os, json, argparse, numpy as np, pandas as pd
from pylab import exp
import matplotlib as mpl
import scipy.stats as ss
from matplotlib import mlab
from tabulate import tabulate
import matplotlib.pyplot as plt
from pprint import pprint as pp
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator

def plotBox(data=[], title='', xlabel='', ylabel=''):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(data)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax


def plotBar(x_seq, title='', xlabel='', ylabel=''):
    width = len(x_seq)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(width, x_seq)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax