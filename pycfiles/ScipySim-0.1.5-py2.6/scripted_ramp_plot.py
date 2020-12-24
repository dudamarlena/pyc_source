# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/scripted_ramp_plot.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 23/11/2009

@author: brian
"""
from scipysim.actors.signal import Ramp
from scipysim.actors.display import Plotter
from scipysim.actors import Channel, Model

class RampPlot(Model):
    """This example simulation connects a ramp source to a plotter."""

    def __init__(self):
        """Create the components"""
        super(RampPlot, self).__init__()
        connection = Channel()
        src = Ramp(connection)
        dst = Plotter(connection, xlabel='Time (s)', ylabel='Amplitude', title='Ramp Plot')
        self.components = [
         src, dst]


if __name__ == '__main__':
    RampPlot().run()