# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/signal/delay.py
# Compiled at: 2010-04-22 07:32:36
"""
Created on 23/11/2009

@author: Brian Thorne
"""
import logging
from scipysim.actors import Siso, Channel
import unittest, numpy

class Delay(Siso):
    """
    This siso actor takes a source and delays it by an arbitrary amount of time.
    """

    def __init__(self, input_channel, output_channel, wait=1.0 / 10):
        """
        Constructor for a delay block.

        @param input_channel: The input channel to be delayed

        @param output_channel: The output channel that has been delayed

        @param wait: The delay time in seconds. Defaults to delaying
                     the signal by one tenth of a second.
        """
        super(Delay, self).__init__(input_channel=input_channel, output_channel=output_channel)
        self.delay = wait

    def siso_process(self, obj):
        """Delay the input values by a set amount of time..."""
        logging.debug('Running delay process')
        tag = obj['tag'] + self.delay
        value = obj['value']
        data = {'tag': tag, 
           'value': value}
        return data


from numpy import linspace, arange

class DelayTests(unittest.TestCase):

    def setUp(self):
        self.q_in = Channel()
        self.q_out = Channel()

    def tearDown(self):
        del self.q_in
        del self.q_out

    def test_basic_delay(self):
        """Test delaying a basic integer tagged signal by 1"""
        delay = 2
        input1 = [ {'value': 1, 'tag': i} for i in xrange(100) ]
        expected_output = [ {'value': 1, 'tag': i + delay} for i in xrange(100) ]
        block = Delay(self.q_in, self.q_out, delay)
        block.start()
        [ self.q_in.put(i) for i in input1 + [None] ]
        block.join()
        actual_output = [ self.q_out.get() for i in xrange(100) ]
        [ self.assertEquals(actual_output[i], expected_output[i]) for i in xrange(100) ]
        self.assertEquals(None, self.q_out.get())
        return

    def test_complex_delay(self):
        """Test delaying a CT signal"""
        delay = 11.5
        simulation_time = 120
        resolution = 10.0
        tags = linspace(0, simulation_time, simulation_time / resolution)
        values = arange(len(tags))
        data_in = [ {'value': values[i], 'tag': tags[i]} for i in xrange(len(tags)) ]
        expected_output = [ {'value': values[i], 'tag': tags[i] + delay} for i in xrange(len(tags)) ]
        block = Delay(self.q_in, self.q_out, delay)
        block.start()
        [ self.q_in.put(i) for i in data_in + [None] ]
        block.join()
        actual_output = [ self.q_out.get() for i in xrange(len(tags)) ]
        [ self.assertEquals(actual_output[i], expected_output[i]) for i in xrange(len(tags)) ]
        self.assertEquals(None, self.q_out.get())
        return


if __name__ == '__main__':
    unittest.main()