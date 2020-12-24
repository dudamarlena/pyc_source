# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_matplotlib/util.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 744 bytes
import matplotlib.pyplot as plt

def plot(x, y):
    plt.plot(x, y)


def horizontal_line(xmin, xmax, y=0):
    plt.hlines(y, xmin=xmin, xmax=xmax, linestyles='dashed')


def errorbar(x, y, xerr, yerr):
    plt.errorbar(x=x,
      y=y,
      xerr=xerr,
      yerr=yerr,
      markersize=1,
      marker='o',
      linestyle='None')


def title(title_name):
    if title_name is not None:
        plt.title(title_name)


def label_axes(xlabel, ylabel):
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)


def grid(is_grid):
    if is_grid:
        plt.grid(True)


def show_or_export(output_path=None):
    if output_path is None:
        plt.show()
        return
    plt.savefig(output_path)
    plt.clf()