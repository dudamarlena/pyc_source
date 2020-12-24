# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/sum_sin_plot.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 03/12/2009

@author: allan
"""
from scipysim.actors import Channel, Model
from scipysim.actors.display import Plotter
from scipysim.actors.math import Summer
from scipysim.actors.math.trig import CTSinGenerator
import numpy, logging
logging.basicConfig(level=logging.INFO)
logging.info('Logger enabled')

class SumSinPlot(Model):
    """
    Summing two continous sinusoidal sources together and plotting. 
    """

    def __init__(self):
        """Setup the simulation"""
        super(SumSinPlot, self).__init__()
        connection1 = Channel(domain='CT')
        connection2 = Channel(domain='CT')
        connection3 = Channel()
        src1 = CTSinGenerator(connection1, 2, 2.0, numpy.pi / 2)
        src2 = CTSinGenerator(connection2, 1, 3.5, numpy.pi / 4)
        summer = Summer([connection1, connection2], connection3)
        dst = Plotter(connection3, refresh_rate=1.0 / 2)
        self.components = [
         src1, src2, summer, dst]


if __name__ == '__main__':
    SumSinPlot().run()