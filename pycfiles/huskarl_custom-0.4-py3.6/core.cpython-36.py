# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/huskarl/core.py
# Compiled at: 2019-06-13 12:59:36
# Size of source mod 2**32: 794 bytes


class HkException(Exception):
    __doc__ = 'Basic exception for errors raised by Huskarl.'


class Agent:
    __doc__ = 'Abstract base class for all implemented agents.\n\n\tDo not use this abstract base class directly but instead use one of the concrete agents implemented.\n\n\tTo implement your own agent, you have to implement the following methods:\n\t'

    def save(self, filename, overwrite=False):
        """Saves the model parameters to the specified file."""
        raise NotImplementedError()

    def act(self, state, instance=0):
        """Returns the action to be taken given a state."""
        raise NotImplementedError()

    def push(self, transition, instance=0):
        """Stores the transition in memory."""
        raise NotImplementedError()

    def train(self, step):
        """Trains the agent for one step."""
        raise NotImplementedError()