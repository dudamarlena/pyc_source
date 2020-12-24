# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/tqdm/tqdm/_tqdm_gui.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 13201 bytes
"""
GUI progressbar decorator for iterators.
Includes a default (x)range iterator printing to stderr.

Usage:
  >>> from tqdm import tgrange[, tqdm_gui]
  >>> for i in tgrange(10): #same as: for i in tqdm_gui(xrange(10))
  ...     ...
"""
from __future__ import division, absolute_import
from time import time
from ._utils import _range
from ._tqdm import tqdm, TqdmExperimentalWarning
from warnings import warn
__author__ = {'github.com/': ['casperdcl', 'lrq3000']}
__all__ = ['tqdm_gui', 'tgrange']

class tqdm_gui(tqdm):
    __doc__ = '\n    Experimental GUI version of tqdm!\n    '

    def __init__(self, *args, **kwargs):
        import matplotlib as mpl, matplotlib.pyplot as plt
        from collections import deque
        kwargs['gui'] = True
        (super(tqdm_gui, self).__init__)(*args, **kwargs)
        if self.disable or not kwargs['gui']:
            return
        else:
            warn('GUI is experimental/alpha', TqdmExperimentalWarning)
            self.mpl = mpl
            self.plt = plt
            self.sp = None
            self.toolbar = self.mpl.rcParams['toolbar']
            self.mpl.rcParams['toolbar'] = 'None'
            self.mininterval = max(self.mininterval, 0.5)
            self.fig, ax = plt.subplots(figsize=(9, 2.2))
            if self.total:
                self.xdata = []
                self.ydata = []
                self.zdata = []
            else:
                self.xdata = deque([])
                self.ydata = deque([])
                self.zdata = deque([])
            self.line1, = ax.plot((self.xdata), (self.ydata), color='b')
            self.line2, = ax.plot((self.xdata), (self.zdata), color='k')
            ax.set_ylim(0, 0.001)
            if self.total:
                ax.set_xlim(0, 100)
                ax.set_xlabel('percent')
                self.fig.legend((self.line1, self.line2), ('cur', 'est'), loc='center right')
                self.hspan = plt.axhspan(0, 0.001, xmin=0,
                  xmax=0,
                  color='g')
            else:
                ax.set_xlim(0, 60)
                ax.invert_xaxis()
                ax.set_xlabel('seconds')
                ax.legend(('cur', 'est'), loc='lower left')
        ax.grid()
        ax.set_ylabel((self.unit if self.unit else 'it') + '/s')
        if self.unit_scale:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax.yaxis.get_offset_text().set_x(-0.15)
        self.wasion = plt.isinteractive()
        plt.ion()
        self.ax = ax

    def __iter__(self):
        iterable = self.iterable
        if self.disable:
            for obj in iterable:
                yield obj

            return
        mininterval = self.mininterval
        maxinterval = self.maxinterval
        miniters = self.miniters
        dynamic_miniters = self.dynamic_miniters
        unit = self.unit
        unit_scale = self.unit_scale
        ascii = self.ascii
        start_t = self.start_t
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        n = self.n
        smoothing = self.smoothing
        avg_time = self.avg_time
        bar_format = self.bar_format
        plt = self.plt
        ax = self.ax
        xdata = self.xdata
        ydata = self.ydata
        zdata = self.zdata
        line1 = self.line1
        line2 = self.line2
        for obj in iterable:
            yield obj
            n += 1
            delta_it = n - last_print_n
            if delta_it >= miniters:
                cur_t = time()
                delta_t = cur_t - last_print_t
                if delta_t >= mininterval:
                    elapsed = cur_t - start_t
                    if smoothing and delta_t and delta_it:
                        rate = delta_t / delta_it
                        avg_time = self.ema(rate, avg_time, smoothing)
                    total = self.total
                    y = delta_it / delta_t
                    z = n / elapsed
                    xdata.append(n * 100.0 / total if total else cur_t)
                    ydata.append(y)
                    zdata.append(z)
                    if not total:
                        if elapsed > 66:
                            xdata.popleft()
                            ydata.popleft()
                            zdata.popleft()
                    ymin, ymax = ax.get_ylim()
                    if y > ymax or z > ymax:
                        ymax = 1.1 * y
                        ax.set_ylim(ymin, ymax)
                        ax.figure.canvas.draw()
                    if total:
                        line1.set_data(xdata, ydata)
                        line2.set_data(xdata, zdata)
                        try:
                            poly_lims = self.hspan.get_xy()
                        except AttributeError:
                            self.hspan = plt.axhspan(0, 0.001, xmin=0, xmax=0,
                              color='g')
                            poly_lims = self.hspan.get_xy()

                        poly_lims[(0, 1)] = ymin
                        poly_lims[(1, 1)] = ymax
                        poly_lims[2] = [n / total, ymax]
                        poly_lims[3] = [poly_lims[(2, 0)], ymin]
                        if len(poly_lims) > 4:
                            poly_lims[(4, 1)] = ymin
                        self.hspan.set_xy(poly_lims)
                    else:
                        t_ago = [cur_t - i for i in xdata]
                        line1.set_data(t_ago, ydata)
                        line2.set_data(t_ago, zdata)
                    ax.set_title((self.format_meter(n, total, elapsed, 0, self.desc, ascii, unit, unit_scale, 1 / avg_time if avg_time else None, bar_format)),
                      fontname='DejaVu Sans Mono',
                      fontsize=11)
                    plt.pause(1e-09)
                    if dynamic_miniters:
                        if maxinterval:
                            if delta_t > maxinterval:
                                miniters = delta_it * maxinterval / delta_t
                        elif mininterval:
                            if delta_t:
                                rate = delta_it
                                if mininterval:
                                    if delta_t:
                                        rate *= mininterval / delta_t
                                miniters = self.ema(rate, miniters, smoothing)
                        else:
                            miniters = self.ema(delta_it, miniters, smoothing)
                    last_print_n = n
                    last_print_t = cur_t

        self.last_print_n = last_print_n
        self.n = n
        self.close()

    def update(self, n=1):
        if self.disable:
            return
        else:
            if n < 0:
                n = 1
            self.n += n
            delta_it = self.n - self.last_print_n
            if delta_it >= self.miniters:
                cur_t = time()
                delta_t = cur_t - self.last_print_t
                if delta_t >= self.mininterval:
                    elapsed = cur_t - self.start_t
                    if self.smoothing:
                        if delta_t:
                            if delta_it:
                                rate = delta_t / delta_it
                                self.avg_time = self.ema(rate, self.avg_time, self.smoothing)
                    total = self.total
                    ax = self.ax
                    y = delta_it / delta_t
                    z = self.n / elapsed
                    self.xdata.append(self.n * 100.0 / total if total else cur_t)
                    self.ydata.append(y)
                    self.zdata.append(z)
                    if not total and elapsed > 66:
                        self.xdata.popleft()
                        self.ydata.popleft()
                        self.zdata.popleft()
                    ymin, ymax = ax.get_ylim()
                    if y > ymax or z > ymax:
                        ymax = 1.1 * y
                        ax.set_ylim(ymin, ymax)
                        ax.figure.canvas.draw()
                    if total:
                        self.line1.set_data(self.xdata, self.ydata)
                        self.line2.set_data(self.xdata, self.zdata)
                        try:
                            poly_lims = self.hspan.get_xy()
                        except AttributeError:
                            self.hspan = self.plt.axhspan(0, 0.001, xmin=0, xmax=0,
                              color='g')
                            poly_lims = self.hspan.get_xy()

                        poly_lims[(0, 1)] = ymin
                        poly_lims[(1, 1)] = ymax
                        poly_lims[2] = [self.n / total, ymax]
                        poly_lims[3] = [poly_lims[(2, 0)], ymin]
                        if len(poly_lims) > 4:
                            poly_lims[(4, 1)] = ymin
                        self.hspan.set_xy(poly_lims)
                    else:
                        t_ago = [cur_t - i for i in self.xdata]
                        self.line1.set_data(t_ago, self.ydata)
                        self.line2.set_data(t_ago, self.zdata)
                    ax.set_title((self.format_meter(self.n, total, elapsed, 0, self.desc, self.ascii, self.unit, self.unit_scale, 1 / self.avg_time if self.avg_time else None, self.bar_format)),
                      fontname='DejaVu Sans Mono',
                      fontsize=11)
                    self.plt.pause(1e-09)
                    if self.dynamic_miniters:
                        if self.maxinterval:
                            if delta_t > self.maxinterval:
                                self.miniters = self.miniters * self.maxinterval / delta_t
                        elif self.mininterval:
                            if delta_t:
                                self.miniters = self.smoothing * delta_it * self.mininterval / delta_t + (1 - self.smoothing) * self.miniters
                        else:
                            self.miniters = self.smoothing * delta_it + (1 - self.smoothing) * self.miniters
                    self.last_print_n = self.n
                    self.last_print_t = cur_t

    def close(self):
        if self.disable:
            return
        else:
            self.disable = True
            self._instances.remove(self)
            self.mpl.rcParams['toolbar'] = self.toolbar
            if not self.wasion:
                self.plt.ioff()
            if not self.leave:
                self.plt.close(self.fig)


def tgrange(*args, **kwargs):
    """
    A shortcut for tqdm_gui(xrange(*args), **kwargs).
    On Python3+ range is used instead of xrange.
    """
    return tqdm_gui(_range(*args), **kwargs)