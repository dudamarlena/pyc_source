# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/overlay/pilot_description.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import os, radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class PilotDescription(tu.Properties):
    """
    The `PilotDescription` class is a simple container for properties which
    describe a :class:`Pilot`, i.e. a overlay element.  `PilotDescription`s are
    submitted to :class:`OverlayManager` instances on `add_pilot`, and are
    internally used to create :class:`Pilot` instances.

    FIXME: description of supported properties goes here
    """

    def __init__(self, descr={}):
        tu.Properties.__init__(self, descr)
        self.size = 1
        for key in descr:
            self.set_attribute(key, descr[key])

    def __str__(self):
        return str(self.as_dict())