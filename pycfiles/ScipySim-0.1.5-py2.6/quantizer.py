# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/signal/quantizer.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on 2010-04-06

@author: Allan McInnes
"""
from scipysim.actors import Siso, Actor, Channel
import logging, unittest
from numpy import floor

class Quantizer(Siso):
    """
    This actor takes an input signal with values at arbitrary levels, and
    generates an output signal with values at corresponding quantization
    levels.
    This quantizer uses a 'floor' function to make the conversion to 
    quantization levels.  
    """

    def __init__(self, input_channel, output_channel, delta=0.5):
        """
        Constructor for a quantizer.
        
        @param delta: the quantization step
        """
        super(Quantizer, self).__init__(input_channel=input_channel, output_channel=output_channel, child_handles_output=True)
        self.delta = delta

    def siso_process(self, obj):
        tag, value = obj['tag'], obj['value']
        logging.debug('Quantizer received (tag: %2.e, value: %2.e )' % (tag, value))
        quantized_value = self.delta * floor(value / self.delta)
        self.output_channel.put({'tag': tag, 'value': quantized_value})


class QuantizerTests(unittest.TestCase):
    """Test the quantizer actor"""

    def setUp(self):
        """
        Unit test setup code
        """
        self.q_in = Channel('CT')
        self.q_out = Channel('CT')

    def test_ramp_quantization(self):
        """
        Test quantizing a simple ramp signal.
        """
        inp = [ {'tag': i, 'value': i} for i in xrange(-20, 21, 1) ]
        quantizer = Quantizer(self.q_in, self.q_out, 2)
        expected_outputs = [ {'tag': i, 'value': i if i % 2 == 0 else i - 1} for i in xrange(-20, 21, 1) ]
        quantizer.start()
        [ self.q_in.put(val) for val in inp ]
        self.q_in.put(None)
        quantizer.join()
        for expected_output in expected_outputs:
            out = self.q_out.get()
            self.assertEquals(out['value'], expected_output['value'])
            self.assertEquals(out['tag'], expected_output['tag'])

        self.assertEquals(self.q_out.get(), None)
        return


if __name__ == '__main__':
    unittest.main()