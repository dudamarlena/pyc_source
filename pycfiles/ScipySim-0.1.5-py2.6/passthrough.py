# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/logic/passthrough.py
# Compiled at: 2010-04-22 07:28:57
"""
This actor makes an "IF" like structure.
The first input is a boolean tagged signal, at the tags where it is true
the other channel's data gets passed on, otherwise discarded.

Created on 13/12/2009

@author: Brian
"""
from scipysim.actors import Actor, Channel
import logging

class PassThrough(Actor):
    """
    This actor takes a boolean tagged signal and a data channel.
    At the tag points where the boolean signal is True, the values from the input are
    passed on to the output, a second data channel can be added as an else clause.

    @note: For now this has to be used with discrete signals, or at least aligned continuous signals.
    """
    num_inputs = 2
    num_outputs = 2
    input_domains = ('BIN', None)
    output_domains = (None, None)

    def __init__(self, bool_input, data_input, output_channel, else_data_input=None):
        """
        Constructor for a PassThrough block

        @param bool_input: A boolean tagged signal.
        
        @param data_input: The data to be passed through if control was True.
        
        @param output_channel: A single channel where the output will be put.

        @param else_data_input: Optional alternative data to be passed on.
        """
        super(PassThrough, self).__init__(output_channel=output_channel)
        self.bool_input = bool_input
        self.data_input = data_input
        self.has_else_clause = else_data_input is not None
        if self.has_else_clause:
            self.else_data_input = else_data_input
        logging.info('We have set up a pass through actor')
        return

    def process(self):
        """Wait for data from both input channels"""
        logging.debug('Running pass-through, blocking on both channels')
        bool_in = self.bool_input.get(True)
        logging.debug('Got a boolean value, waiting for data point')
        data_in = self.data_input.get(True)
        if self.has_else_clause:
            else_data_in = self.else_data_input.get(True)
        if bool_in is None and data_in is None:
            logging.info('We have finished PassingThrough the data')
            self.stop = True
            self.output_channel.put(None)
            return
        else:
            logging.debug('Received a boolean and a data point. Tags = (%e,%e)' % (bool_in['tag'], data_in['tag']))
            assert bool_in['tag'] == data_in['tag']
            if bool_in['value'] is True:
                logging.debug('The input was positive, passing data through')
                self.output_channel.put(data_in)
            elif self.has_else_clause:
                self.output_channel.put(else_data_in)
            else:
                logging.debug('Discarding data.')
            return