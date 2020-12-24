# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/math/subtract.py
# Compiled at: 2010-04-22 06:03:43
"""
This Sum actor takes any number of input channels and adds up the data points
where the tags coincide, if there are missing tags it can discard the data point
or alternativly sum the remaining inputs.

Created on 24/11/2009

@author: brian
"""
import logging, numpy as np
from scipysim.actors import Actor, Channel

class Subtractor(Actor):
    """Subtraction Actor
    
    This actor takes two signals and subtracts the second
    from the first at the corresponding tagged time.
    This has to be used with discrete signals, or at least aligned continuous signals.
    """
    num_inputs = 2
    num_outputs = 1
    input_domains = (None, None)
    output_domains = (None, )

    def __init__(self, input_1, input_2, output_channel, discard_incomplete_sets=True):
        """
        Constructor for a subtraction block

        @param input_1: input channel for subtracting from.
        
        @param input_2: input channel of values to subtract

        @param output_channel: A single channel where the output will be put.

        @param discard_incomplete_sets: Boolean for either outputting incomplete
        data sets, or discarding.

        """
        Actor.__init__(self, output_channel=output_channel)
        self.input_1 = input_1
        self.input_2 = input_2
        self.discard_incomplete = discard_incomplete_sets
        self.data_is_stored = False
        self.future_data = []

    def process(self):
        """Wait for data from both (all) input channels"""
        logging.debug('Running subtraction process')
        objects = [ in_channel.get(True) for in_channel in [self.input_1, self.input_2] ]
        if objects.count(None) == len(objects):
            logging.info('We have finished subtracting the data')
            self.stop = True
            self.output_channel.put(None)
            return
        else:
            tags = [ obj['tag'] for obj in objects ]
            values = [ obj['value'] for obj in objects ]
            if tags.count(tags[0]) == len(tags):
                new_value = values[0] - values[1]
                logging.debug('Subtractor received all equally tagged inputs, subtracted and sent out: (tag: %2.e, value: %2.e)' % (tags[0], new_value))
                data = {'tag': tags[0], 
                   'value': new_value}
                self.output_channel.put(data)
            else:
                logging.debug('Tags were not all equal... First two tags: %.5e, %.5e' % (tags[0], tags[1]))
                oldest_tag = min(tags + [ a['tag'] for a in self.future_data ])
                if self.data_is_stored:
                    logging.debug('We have got previously stored data - checking for any at oldest tag')
                    current_data = [ obj for obj in self.future_data + objects if obj['tag'] == oldest_tag ]
                else:
                    current_data = [ obj for obj in objects if obj['tag'] == oldest_tag ]
                num_points = len(current_data)
                if num_points == 2 or not self.discard_incomplete:
                    logging.debug('We are subtracting what we have and outputting')
                    the_value = current_data[0]['value'] - current_data[1]['value']
                    self.output_channel.put({'tag': oldest_tag, 
                       'value': the_value})
                else:
                    logging.debug('We are throwing away the oldest tag, and storing the rest')
                self.future_data = [ obj for obj in self.future_data + objects if obj['tag'] is not oldest_tag ]
                if self.future_data is not None:
                    self.data_is_stored = True
            return


import unittest

class SubtractionTests(unittest.TestCase):

    def test_basic_subtract(self):
        """Test subtracting two channels of complete pairs together"""
        q_in_1 = Channel()
        q_in_2 = Channel()
        q_out = Channel()
        input1 = [ {'value': 10, 'tag': i} for i in xrange(100) ]
        input2 = [ {'value': 2, 'tag': i} for i in xrange(100) ]
        block = Subtractor(q_in_1, q_in_2, q_out)
        block.start()
        for val in input1:
            q_in_1.put(val)

        for val in input2:
            q_in_2.put(val)

        q_in_1.put(None)
        q_in_2.put(None)
        block.join()
        for i in xrange(100):
            self.assertEquals(q_out.get()['value'], 8)

        self.assertEquals(q_out.get(), None)
        return


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SubtractionTests)
    unittest.TextTestRunner(verbosity=4).run(suite)