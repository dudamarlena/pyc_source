# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/actors/io/unbundle.py
# Compiled at: 2010-04-22 06:03:43
"""
Created on Feb 2, 2010

@author: brianthorne
"""
from scipysim.actors import Actor

class Unbundle(Actor):
    """Given a bundled source, recreate the channel that made it"""
    num_inputs = 1
    num_outputs = 1

    def __init__(self, input_channel, output_channel):
        super(Unbundle, self).__init__(input_channel=input_channel, output_channel=output_channel)

    def process(self):
        x = self.input_channel.get(True)
        if x is not None:
            [ self.output_channel.put({'tag': tag, 'value': value}) for (tag, value) in x ]
        else:
            self.output_channel.put(None)
            self.stop = True
        return