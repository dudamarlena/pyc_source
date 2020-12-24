# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/interfaces.py
# Compiled at: 2009-08-25 18:19:45
"""
ModiPy interfaces
"""
from zope.interface import Interface, implements
import logging, debug
log = logging.getLogger('modipy')

class IProvisioner(Interface):
    """
    Defines the Provisioner interface
    """

    def __init__(self, name='', namespace={}):
        """
        """
        pass

    def perform_change(self, ignored, change):
        """
        Applies a change to the devices the change is defined to affect.
        """
        pass

    def apply_change(self, device, change):
        """
        Apply a change to a specific device.
        """
        pass

    def backout_change(self, device, change):
        """
        Back out a change that was applied to a specific device.
        """
        pass