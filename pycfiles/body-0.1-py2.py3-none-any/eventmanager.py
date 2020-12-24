# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/event/eventmanager.py
# Compiled at: 2009-08-14 17:29:28
__doc__ = 'This module defines the IEventManager interface.'
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