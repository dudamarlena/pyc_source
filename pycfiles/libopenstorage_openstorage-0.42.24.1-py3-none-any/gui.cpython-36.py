# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/tqdm/tqdm/gui.py
# Compiled at: 2020-01-10 16:25:33
# Size of source mod 2**32: 11601 bytes
"""
GUI progressbar decorator for iterators.
Includes a default (x)range iterator printing to stderr.

Usage:
  >>> from tqdm.gui import trange[, tqdm]
  >>> for i in trange(10): #same as: for i in tqdm(xrange(10))
  ...     ...
"""
from __future__ import division, absolute_import
from .utils import _range
from .std import tqdm as std_tqdm
from .std import TqdmExperimentalWarning
from warnings import warn
__author__ = {'github.com/': ['casperdcl', 'lrq3000']}
__all__ = ['tqdm_gui', 'tgrange', 'tqdm', 'trange']

class tqdm_gui(std_tqdm):
    __doc__ = '\n    Experimental GUI version of tqdm!\n    '

    def __init__(self, *args, **kwargs):
        import matplotlib as mpl, matplotlib.pyplot as plt
        from collections import deque
        kwargs['gui'] = True
        (super(tqdm_gui, self).__init__)(*args, **kwargs)
        if self.disable or not kwargs['gui']:
            return
        else:
            warn('GUI is experimental/alpha', TqdmExperimentalWarning, stacklevel=2)
            self.mpl = mpl
            self.plt = plt
            self.sp = None
            self.toolbar = self.mpl.rcParams['toolbar']
            self.mpl.rcParams['toolbar'] = 'None'
            self.mininterval = max(self.mininterval, 0.5)
            self.fig, ax = plt.subplots(figsize=(9, 2.2))
            total = len(self)
            if total is not None:
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
            if total is not None:
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
        last_print_t = self.last_print_t
        last_print_n = self.last_print_n
        n = self.n
        smoothing = self.smoothing
        avg_time = self.avg_time
        time = self._time
        for obj in iterable:
            yield obj
            n += 1
            if n - last_print_n >= self.miniters:
                miniters = self.miniters
                delta_t = time() - last_print_t
                if delta_t >= mininterval:
                    cur_t = time()
                    delta_it = n - last_print_n
                    if smoothing:
                        if delta_t:
                            if delta_it:
                                rate = delta_t / delta_it
                                avg_time = self.ema(rate, avg_time, smoothing)
                                self.avg_time = avg_time
                    self.n = n
                    self.display()
                    if dynamic_miniters:
                        if maxinterval and delta_t >= maxinterval:
                            if mininterval:
                                miniters = delta_it * mininterval / delta_t
                            else:
                                miniters = delta_it * maxinterval / delta_t
                        else:
                            if smoothing:
                                rate = delta_it
                                if mininterval:
                                    if delta_t:
                                        rate *= mininterval / delta_t
                                miniters = self.ema(rate, miniters, smoothing)
                            else:
                                miniters = max(miniters, delta_it)
                    self.n = self.last_print_n = last_print_n = n
                    self.last_print_t = last_print_t = cur_t
                    self.miniters = miniters

        self.last_print_n = last_print_n
        self.n = n
        self.miniters = miniters
        self.close()

    def update(self, n=1):
        if self.disable:
            return
        else:
            if n < 0:
                self.last_print_n += n
            self.n += n
            if self.n - self.last_print_n >= self.miniters:
                delta_t = self._time() - self.last_print_t
                if delta_t >= self.mininterval:
                    cur_t = self._time()
                    delta_it = self.n - self.last_print_n
                    if self.smoothing:
                        if delta_t:
                            if delta_it:
                                rate = delta_t / delta_it
                                self.avg_time = self.ema(rate, self.avg_time, self.smoothing)
                    self.display()
                    if self.dynamic_miniters:
                        if self.maxinterval:
                            if delta_t >= self.maxinterval:
                                if self.mininterval:
                                    self.miniters = delta_it * self.mininterval / delta_t
                                else:
                                    self.miniters = delta_it * self.maxinterval / delta_t
                        else:
                            if self.smoothing:
                                self.miniters = self.smoothing * delta_it * (self.mininterval / delta_t if self.mininterval and delta_t else 1) + (1 - self.smoothing) * self.miniters
                            else:
                                self.miniters = max(self.miniters, delta_it)
                    self.last_print_n = self.n
                    self.last_print_t = cur_t

    def close(self):
        if self.disable:
            return
        else:
            self.disable = True
            with self.get_lock():
                self._instances.remove(self)
            self.mpl.rcParams['toolbar'] = self.toolbar
            if not self.wasion:
                self.plt.ioff()
            if not self.leave:
                self.plt.close(self.fig)

    def display(self):
        n = self.n
        cur_t = self._time()
        elapsed = cur_t - self.start_t
        delta_it = n - self.last_print_n
        delta_t = cur_t - self.last_print_t
        total = self.total
        xdata = self.xdata
        ydata = self.ydata
        zdata = self.zdata
        ax = self.ax
        line1 = self.line1
        line2 = self.line2
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
                self.hspan = self.plt.axhspan(0,
                  0.001, xmin=0, xmax=0, color='g')
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
        ax.set_title((self.format_meter(n, total, elapsed, 0, self.desc, self.ascii, self.unit, self.unit_scale, 1 / self.avg_time if self.avg_time else None, self.bar_format, self.postfix, self.unit_divisor)),
          fontname='DejaVu Sans Mono',
          fontsize=11)
        self.plt.pause(1e-09)


def tgrange(*args, **kwargs):
    """
    A shortcut for `tqdm.gui.tqdm(xrange(*args), **kwargs)`.
    On Python3+, `range` is used instead of `xrange`.
    """
    return tqdm_gui(_range(*args), **kwargs)


tqdm = tqdm_gui
trange = tgrange