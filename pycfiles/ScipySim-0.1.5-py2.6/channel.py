# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/core/channel.py
# Compiled at: 2010-04-22 06:03:43
"""
Contains the Channel class and helper functions for creating multiple channels.
"""
from Queue import Queue
from copy import deepcopy as copy

class Channel(Queue, object):
    """
    A Channel is based on the Python Queue, used for communicating between Actor threads.
    
    A Channel must be created for a specific domain:
        * CT - Continuous Time
        * DT - Discrete Time
        * DE - Discrete Event
        
    @param domain: The two letter domain code as a string
    """

    def __init__(self, domain='CT'):
        """Construct a queue with domain type information.
        
        @param domain: The specific domain of events that this channel will carry.
                        - defaults to "CT" domain.
        """
        super(Channel, self).__init__()
        self.domain = domain

    def put(self, new_item, *args, **kwargs):
        """
        Put an item into this channel, ensures immutable by copying.
        """
        if new_item is not None:
            item = copy(new_item)
        else:
            item = None
        super(Channel, self).put(item, args, kwargs)
        return


def MakeChans(num):
    """Return a list of n channels.
    
    @param num of channels to create.
    """
    return [ Channel() for i in xrange(num) ]