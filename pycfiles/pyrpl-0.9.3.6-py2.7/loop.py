# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/loop.py
# Compiled at: 2017-08-29 09:44:06
"""
Defines a number of Loop modules to be used to perform periodically a task
"""
import numpy as np, pyqtgraph as pg
from ..modules import Module
from ..async_utils import MainThreadTimer
from ..pyrpl_utils import time

class Loop(Module):

    def __init__(self, parent, name='loop', interval=1.0, autostart=True, loop_function=None, setup_function=None, teardown_function=None, **kwargs):
        super(Loop, self).__init__(parent, name=name)
        self.kwargs = kwargs
        if setup_function is not None:
            self.setup_loop = setup_function
        if loop_function is not None:
            self.loop = loop_function
        if teardown_function is not None:
            self.teardown_loop = teardown_function
        self._ended = False
        self.timer = MainThreadTimer(interval=0)
        self.interval = interval
        self.timer.timeout.connect(self.main_loop)
        self.n = 0
        self.time
        try:
            self.setup_loop()
        except TypeError:
            self.setup_loop(self.parent, self)

        if autostart:
            self.main_loop()
        return

    @property
    def time(self):
        """ time since start of the loop """
        try:
            return time() - self.loop_start_time
        except AttributeError:
            self.loop_start_time = time()
            return 0

    @property
    def interval(self):
        return float(self.timer.interval()) / 1000.0

    @interval.setter
    def interval(self, val):
        self.timer.setInterval(val * 1000.0)

    def _clear(self):
        self._ended = True
        self.timer.stop()
        try:
            self.teardown_loop()
        except TypeError:
            self.teardown_loop(self.parent, self)

        super(Loop, self)._clear()

    def main_loop(self):
        try:
            try:
                self.loop()
            except TypeError:
                try:
                    self.loop(self.parent, self)
                except TypeError:
                    self.loop(self.parent)

        except BaseException as e:
            self._logger.error('Error in main_loop of %s: %s', self.name, e)

        self.n += 1
        if not self._ended:
            self.timer.start()

    def setup_loop(self):
        """ put your initialization routine here"""
        pass

    def pause_loop(self):
        self._ended = True

    def start_loop(self):
        self._ended = False
        self.main_loop()

    def loop(self):
        pass

    def teardown_loop(self):
        """ put your destruction routine here"""
        pass

    @property
    def fpga_time(self):
        """ current FPGA time in s since startup """
        return 8e-09 * self.pyrpl.rp.trig.current_timestamp / self.pyrpl.rp.frequency_correction - self.loop_start_time

    @property
    def trigger_time(self):
        """ FPGA time in s when trigger even occured (same frame of reference
        as self.time())"""
        return 8e-09 * self.pyrpl.rp.trig.trigger_timestamp / self.pyrpl.rp.frequency_correction - self.loop_start_time


class PlotWindow(object):
    """ makes a plot window where the x-axis is time since startup.

    append(color=value) adds new data to the plot for
    color in (red, green).

    close() closes the plot"""

    def __init__(self, title='plotwindow'):
        self.win = pg.GraphicsWindow(title=title)
        self.pw = self.win.addPlot()
        self.curves = {}
        self.win.show()
        self.plot_start_time = time()

    _defaultcolors = [
     'g', 'r', 'b', 'y', 'c', 'm', 'o', 'w']

    def append(self, *args, **kwargs):
        """
        usage:
            append(green=0.1, red=0.5, blue=0.21)
        # former, now almost deprecated version:
            append(0.5, 0.6)
        """
        for k in kwargs.keys():
            v = kwargs.pop(k)
            kwargs[k[0]] = v

        i = 0
        for value in args:
            while self._defaultcolors[i] in kwargs:
                i += 1

            kwargs[self._defaultcolors[i]] = value

        t = time() - self.plot_start_time
        for color, value in kwargs.items():
            if value is not None:
                if color not in self.curves:
                    self.curves[color] = self.pw.plot(pen=color)
                curve = self.curves[color]
                x, y = curve.getData()
                if x is None or y is None:
                    x, y = np.array([t]), np.array([value])
                else:
                    x, y = np.append(x, t), np.append(y, value)
                curve.setData(x, y)

        return

    def close(self):
        self.win.close()


class PlotLoop(Loop):

    def __init__(self, *args, **kwargs):
        try:
            self.plot = kwargs.pop('plot')
        except KeyError:
            self.plot = True

        try:
            self.plotter = kwargs.pop('plotter')
        except KeyError:
            self.plotter = None

        if self.plot and self.plotter is None:
            self.plot = PlotWindow(title=self.name)
        super(PlotLoop, self).__init__(*args, **kwargs)
        return

    def plotappend(self, *args, **kwargs):
        if self.plot:
            if self.plotter is not None:
                setattr(self.parent, self.plotter, (args, kwargs))
            else:
                try:
                    self.plot.append(**kwargs)
                except BaseException as e:
                    self._logger.error('Error occured during plotting in Loop %s: %s', self.name, e)

        return

    def _clear(self):
        super(PlotLoop, self)._clear()
        if hasattr(self, 'plot') and hasattr(self.plot, 'close'):
            self.plot.close()