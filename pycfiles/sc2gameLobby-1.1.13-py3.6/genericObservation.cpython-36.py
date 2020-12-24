# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\genericObservation.py
# Compiled at: 2018-07-09 21:33:29
# Size of source mod 2**32: 881 bytes
import multiprocessing

def doNothing(observation):
    """simply ignore the observation
    default callaback unless specified otherwise.
    useful if a human is playing unaided
    """
    pass


class forwardObservation(object):
    __doc__ = 'allow the observation getter to connect to the commander by forwarding observations'

    def __init__(self, pushQueue):
        self.pushQ = pushQueue

    def __call__(self, observation):
        self.pushQ.put(observation)