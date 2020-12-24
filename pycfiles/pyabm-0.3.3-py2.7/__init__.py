# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyabm\__init__.py
# Compiled at: 2013-02-01 18:32:08
"""
Sets up rc parameters so that they can be loaded and reused by other parts of 
the toolkit.
"""
__version__ = '0.3.3'
import os, sys, warnings, logging
logger = logging.getLogger(__name__)
import numpy as np
from rcsetup import rc_params_management

class IDError(Exception):
    pass


class IDGenerator(object):
    """A generator class for consecutive unique ID numbers. IDs can be assigned 
    externally by other code, and tracked in this class with the use_ID 
    function. The use_ID function will raise an error if called with an ID that has 
    already been assigned."""

    def __init__(self):
        self._last_ID = -1
        self._used_IDs = []

    def reset(self):
        self.__init__()

    def next(self):
        newID = self._last_ID + 1
        while newID in self._used_IDs:
            newID += 1

        self._last_ID = newID
        self._used_IDs.append(newID)
        return newID

    def use_ID(self, used_ID):
        if used_ID in self._used_IDs:
            raise IDError('ID %s has already been used' % used_ID)
        self._used_IDs.append(used_ID)


def boolean_choice(trueProb=0.5):
    """A function that returns true or false depending on whether a randomly
    drawn float is less than trueProb"""
    if np.random.rand() < trueProb:
        return True
    else:
        return False


rc_params = rc_params_management()
rc_params.initialize(__name__)