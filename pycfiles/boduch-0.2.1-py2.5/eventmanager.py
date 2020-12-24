# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/event/eventmanager.py
# Compiled at: 2009-08-14 17:29:28
"""This module defines the IEventManager interface."""
from zope.interface import Interface, Attribute

class IEventManager(Interface):
    subscriptions = Attribute('Stores all event subscriptions.')
    queue = Attribute('The queue where threaded handles are placed.')

    def get_subscriptions(cls, evt=None):
        """Return the handles for the specified event."""
        pass

    def publish(cls, evt, args=[], kw={}, atomic=False):
        """Publish the specified event."""
        pass

    def subscribe(cls, evt, handle):
        """Subscribe the specified handle to the specified event."""
        pass

    def unsubscribe(cls, evt, handle):
        """Remove the subscription of the specified handle to the specified
        event."""
        pass

    def prioritize(cls, evt):
        """Sort the list of subscribers to the specified event,
        making the largest handles first."""
        pass

    def build_handlers(cls, evt, params={}):
        """Build the Handle instances that are currently subcribers to
        the specified event.  The instance is also passed the specified
        keyword parameters."""
        pass


__all__ = [
 'IEventManager']