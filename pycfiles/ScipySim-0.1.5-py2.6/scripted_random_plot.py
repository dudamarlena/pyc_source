# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/scripted_random_plot.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 23/11/2009

@author: brian
"""
from scipysim.actors import Channel, Model
from scipysim.actors.display import Plotter
from scipysim.actors.signal import RandomSource

class RandomPlot(Model):
    """
    Run a simple example connecting a random source with a plotter
    """

    def __init__(self):
        """Run the simulation"""
        super(RandomPlot, self).__init__()
        connection = Channel()
        src = RandomSource(connection)
        dst = Plotter(connection)
        self.components = [
         src, dst]


if __name__ == '__main__':
    RandomPlot().run()