# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/handle/handle.py
# Compiled at: 2009-08-14 17:29:29
"""This module defines the interface provided by the base event handler."""
from zope.interface import Interface, Attribute

class IHandle(Interface):
    """This is the base event handler interface.  All handlers must define
    a run method."""

    def run(self):
        """Execute the event handler."""
        pass

    def get_event(self):
        """Return the event associated with this handle."""
        pass

    def get_event_data(self, key):
        """Return event data from the event data dictionary using the
        specified key."""
        pass


__all__ = [
 'IHandle']