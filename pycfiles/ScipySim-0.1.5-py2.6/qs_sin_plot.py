# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/qs_sin_plot.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 2010-04-06

@author: Allan McInnes
"""
from scipysim.actors import Channel, Model
from scipysim.actors.display import Plotter, Stemmer
from scipysim.actors.math.trig import CTSinGenerator
from scipysim.actors.signal import EventFilter
import numpy, logging
logging.basicConfig(level=logging.INFO)
logging.info('Logger enabled')

class QSSinPlot(Model):
    """
    Plot of a CT sinusoidal converted to a quantized-state representation.   
    """

    def __init__(self):
        """Setup the simulation"""
        super(QSSinPlot, self).__init__()
        connection1 = Channel(domain='CT')
        connection2 = Channel(domain='CT')
        src = CTSinGenerator(connection1, 2.1, 0.2, numpy.pi / 2)
        de = EventFilter(connection1, connection2, 0.2)
        dst = Stemmer(connection2, refresh_rate=1.0 / 2)
        self.components = [
         src, de, dst]


if __name__ == '__main__':
    QSSinPlot().run()