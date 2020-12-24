# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bxa/xspec/plot.py
# Compiled at: 2020-01-28 12:31:59
# Size of source mod 2**32: 1059 bytes
from __future__ import absolute_import, unicode_literals, print_function
__doc__ = '\nPlotting of posterior parameter marginal distributions\n\nAuthor: Johannes Buchner (C) 2013-2019\n'
import matplotlib.pyplot as plt, json, corner, numpy, warnings

def marginal_plots(analyzer, minweight=0.0001, **kwargs):
    """
        Create marginal plots
        
        * analyzer: A instance of pymultinest.Analyzer
        * d: if more than 20 dimensions, by default only 1d marginal distributions
           are plotted. set d=2 if you want to force a 2d matrix plot
        
        """
    prefix = analyzer.outputfiles_basename
    parameters = json.load(open(prefix + 'params.json'))
    data = analyzer.get_data()[:, 2:]
    weights = analyzer.get_data()[:, 0]
    mask = weights > minweight
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        (corner.corner)(data[mask, :], weights=weights[mask], labels=parameters, 
         show_titles=True, **kwargs)
    plt.savefig(prefix + 'corner.pdf')
    plt.savefig(prefix + 'corner.png')
    plt.close()