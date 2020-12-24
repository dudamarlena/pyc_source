# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3plex/algorithms/statistics/topology.py
# Compiled at: 2020-01-19 02:29:57
# Size of source mod 2**32: 4216 bytes
import networkx as nx, numpy as np, random, argparse
from itertools import groupby, chain
from collections import defaultdict
import pandas as pd
from .powerlaw import *
import matplotlib.pyplot as plt

def basic_pl_stats(degree_sequence):
    """
    :param degree sequence of individual nodes
    """
    results = Fit(degree_sequence, discrete=True)
    return (
     results.alpha, results.sigma)


def plot_power_law(degree_sequence, title, xlabel, plabel, ylabel='Number of nodes', formula_x=70, formula_y=0.05, show=True, use_normalization=False):
    plt.figure(2)
    ax1 = plt.subplot(211)
    results = Fit(degree_sequence, discrete=True)
    a = results.power_law.pdf(degree_sequence)
    fig1 = results.plot_pdf(linewidth=1, color='black', label='Raw data', linear_bins=True, linestyle='', marker='o', markersize=1)
    results.power_law.plot_pdf(linewidth=1.5, ax=fig1, color='green', linestyle='--', label='Power law')
    results.lognormal.plot_pdf(linewidth=0.5, ax=fig1, color='blue', linestyle='-', label='Log-normal')
    results.truncated_power_law.plot_pdf(linewidth=0.5, ax=fig1, color='orange', linestyle='-', label='Truncated power law')
    results.exponential.plot_pdf(linewidth=0.5, ax=fig1, color='red', linestyle='-', label='Exponential')
    print('ALPHA: ', results.alpha)
    print('SIGMA: ', results.sigma)
    print('xmin: ', results.xmin)
    print('percent of non PL coverage: {}'.format(len([x for x in degree_sequence if x < results.xmin]) * 100 / len(degree_sequence)))
    print('Percentage of PL coverage: {}'.format(len([x for x in degree_sequence if x > results.xmin]) * 100 / len(degree_sequence)))
    start = a[int(results.xmin)]
    k = results.xmin
    norm = int(round(start * len(degree_sequence) * 100 / pow(k, -results.alpha), 0))
    print('Fixed xmax: ', results.fixed_xmax)
    print(results.distribution_compare('truncated_power_law', 'lognormal'))
    print(results.distribution_compare('lognormal', 'power_law'))
    print(results.distribution_compare('truncated_power_law', 'power_law'))
    print('............')
    print(results.distribution_compare('exponential', 'lognormal'))
    print(results.distribution_compare('exponential', 'truncated_power_law'))
    print(results.distribution_compare('exponential', 'power_law'))
    import matplotlib.ticker as mtick
    from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
    plt.legend(numpoints=1, loc='lower left', bbox_to_anchor=(0.05, 0))
    vals = ax1.get_yticks()
    vals = [float(round(x * len(degree_sequence), 1)) for x in vals]
    ax1.set_yticklabels(vals[0:6])
    plt.ylabel(ylabel)
    plt.axvline(x=(results.xmin), color='black', linestyle='--')
    plt.ylim(0, 0.1)
    if not use_normalization:
        norm = 'C'
    ax1.text(formula_x, formula_y, ('$f(k) = ' + norm + ' \\cdot k^{-' + str(round(results.alpha, 3)) + '}$'), fontsize=13)
    ax1 = plt.subplot(212)
    plt.axvline(x=(results.xmin), color='black', linestyle='--')
    plt.xlabel(xlabel)
    ax1.text((results.xmin + 0.5), 0.001, '$X_{min}$', fontsize=13)
    fig1 = results.plot_ccdf(linewidth=2, color='black', label='Raw data', linestyle='', marker='o', markersize=1)
    results.power_law.plot_ccdf(ax=fig1, color='green', linestyle='--', label='Power law', linewidth=1.5)
    results.lognormal.plot_ccdf(ax=fig1, color='blue', linestyle='-', label='Log-normal')
    results.truncated_power_law.plot_ccdf(ax=fig1, color='orange', linestyle='-', label='Truncated power law')
    results.exponential.plot_ccdf(ax=fig1, color='red', linestyle='-', label='Exponential', linewidth=0.5)
    import matplotlib.ticker as mtick
    plt.ylabel('$P(k) = Pr(K \\geq k)$')
    if show:
        plt.show()


if __name__ == '__main__':
    G = nx.powerlaw_cluster_graph(1000, 3, 0.5, 1573)
    val_vect = sorted((dict(nx.degree(G)).values()), reverse=True)
    plot_power_law(val_vect, '', 'Node degree', 'individual node')