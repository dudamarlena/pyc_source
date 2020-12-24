# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/signal/ramp.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 23/11/2009

@author: brian
"""
import logging
from numpy import linspace
from scipysim.actors import Source, Actor
import time, random

class Ramp(Source):
    """
    This actor is a ramp source
    """

    def __init__(self, out, amplitude=2.0, freq=1.0 / 30, resolution=10, simulation_time=120, endpoint=False):
        """
        default parameters creates a ramp up to 2 that takes 30 seconds with 10 values per "second"

        """
        super(Ramp, self).__init__(output_channel=out, simulation_time=simulation_time)
        self.amplitude = amplitude
        self.frequency = freq
        self.resolution = resolution
        self.endpoint = endpoint

    def process(self):
        """Create the numbers..."""
        logging.debug('Running ramp process')
        tags = linspace(0, self.simulation_time, self.simulation_time * self.resolution, endpoint=self.endpoint)
        for tag in tags:
            value = tag * self.frequency * self.amplitude
            while value >= self.amplitude:
                value = value - self.amplitude

            data = {'tag': tag, 
               'value': value}
            self.output_channel.put(data)

        logging.debug('Ramp process finished adding all data to channel')
        self.stop = True
        self.output_channel.put(None)
        return