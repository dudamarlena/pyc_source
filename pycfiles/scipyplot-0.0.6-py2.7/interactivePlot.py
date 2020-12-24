# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/plot/utils/interactivePlot.py
# Compiled at: 2017-06-02 17:59:41
from __future__ import division, print_function, absolute_import
from builtins import range
import matplotlib.pyplot as plt
from ..save2file import save2file

def interactivePlot(plotFunction, nplots, initial_idx=0):
    """

    :param plotFunction: pointer to the function that render the figures. the function should be in the form
        plotFunction(idx) with 0<idx<nplots
    :param nplots: scalar. number of plots over which to iterate.
    :param initial_idx: index of the plot used to initialize the visualization.
    :return:
    """
    global curr_idx
    curr_idx = initial_idx

    def key_event(e):
        global curr_idx
        if e.key == 'right' or e.key == 'up':
            curr_idx += 1
        elif e.key == 'left' or e.key == 'down':
            curr_idx -= 1
        elif e.key == 'p':
            key = input('Insert name file to save: [default: figure].pdf') or 'figure'
            save2file(fig=fig, nameFile=key, fileFormat='pdf')
        else:
            if e.key == 'q':
                plt.close()
                return
            else:
                return

        curr_idx = curr_idx % nplots
        ax.cla()
        plotFunction(curr_idx)
        fig.canvas.draw()

    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', key_event)
    ax = fig.add_subplot(111)
    plotFunction(curr_idx)
    plt.show()