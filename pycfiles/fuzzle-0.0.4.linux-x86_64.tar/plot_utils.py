# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/fuzzle/plot_utils.py
# Compiled at: 2016-04-12 16:05:34
import matplotlib.pyplot as plt
from fuzzle.utils import frange

def plot_lvar(lvars, resolution=10):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
    if not isinstance(lvars, list):
        lvars = [
         lvars]
    for i, lvar in enumerate(lvars, 1):
        start, end = lvar.domain
        domain = [ i for i in frange(end, start, step=1.0 / resolution) ]
        mfs = dict()
        for mf in lvar:
            mfs[mf] = [ lvar[mf](x) for x in domain ]

        plt.subplot(1, len(lvars), i)
        for j, (mf, values) in enumerate(mfs.items()):
            ax.plot(domain, values, colors[((j - 1) % len(colors))])
            ax.grid(True)


def plot_mf(mf, domain, resolution=10, color='r'):
    start, end = domain
    points = [ (i, mf(i)) for i in frange(end, start, step=1.0 / resolution) ]
    plt.fill([ i[0] for i in points ], [ i[1] for i in points ], color)
    plt.show()