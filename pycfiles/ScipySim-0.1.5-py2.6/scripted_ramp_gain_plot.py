# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/scripted_ramp_gain_plot.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 23/11/2009

@author: brian
"""
from scipysim.actors.display import Plotter
from scipysim.actors import Channel, Model
from scipysim.actors.math import Proportional
from scipysim.actors.signal import Ramp
import logging
logging.basicConfig(level=logging.DEBUG)
logging.info('Logger enabled')

class RampGainPlot(Model):
    """
    This example connects a ramp to a gain to a plotter.
    It could easily have used a different ramp to achieve the same effect.
    """

    def __init__(self):
        """Setup the sim"""
        super(RampGainPlot, self).__init__()
        ramp2gain = Channel()
        gain2plot = Channel()
        src = Ramp(ramp2gain)
        filt = Proportional(ramp2gain, gain2plot)
        dst = Plotter(gain2plot)
        self.components = [
         src, filt, dst]


if __name__ == '__main__':
    SIM = RampGainPlot()
    SIM.run()