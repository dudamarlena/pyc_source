# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/signal/copier.py
# Compiled at: 2010-04-22 06:03:43
import logging
from scipysim.actors import Actor, Channel

class Copier(Actor):
    """
    This actor takes a source and copies it to a number of outputs.
    """
    num_inputs = 1
    num_outputs = None
    input_domains = (None, )
    output_domains = (None, )

    def __init__(self, input_channel, outputs):
        """
        Constructor for a Copier Actor.
        
        @param input_channel: The input data channel to be copied
        
        @param outputs: A list of channels to copy the data to.
        """
        super(Copier, self).__init__(input_channel=input_channel)
        self.output_channels = outputs

    def process(self):
        """Just copy the input data to all the outputs..."""
        logging.debug('Running copier process')
        obj = self.input_channel.get(True)
        if obj is None:
            logging.info('We have finished copying the data')
            self.stop = True
            [ q.put(None) for q in self.output_channels ]
            return
        else:
            [ q.put(obj.copy()) for q in self.output_channels ]
            obj = None
            return


import unittest

class CopierTests(unittest.TestCase):
    """Test the Copier Actor"""

    def test_basic_copy(self):
        """Test getting two for the price of one - cloning a channel"""
        q_in = Channel()
        q_out1 = Channel()
        q_out2 = Channel()
        inp = {'value': 15, 'tag': 1}
        cloneQ = Copier(q_in, [q_out1, q_out2])
        cloneQ.start()
        q_in.put(inp)
        q_in.put(None)
        cloneQ.join()
        out1 = q_out1.get()
        self.assertEquals(out1['value'], inp['value'])
        self.assertEquals(out1['tag'], inp['tag'])
        self.assertEquals(q_out1.get(), None)
        out2 = q_out2.get()
        self.assertEquals(out2['value'], inp['value'])
        self.assertEquals(out2['tag'], inp['tag'])
        self.assertEquals(q_out2.get(), None)
        return


if __name__ == '__main__':
    unittest.main()