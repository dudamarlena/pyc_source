# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/math/constant.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 23/11/2009

@author: brian
"""
import logging
from numpy import linspace
from scipysim.actors import Source

class Constant(Source):
    """
    This actor is a constant value source
    """

    def __init__(self, out, value=1.0, resolution=10, simulation_time=120, endpoint=False):
        """
        default parameters creates a constant output of 1.0 for 2 minutes (with 10 values per "second")

        """
        super(Constant, self).__init__(output_channel=out, simulation_time=simulation_time)
        self.resolution = resolution
        self.endpoint = endpoint
        self.value = value

    def process(self):
        """Create the numbers..."""
        logging.debug('Running ramp process')
        tags = linspace(0, self.simulation_time, self.simulation_time * self.resolution, endpoint=self.endpoint)
        [ self.output_channel.put({'tag': tag, 'value': self.value}) for tag in tags
        ]
        logging.debug('Const process finished adding all data to its output channel')
        self.stop = True
        self.output_channel.put(None)
        return