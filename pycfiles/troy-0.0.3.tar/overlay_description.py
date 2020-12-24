# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/overlay/overlay_description.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class OverlayDescription(tu.Properties):
    """
    The `OverlayDescription` class is a simple container for properties which
    describe a :class:`Overlay`.  `OverlayDescription`s passed to `Overlay`
    instances on construction, to initialize their configuration.

    FIXME: description of supported properties goes here
    """

    def __init__(self, descr=None):
        if not descr:
            descr = dict()
        tu.Properties.__init__(self, descr)
        self.register_property('workload_id')
        self.register_property('cores')
        self.register_property('walltime')

    def __str__(self):
        return str(self.as_dict())