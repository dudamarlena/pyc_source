# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pySPM\tools\emission_current_plotter.py
# Compiled at: 2019-05-21 08:54:40
# Size of source mod 2**32: 1976 bytes
import psutil, numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from matplotlib.dates import strpdate2num
import pandas as pd, sys
from pySPM.tools.fpanel import Fpanel

def plotLog(filename, watch=False, **kargs):
    fig, ax = plt.subplots(1, 1)
    fig.subplots_adjust(hspace=0)
    plt.show(block=False)
    while 1:
        with open(filename, 'r') as (f):
            names = f.readline().rstrip().split('\t')
        df = pd.read_csv(filename, skiprows=1, delimiter='\t', parse_dates=[0], na_values='<undefined>', names=names)
        ax2 = df.plot('Time', subplots=True, ax=ax, sharex=True)
        dt = df.iloc[(-1, 0)] - df.iloc[(0, 0)]
        for a in ax2:
            if dt.seconds < 900:
                a.xaxis.set_major_locator(mpl.dates.MinuteLocator(interval=1))
            else:
                if dt.seconds < 10800:
                    a.xaxis.set_major_locator(mpl.dates.MinuteLocator(interval=5))
                else:
                    a.xaxis.set_major_locator(mpl.dates.MinuteLocator(interval=15))
            a.xaxis.set_major_formatter(mpl.dates.DateFormatter('%H:%M'))
            a.grid()

        plt.minorticks_off()
        if watch:
            mypause(3)
        else:
            plt.show()
        if not watch:
            break


def mypause(interval):
    backend = plt.rcParams['backend']
    if backend in mpl.rcsetup.interactive_bk:
        figManager = mpl._pylab_helpers.Gcf.get_active()
        if figManager is not None:
            canvas = figManager.canvas
            if canvas.figure.stale:
                canvas.draw()
            canvas.start_event_loop(interval)
            return


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        print('Plot file "{}"'.format(filename))
        plotLog(filename, watch=False)
    else:
        F = Fpanel()
        logfile = F.getLogFile()
        plotLog(logfile, watch=True)


if __name__ == '__main__':
    main()