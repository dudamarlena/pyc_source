# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/plotting/plotting.py
# Compiled at: 2013-04-05 15:45:02
"""
Created on Dec 6, 2012

@author: jonathanfriedman
"""
import matplotlib.pyplot as plt, numpy as np
from pysurvey.core.core_methods import _get_axis

def plot_cols(frame, **kwargs):
    """
    Line plot of all columns of frame.
    """
    if 'cols' in kwargs:
        cols = kwargs.pop('cols')
        data = frame.filter(items=cols)
    else:
        data = frame
    (n, m) = np.shape(data)
    x = kwargs.pop('x', np.arange(1, n + 1))
    logx = kwargs.pop('logx', False)
    logy = kwargs.pop('logy', False)
    fs = kwargs.pop('fs', 16)
    legend = kwargs.pop('legend', True)
    legend_kwargs = kwargs.pop('legend_kwargs', {'loc': 'best'})
    new_fig = kwargs.pop('new_fig', True)
    xlabel = kwargs.pop('xlabel', 'X axis')
    ylabel = kwargs.pop('ylabel', 'Y axis')
    xticks = kwargs.pop('xticks', np.arange(1, n + 1))
    labelx = kwargs.pop('labelx', False)
    xlabel_rot = kwargs.pop('xlabel_rot', 90)
    grid = kwargs.pop('grid', True)
    if new_fig:
        plt.figure()
    if logx:
        x = np.log10(x)
    if logy:
        data = np.log10(data)
    for (c, y) in data.iteritems():
        plt.plot(x, y.values, label=c, **kwargs)

    plt.xlim(x[0], x[(-1)])
    if logx:
        xlabel = 'log10(' + xlabel + ')'
    if logy:
        ylabel = 'log10(' + ylabel + ')'
    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    if logx:
        xticks = np.log10(xticks)
    if labelx:
        plt.xticks(xticks, data.index, rotation=xlabel_rot)
    else:
        plt.xticks([0], '')
    if legend:
        plt.legend(**legend_kwargs)
    plt.grid(grid)


def stacked_plot(frame, logx=False, logy=False, fs=16, legend=False, legend_kwargs={'loc': 'best'}, xlabel=None, ylabel=None, labelx=False, xlabel_rot=90, grid=False, interactive=True, annotator_kwargs={'write': True, 'draw': False, 'title': True}, **kwargs):
    """
    stacked (area) plot of all columns of frame.
    """
    from stacked_plot import stacked_plot
    if 'cols' in kwargs:
        cols = kwargs.pop('cols')
        data = frame.filter(items=cols)
    else:
        data = frame
    n = data.shape[0]
    x = kwargs.pop('x', np.arange(1, n + 1))
    xticks = kwargs.pop('xticks', np.arange(1, n + 1))
    xlabels = kwargs.pop('xlabels', list(frame.index))
    clabels = kwargs.pop('clabels', list(frame.columns))
    xannotes = kwargs.pop('xannotes', xlabels)
    col_annotes = kwargs.pop('col_annotes', clabels)
    if logx:
        x = np.log10(x)
    if logy:
        data = np.log10(data)
    if legend:
        labels = clabels
    else:
        labels = None
    stacked_plot(x, data.T, labels=labels, **kwargs)
    plt.xlim(x[0], x[(-1)])
    if xlabel is not None:
        if logx:
            xlabel = 'log10(' + xlabel + ')'
        plt.xlabel(xlabel, fontsize=fs)
    if ylabel is not None:
        if logy:
            ylabel = 'log10(' + ylabel + ')'
        plt.ylabel(ylabel, fontsize=fs)
    if logx:
        xticks = np.log10(xticks)
    if labelx:
        plt.xticks(xticks, xlabels, rotation=xlabel_rot)
    else:
        plt.xticks([0], '')
    if legend:
        plt.legend(**legend_kwargs)
    plt.grid(grid)
    if interactive:
        from interactive.annotators import StackedAnnotator
        xannotes = np.asarray(xannotes, dtype=str)
        col_annotes = np.asarray(col_annotes, dtype=str)
        StackedAnnotator(x, data.T, xannotes=xannotes, yannotes=col_annotes, **annotator_kwargs)
    return


def bar_plot(frame, style='stacked', **kwargs):
    """
    Make a bar plot of frame
    """
    from Bars import multibar
    xlabel = kwargs.pop('xlabel', None)
    ylabel = kwargs.pop('ylabel', None)
    fs = kwargs.pop('fs', 16)
    label_rows = kwargs.pop('label_rows', True)
    rlabels = kwargs.pop('rlabels', list(frame.index))
    rotation = kwargs.pop('rotation', 0)
    legend = kwargs.pop('legend', False)
    clabels = kwargs.pop('clabels', list(frame.columns))
    interactive = kwargs.pop('interactive', True)
    row_annotes = kwargs.pop('row_annotes', rlabels)
    col_annotes = kwargs.pop('col_annotes', clabels)
    write = kwargs.pop('write', True)
    draw = kwargs.pop('draw', False)
    title = kwargs.pop('title', True)
    (n, m) = np.shape(frame)
    x = np.arange(n)
    if legend:
        labels = clabels
    else:
        labels = False
    y = frame.values
    rects = multibar(x, y, style, labels=labels, **kwargs)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=fs)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=fs)
    if label_rows is True:
        labels = rlabels
    elif label_rows is False:
        labels = []
    plt.xticks(x, labels, rotation=rotation)
    if interactive:
        from interactive.annotators import MultibarAnnotator
        row_annotes = np.asarray(row_annotes, dtype=str)
        col_annotes = np.asarray(col_annotes, dtype=str)
        MultibarAnnotator(x, y, xannotes=row_annotes, yannotes=col_annotes, style=style, write=write, draw=draw, title=title)
    return


def plot_heatmap(frame, **kwargs):
    """
    Plot heatmap of frame, sorted by heirarchical clustering with given distance metric
    If plotting a distance matrix, set the dist_mat option to True in order to avoid 
    sorting by the distances of distances, but rather by the given values in the distance matrix.
    """
    from heatmaps import clustered_heatmap
    matrix = frame.values
    rlabels = frame.index
    clabels = frame.columns
    kwargs.setdefault('plot_rlabels', False)
    kwargs.setdefault('plot_clabels', False)
    kwargs.setdefault('rlabels', rlabels)
    kwargs.setdefault('clabels', clabels)
    cstrip = kwargs.pop('cstrip', None)
    cmeta = kwargs.pop('cmeta', None)
    if isinstance(cstrip, str):
        cstrip = cmeta[cstrip]
    if hasattr(cstrip, 'reindex'):
        cstrip = cstrip.reindex(index=frame.columns)
    kwargs['cstrip'] = cstrip
    rstrip = kwargs.pop('rstrip', None)
    rmeta = kwargs.pop('rmeta', None)
    if isinstance(rstrip, str):
        rstrip = rmeta[rstrip]
    if hasattr(rstrip, 'reindex'):
        rstrip = rstrip.reindex(index=frame.index)
    kwargs['rstrip'] = rstrip
    return clustered_heatmap(matrix, **kwargs)


def plot_dist_heatmap(frame, metric='euclidean', axis=0, **kwargs):
    """
    Calculate distance matrix and make a heatplot of the resulting distance matrix.
    Return the distance matrix and the output of plot_heatmap.
    """
    from pysurvey.analysis.analysis_methods import dist_mat
    D = dist_mat(frame, metric=metric, axis=axis)
    out = plot_heatmap(D, dist_mat=True, **kwargs)
    return (D, out)


def bar_plot_lins(frame, lins, style='stacked', level='all', **kwargs):
    """
    Make an interactive bar plot with linegaes as annotations.
    """
    if level == 'all':
        col_annotes = [ id + ':' + lins[id].lin_str for id in frame.get_labels('c') ]
    else:
        col_annotes = [ id + ':' + lins[id].lin[level] for id in frame.get_labels('c') ]
    bar_plot(frame, style, col_annotes=col_annotes, **kwargs)


def plot_range_abunance(frame, **kwargs):
    """
    Make a plot of OTU range vs average fraction.
    """
    from pysurvey import sample_diversity
    range_log = kwargs.get('range_log', False)
    frac_log = kwargs.get('frac_log', True)
    fs = kwargs.get('fs', 16)
    plt.figure()
    otu_avg = frame.mean()
    method = kwargs.get('method', 'ML')
    index = kwargs.get('index', 'Hill_0')
    otu_range = sample_diversity(frame.T, indices=[
     index], methods=[method])
    x = otu_avg.values
    y = otu_range.values[:, 0]
    if frac_log:
        x = np.log10(x)
    if range_log:
        y = np.log10(y)
    plt.plot(x, y, 'bo')
    if range_log:
        ylab = 'log10(Effective # samples)'
    else:
        ylab = 'Effective # samples'
    if frac_log:
        xlab = 'log10(<fraction>)'
    else:
        xlab = '<fraction>'
    plt.xlabel(xlab, fontsize=fs)
    plt.ylabel(ylab, fontsize=fs)
    plt.grid()
    show_cor = kwargs.get('show_cor', True)
    if show_cor:
        import scipy.stats as stats
        (r, p) = stats.spearmanr(x, y)
        s = 'spearman r = %.1f \np_val = %1.0e' % (r, p)
        str_x = 0.05
        str_y = 0.95
        ax = plt.gca()
        plt.text(str_x, str_y, s, bbox=dict(boxstyle='round', fc='0.8'), transform=ax.transAxes, ha='left', va='top')


def plot_incidence_abunance(frame, **kwargs):
    """
    Make a plot of OTU range vs average fraction.
    """
    range_log = kwargs.get('range_log', False)
    frac_log = kwargs.get('frac_log', True)
    fs = kwargs.get('fs', 16)
    (n, k) = np.shape(frame)
    n *= 1.0
    plt.figure()
    otu_avg = frame.apply(lambda x: np.mean(x[(x > 0)]))
    otu_range = frame.apply(lambda x: len(x[(x > 0)]) / n)
    x = otu_range.values
    y = otu_avg.values
    if frac_log:
        y = np.log10(y)
    if range_log:
        x = np.log10(x)
    plt.plot(x, y, 'bo')
    if range_log:
        xlab = 'log10(% samples present)'
    else:
        xlab = '% samples present'
    if frac_log:
        ylab = 'log10(<fraction>)'
    else:
        ylab = '<fraction>'
    plt.xlabel(xlab, fontsize=fs)
    plt.ylabel(ylab, fontsize=fs)
    plt.grid()
    show_cor = kwargs.get('show_cor', True)
    if show_cor:
        import scipy.stats as stats
        (r, p) = stats.spearmanr(x, y)
        s = 'spearman r = %.1f \np_val = %1.0e' % (r, p)
        str_x = 0.05
        str_y = 0.95
        ax = plt.gca()
        plt.text(str_x, str_y, s, bbox=dict(boxstyle='round', fc='0.8'), transform=ax.transAxes, ha='left', va='top')


def GMM_plot(frame, n_components, metric=None, **kwargs):
    from pysurvey.analysis.GMM import plot_GMM
    from pysurvey.analysis.analysis_methods import PCoA
    from pandas import Series
    fs = kwargs.pop('fs', 16)
    grid = kwargs.pop('grid', True)
    kwargs.setdefault('sample_labels', list(frame.index))
    (points, eigs) = PCoA(frame, metric)
    var = eigs / eigs.sum() * 100
    X = points.values[:, :2]
    (gmm, splot) = plot_GMM(X, n_components, **kwargs)
    xl = 'PC1 (%.1f' % var[0] + '%)'
    yl = 'PC2 (%.1f' % var[1] + '%)'
    splot.set_xlabel(xl, fontsize=fs)
    splot.set_ylabel(yl, fontsize=fs)
    mem = gmm.predict(X)
    membership_hard = Series(mem, index=list(frame.index))
    membership_hard.sort()
    plt.grid(grid)
    return (membership_hard, gmm, points, eigs)


def plot_rank_abundance(frame, **kwargs):
    """
    Make a rank abundance plot for samples.
    """
    from pysurvey.analysis.analysis_methods import rank_abundance
    kwargs.setdefault('xlabel', 'Rank')
    kwargs.setdefault('ylabel', 'Abundance')
    kwargs.setdefault('logx', True)
    kwargs.setdefault('logy', True)
    kwargs.setdefault('linestyle', 'dashed')
    kwargs.setdefault('linewidth', 1)
    kwargs.setdefault('marker', 'x')
    kwargs.setdefault('ms', 10)
    kwargs.setdefault('legend', False)
    ranked = rank_abundance(frame)
    ranked.plot_cols(**kwargs)
    return ranked


if __name__ == '__main__':
    from pandas import DataFrame
    rows = [
     'r2', 'r0', 'r1']
    cols = ['c0', 'c1']
    metac = DataFrame([['sample1', 'big'], ['sample0', 'small']], index=['c1', 'c0'], columns=['name', 'size'])
    metar = DataFrame([['otu0', 5], ['otu2', 10], ['otu1', 10]], index=['r0', 'r2', 'r1'], columns=['name', 'IQ'])
    mat = np.array([[2.0, 1], [1, 3], [10, 15]])
    df = DataFrame(mat, index=rows, columns=cols)