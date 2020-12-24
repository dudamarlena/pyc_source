# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/signal/interpolator.py
# Compiled at: 2010-04-22 07:33:36
"""
Interpolation actors. Inserts additional events between each pair of events, using
a selected interpolation scheme.The interpolation schemes are:
    
* zero interpolation - insert zero values
* step interpolation - holds the last value
* linear interpolation - places values on a straight line between successive events

@author: Brian Thorne
@author: Allan McInnes

Created on 1/12/2009
"""
from scipysim.actors import Siso, Channel, SisoTestHelper
import logging, unittest

class Interpolator(Siso):
    """
    Abstract base class for interpolation actors.
    """

    def __init__(self, input_channel, output_channel, interpolation_factor=2):
        """
        Constructor for an interpolation actor. 
                
        @param interpolation_factor: the number of events in the signal will be increased
                                     by this factor. For interpolation_factor N, the interpolator
                                     will add N-1 events between each pair of input events.
        """
        super(Interpolator, self).__init__(input_channel=input_channel, output_channel=output_channel, child_handles_output=True)
        self.interpolation_factor = int(interpolation_factor)
        self.last_event = None
        self.last_out_tag = None
        self.domain = input_channel.domain
        return

    def interpolate(self, event, tag):
        """This method must be overridden. It implements the interpolation algorithm
        based on the current and previous events.
        @return an event
        """
        raise NotImplementedError

    def siso_process(self, event):
        if self.last_event:
            for i in range(1, self.interpolation_factor):
                tag = self.last_event['tag'] + (event['tag'] - self.last_event['tag']) * (i / float(self.interpolation_factor))
                new_event = self.interpolate(event, tag)
                if self.domain == 'DT':
                    assert self.last_out_tag is not None
                    new_event['tag'] = self.last_out_tag + i
                print new_event['tag']
                self.output_channel.put(new_event)

        self.last_event = event.copy()
        if self.domain == 'DT' and self.last_out_tag is not None:
            event['tag'] = self.last_out_tag + self.interpolation_factor
        self.last_out_tag = event['tag']
        self.output_channel.put(event)
        return


class InterpolatorZero(Interpolator):
    """zero interpolation - insert zero values."""

    def interpolate(self, event, tag):
        return {'tag': tag, 'value': 0.0}


class InterpolatorStep(Interpolator):
    """step interpolation - holds the last value."""

    def interpolate(self, event, tag):
        return {'tag': tag, 'value': self.last_event['value']}


class InterpolatorLinear(Interpolator):
    """linear interpolation - places values on a straight line between 
       successive events.
    """

    def interpolate(self, event, tag):
        m = (event['value'] - self.last_event['value']) / (event['tag'] - self.last_event['tag'])
        dt = tag - self.last_event['tag']
        val = m * dt + self.last_event['value']
        return {'tag': tag, 'value': val}


class InterpolateTests(unittest.TestCase):
    """Test the interpolation actors"""

    def setUp(self):
        """
        Unit test setup code
        """
        self.q_in = Channel()
        self.q_out = Channel()

    def test_zero_interpolation_ct(self):
        """Test zero interpolation of a simple CT signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(-10, 11, 2) ]
        expected_outputs = [ {'tag': t, 'value': t if not t % 2 else 0.0} for t in xrange(-10, 11, 1)
                           ]
        block = InterpolatorZero(self.q_in, self.q_out)
        SisoTestHelper(self, block, inp, expected_outputs)

    def test_zero_interpolation_dt(self):
        """Test zero interpolation of a simple DT signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(-10, 11, 1) ]
        expected_outputs = [ {'tag': t, 'value': t / 2.0 - 5.0 if not t % 2 else 0.0} for t in xrange(-10, 31, 1)
                           ]
        self.q_in = Channel('DT')
        self.q_out = Channel('DT')
        block = InterpolatorZero(self.q_in, self.q_out)
        SisoTestHelper(self, block, inp, expected_outputs)

    def test_step_interpolation_ct(self):
        """Test step interpolation of a simple CT signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(-10, 11, 2) ]
        expected_outputs = [ {'tag': t, 'value': t if not t % 2 else t - 1} for t in xrange(-10, 11, 1)
                           ]
        block = InterpolatorStep(self.q_in, self.q_out)
        SisoTestHelper(self, block, inp, expected_outputs)

    def test_step_interpolation_dt(self):
        """Test step interpolation of a simple DT signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(-10, 11, 1) ]
        expected_outputs = [ {'tag': t, 'value': t / 2.0 - 5.0 if not t % 2 else (t - 1) / 2.0 - 5.0} for t in xrange(-10, 31, 1)
                           ]
        self.q_in = Channel('DT')
        self.q_out = Channel('DT')
        block = InterpolatorStep(self.q_in, self.q_out)
        SisoTestHelper(self, block, inp, expected_outputs)

    def test_linear_interpolation_ct(self):
        """Test linear interpolation of a simple CT signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(-10, 11, 2) ]
        expected_outputs = [ {'tag': t, 'value': t} for t in xrange(-10, 11, 1) ]
        block = InterpolatorLinear(self.q_in, self.q_out)
        SisoTestHelper(self, block, inp, expected_outputs)

    def test_linear_interpolation_dt(self):
        """Test linear interpolation of a simple DT signal.
        """
        inp = [ {'value': i, 'tag': i} for i in xrange(-10, 11, 1) ]
        expected_outputs = [ {'tag': t, 'value': t / 2.0 - 5.0} for t in xrange(-10, 31, 1)
                           ]
        self.q_in = Channel('DT')
        self.q_out = Channel('DT')
        block = InterpolatorLinear(self.q_in, self.q_out)
        SisoTestHelper(self, block, inp, expected_outputs)


if __name__ == '__main__':
    unittest.main()