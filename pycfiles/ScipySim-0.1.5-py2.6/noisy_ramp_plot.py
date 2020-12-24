# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/models/noisy_ramp_plot.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 23/11/2009

@author: brian
"""
from scipysim.actors import Channel, Model
from scipysim.actors.display.bundlePlotter import BundlePlotter
from scipysim.actors.io import Bundle
from scipysim.actors.signal import Ramp, RandomSource
from scipysim.actors.math import Summer
import logging
logging.basicConfig(level=logging.INFO)
logging.info('Logger enabled')

class NoiseyRamp(Model):
    """
    This model simulates a ramp source and a random source being added together
    The signals are in sync - there are NO missing tags.

    """

    def __init__(self):
        """Setup the simulation"""
        connection1 = Channel()
        connection2 = Channel()
        connection3 = Channel()
        connection4 = Channel()
        src1 = Ramp(connection1)
        src2 = RandomSource(connection2)
        summer = Summer([connection1, connection2], connection3)
        bundler = Bundle(connection3, connection4)
        dst = BundlePlotter(connection4, title='Scipy-Simulation: Noise + Ramp Sum', show=True)
        self.components = [
         src1, src2, summer, bundler, dst]


if __name__ == '__main__':
    NoiseyRamp().run()