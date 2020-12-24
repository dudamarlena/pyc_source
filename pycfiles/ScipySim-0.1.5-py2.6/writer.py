# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/io/writer.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Feb 1, 2010

@author: brianthorne
"""
from scipysim.actors import Actor
from scipysim.actors import Channel
import numpy

class Writer(Actor):
    """
    This Actor writes tagged signal data to a file.
    It uses numpy to write a binary file, first it gets all the input
    So make sure the signal can fit in memory!
    """
    num_outputs = 0
    num_inputs = 1

    def __init__(self, input_channel, file_name='./signal_data.dat'):
        """
        Constructor for a File Writer Actor
        """
        super(Writer, self).__init__(input_channel=input_channel)
        self.filename = file_name
        self.temp_data = []

    def process(self):
        obj = self.input_channel.get(True)
        self.temp_data.append(obj)
        if obj is None:
            self.write_file()
            self.stop = True
            return
        else:
            return

    def write_file(self):
        x = numpy.zeros(len(self.temp_data), dtype={'names': [
                   'Tag', 'Value'], 
           'formats': [
                     'f8', 'f8'], 
           'titles': [
                    'Domain', 'Name']})
        x[:(-1)] = [ (element['tag'], element['value']) for element in self.temp_data if element is not None ]
        numpy.save(self.filename, x)
        return