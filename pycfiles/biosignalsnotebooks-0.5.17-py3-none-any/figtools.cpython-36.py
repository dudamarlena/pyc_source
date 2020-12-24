# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\figtools.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 4259 bytes
from pylab import rc, close, figure, axes, subplot, plot, axis, show, grid, savefig, text
from numpy import arange
from matplotlib import pyplot as plot
import pandas, tkinter.filedialog as tkFileDialog

def load_data_dialog(path):
    filename = tkFileDialog.askopenfile()
    return pandas.read_csv(filename, sep=' ', header=None)


def pylabconfig():
    rc('lines', linewidth=2, color='k')
    rc(*('font', ), family='serif', serif=['Palatino'])
    rc('font', style='italic', size=10)
    rc('text', color='grey')
    rc('text', usetex=False)
    rc('figure', figsize=(8, 5), dpi=80)
    rc('axes', grid=True, edgecolor='grey', labelsize=10)
    rc('grid', color='grey')
    rc('xtick', color='grey', labelsize=10)
    rc('ytick', color='grey', labelsize=10)
    close('all')


def plotwithhist(t, s, bins=50):
    from matplotlib.ticker import NullFormatter
    nullfmt = NullFormatter()
    figure()
    ax2 = axes([0.625, 0.1, 0.2, 0.8])
    ax1 = axes([0.125, 0.1, 0.5, 0.8])
    ax1.plot(t, s)
    ax1.set_xticks(ax1.get_xticks()[:-1])
    ax2.hist(s, bins, normed=True, facecolor='white', orientation='horizontal',
      lw=2)
    ax2.axis([0, 1, ax1.axis()[2], ax1.axis()[3]])
    ax2.yaxis.set_major_formatter(nullfmt)
    ax2.set_xticks([0, 0.5, 1])
    return (
     ax1, ax2)


def plotwithstats(t, s):
    from matplotlib.ticker import NullFormatter
    nullfmt = NullFormatter()
    figure()
    ax2 = axes([0.625, 0.1, 0.2, 0.8])
    ax1 = axes([0.125, 0.1, 0.5, 0.8])
    ax1.plot(t, s)
    ax1.set_xticks(ax1.get_xticks()[:-1])
    meanv = s.mean()
    mi = s.min()
    mx = s.max()
    sd = s.std()
    ax2.bar((-0.5), (mx - mi), 1, mi, lw=2, color='#f0f0f0')
    ax2.bar((-0.5), (sd * 2), 1, (meanv - sd), lw=2, color='#c0c0c0')
    ax2.bar((-0.5), 0.2, 1, (meanv - 0.1), lw=2, color='#b0b0b0')
    ax2.axis([-1, 1, ax1.axis()[2], ax1.axis()[3]])
    ax2.yaxis.set_major_formatter(nullfmt)
    ax2.set_xticks([])
    return (
     ax1, ax2)


def multilineplot(signal, linesize=250, events=None, title='', dir='', step=1):
    from pylab import rc
    rc('axes', labelcolor='#a1a1a1', edgecolor='#a1a1a1', labelsize='xx-small')
    rc('xtick', color='#a1a1a1', labelsize='xx-small')
    grid('off')
    nplots = len(signal) // linesize + 1
    ma_x = max(signal)
    mi_x = min(signal)
    f = figure(figsize=(20, 1.5 * nplots), dpi=80)
    for i in range(nplots):
        ax = subplot(nplots, 1, i + 1)
        start = i * len(signal) / nplots
        end = (i + 1) * len(signal) / nplots
        plot(arange(start, end, step), signal[start:end:step], 'k')
        axis((start, end, mi_x, ma_x))
        ax.set_yticks([])
        ax.set_xticks(ax.get_xticks()[1:-1])
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        if events != None:
            e = events[((events >= start) & (events < end))]
            if len(e) > 0:
                plot.vlines(e, mi_x, (ma_x - (ma_x - mi_x) / 4.0 * 3.0), lw=2)
        if title != None:
            text(start, ma_x, title)
        grid('off')

    f.tight_layout()
    savefig(dir + title + '.pdf')
    close()