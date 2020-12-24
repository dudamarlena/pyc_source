# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/display/stemmer.py
# Compiled at: 2010-04-22 06:03:43
"""
This dynamic stemmer shows a live signal stream.
"""
from scipysim.actors import DisplayActor
import matplotlib.pyplot as plt, matplotlib.lines as lines, logging, threading
GUI_LOCK = threading.Condition()
import time

class Stemmer(DisplayActor):
    """
    This actor shows a signal dynamically as it comes off the buffer with matplotlib.
    The max refresh rate is an optional input - default is 2Hz.
    """
    additional_figures = 0
    fig = plt.figure()
    firstPlot = True

    def __init__(self, input_channel, refresh_rate=2, title='Scipy Simulator Dynamic Plot', own_fig=False, xlabel=None, ylabel=None):
        super(Stemmer, self).__init__(input_channel=input_channel)
        self.x_axis_data = []
        self.y_axis_data = []
        assert refresh_rate != 0
        self.refresh_rate = refresh_rate
        self.min_refresh_time = 1.0 / self.refresh_rate
        plt.ioff()
        assert plt.isinteractive() == False
        self.fig_num = self.additional_figures
        if own_fig and not self.firstPlot:
            self.__class__.additional_figures += 1
            with GUI_LOCK:
                fig = self.myfig = plt.figure()
        else:
            fig = self.__class__.fig
        self.ax = fig.add_subplot(1, 1, 1)
        self.title = self.ax.set_title(title)
        self.markerline = None
        self.stemlines = None
        self.baseline = None
        if xlabel is not None:
            self.ax.set_xlabel(xlabel)
        if ylabel is not None:
            self.ax.set_ylabel(ylabel)
        self.refreshs = 0
        self.last_update = 0
        self.__class__.firstPlot = False
        return

    def process(self):
        """
        plot any values in the buffer
        """
        obj = self.input_channel.get(True)
        if obj is None:
            logging.info('We have finished processing the channel of data to be displayed')
            self.update_plot()
            self.stop = True
            return
        else:
            self.x_axis_data.append(obj['tag'])
            self.y_axis_data.append(obj['value'])
            logging.debug('Stemmer received values ( %e,%e ) Now have %i values.' % (self.y_axis_data[(-1)], self.x_axis_data[(-1)], len(self.x_axis_data)))
            obj = None
            if time.time() - self.last_update > 1.0 / self.refresh_rate:
                self.update_plot()
            return

    def update_plot(self):
        """
        Update the internal data stored by matplotlib and cause a redraw.
        If this has been called more than 1000 times -> quit.
        """
        logging.debug('Updating plot (refresh: %i)' % self.refreshs)
        self.last_update = time.time()
        if self.refreshs >= 1000:
            logging.info('We have updated the plot 1000 times - forcing a stop of the simulation now')
            self.stop = True
            return
        self.refreshs += 1
        with GUI_LOCK:
            if not self.markerline:
                (self.markerline, self.stemlines, self.baseline) = self.ax.stem(self.x_axis_data, self.y_axis_data)
            else:
                axes = self.markerline.get_axes()
                self.markerline.set_data(self.x_axis_data, self.y_axis_data)
                self.markerline.recache()
                (_, baseline_y) = self.baseline.get_data()
                self.baseline.set_data([min(self.x_axis_data),
                 max(self.x_axis_data)], baseline_y.tolist())
                self.baseline.recache()
                for (x, y) in zip(self.x_axis_data, self.y_axis_data)[len(self.stemlines):]:
                    stemline = lines.Line2D([0], [0])
                    stemline.update_from(self.stemlines[0])
                    stemline.set_data([x, x], [baseline_y[0], y])
                    stemline.recache()
                    axes.add_line(stemline)
                    self.stemlines.append(stemline)

                axes.relim()
                axes.autoscale_view()