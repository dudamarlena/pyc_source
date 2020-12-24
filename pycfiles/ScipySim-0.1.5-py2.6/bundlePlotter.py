# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/display/bundlePlotter.py
# Compiled at: 2010-04-22 07:24:55
"""
This plotting actor creates an output image (png) and optionally opens it.
Since static images don't animate very well it gets all the input at once in a "bundle".

@see scipysim.models.multiple_delayed_sum_ramp_plot for a model which uses both dynamic and static plots.
@see noisy_ramp_plot for a model which uses just this static plot.

@author: brianthorne
"""
from scipysim.actors.io import Bundle
from scipysim.actors import Actor, DisplayActor, Channel
import numpy, logging, matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from urllib import quote

class BundlePlotter(Actor):
    """
    A plot that is NOT dynamic. It takes a packet or bundle of events
    and plots it all at once.
    """
    num_inputs = 1
    num_outputs = 0

    def __init__(self, input_channel, title='Scipy Simulation Output', show=False):
        """A bundle plotter takes bundled data in the input channel.
        The individual discrete events must be compressed using the bundler first.
        """
        super(BundlePlotter, self).__init__(input_channel=input_channel)
        self.title = title
        self.show = show

    def process(self):
        """Collect the data in one lot from the channel and create an image"""
        self.data = self.input_channel.get(True)
        if self.data is None:
            self.stop = True
        else:
            assert type(self.data) == numpy.ndarray
            url = self.save_image()
            url = 'file://' + quote(url)
            logging.info("URL for image file is: '%s'" % url)
            if self.show:
                import webbrowser
                webbrowser.open(url)
        return

    def save_image(self):
        self.x_axis_data = self.data['Tag']
        self.y_axis_data = self.data['Value']
        logging.debug('Creating static plot of %d items' % len(self.data))
        f = Figure()
        canvas = FigureCanvas(f)
        a = f.add_subplot(111)
        a.plot(self.x_axis_data, self.y_axis_data)
        a.set_title(self.title)
        a.grid(True)
        canvas.print_figure(filename=self.title, dpi=150)
        logging.debug('Saved output png image.')
        import os
        url = os.path.join(os.getcwd(), self.title) + '.png'
        logging.debug('Image was saved at %s' % url)
        return url