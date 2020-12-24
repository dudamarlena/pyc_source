# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/sin_double_integral.py
# Compiled at: 2010-04-22 06:03:43
"""
A simple example using DE integrators to double-integrate a sinusoid.

The expected output is:
    * 1st integral should be a cosine with a DC offset, and an amplitude
      less than 1 (peak to peak amplitude is a little over 0.6 in this case)
    * 2nd integral should be a sinusoid riding on a ramp (caused by the
      DC offset of the 1st integral).
      
The results match pretty well with a similar system simulated in Simulink.

Created on 2010-03-22
@author: Allan McInnes
"""
from scipysim.actors import Model, MakeChans
from scipysim.actors.display import Plotter, Stemmer
from scipysim.actors.signal import Copier
from scipysim.actors.math import CTIntegratorDE1
from scipysim.actors.math.trig import CTSinGenerator
import numpy, logging
logging.basicConfig(level=logging.INFO)
logging.info('Logger enabled')

class SinDoubleIntegral(Model):
    """
    Double-integration of a sinusoid 
    """

    def __init__(self):
        """Set up the simulation"""
        super(SinDoubleIntegral, self).__init__()
        wires = MakeChans(10)
        self.components = [
         CTSinGenerator(wires[0], 1, 0.5, 0.0),
         Copier(wires[0], [wires[1], wires[2]]),
         CTIntegratorDE1(wires[1], wires[3], init=0.0, delta=0.001, k=10),
         Copier(wires[3], [wires[4], wires[5]]),
         CTIntegratorDE1(wires[5], wires[6], init=0.0, delta=0.001, k=10),
         Plotter(wires[2], title='Input', own_fig=True),
         Plotter(wires[4], title='1st Integral', own_fig=True),
         Plotter(wires[6], title='2nd Integral', own_fig=True)]


if __name__ == '__main__':
    SinDoubleIntegral().run()