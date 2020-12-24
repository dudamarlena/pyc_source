# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/streamgraph.py
# Compiled at: 2014-12-19 21:47:38
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt

def baseline_symmetric(streams):
    """Symmetric baseline ('silhouette')"""
    g0 = -0.5 * np.sum(np.asarray(streams), axis=0)
    return g0


def baseline_zero(streams):
    """Zero baseline"""
    return np.zeros(np.asarray(streams).shape[1])


def baseline_weighted_wiggle(streams):
    """Weighted-wiggle minimization
    
    NOTE: streams should already be ordered as desired
    """
    streams = np.asarray(streams)
    f = np.hstack((np.zeros((streams.shape[0], 1)), streams))
    df = np.diff(f)
    cum_sum_df = np.vstack((np.zeros((1, df.shape[1])), np.cumsum(df, axis=0)))[:-1, :]
    dg0 = -1.0 / np.sum(streams, axis=0) * np.sum((0.5 * df + cum_sum_df) * streams, axis=0)
    g0 = np.cumsum(dg0)
    return g0


def argsort_onset(streams):
    """Returns permutation indices (like argsort) for onset ordering."""
    streams = np.asarray(streams)
    nonzero_idxs = [ np.arange(streams.shape[1])[idxs] for idxs in streams > 0 ]
    onset_idxs = [ np.min(nzi) if len(nzi) > 0 else streams.shape[1] for nzi in nonzero_idxs ]
    return np.argsort(onset_idxs)


def argsort_inside_out(streams):
    """Returns permutation indices (like argsort) for inside-out ordering."""
    upper = []
    lower = []
    weight_up = 0
    weight_lo = 0
    for i, stream in enumerate(streams):
        if weight_up < weight_lo:
            upper.append(i)
            weight_up += np.sum(stream)
        else:
            lower.append(i)
            weight_lo += np.sum(stream)

    return upper[::-1] + lower


def streamgraph(ax, streams, x=None, colors=None, baseline=baseline_weighted_wiggle, yoffset=0.0, whitebg=True):
    streams = np.asarray(streams)
    g0 = baseline(streams) + yoffset
    if x == None:
        x = range(streams.shape[1])
    if colors == None:
        colors = map(mpl.cm.bone, np.random.uniform(size=streams.shape[0]))
    layers = []
    g_lo = g0
    for stream in streams:
        g_hi = g_lo + stream
        verts_lo = zip(x, g_lo)
        verts_hi = zip(x[::-1], g_hi[::-1])
        layer = verts_lo + verts_hi
        layers.append(layer)
        g_lo = g_hi

    polys = mpl.collections.PolyCollection(layers, facecolors=colors, linewidths=0, zorder=10)
    ax.add_collection(polys)
    if whitebg == True:
        verts = np.asarray(zip(x, g0) + zip(x[::-1], g_hi[::-1]))
        bglayer = mpl.patches.Polygon(verts, closed=True, color='white', alpha=1, zorder=5)
        ax.add_patch(bglayer)
    return ax


def format_streamgraph(ax):
    """Performs some common formatting operations for streamgraphs"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')