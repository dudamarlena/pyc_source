# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/handle/handle.py
# Compiled at: 2009-08-14 17:29:29
__doc__ = 'This module defines the interface provided by the base event handler.'
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