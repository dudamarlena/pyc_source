# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/numeric/plot.py
# Compiled at: 2006-05-18 14:48:41
"""Plotting numerical replicators"""
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def plot_to_file(filename, *args, **kw):
    """"""
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.plot([1, 2, 3])
    ax.set_title('hi mom')
    ax.grid(True)
    ax.set_xlabel('time')
    ax.set_ylabel('volts')
    canvas.show()


plot_to_file('toto')