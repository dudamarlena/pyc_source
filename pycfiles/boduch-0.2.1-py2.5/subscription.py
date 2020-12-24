# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/subscription/subscription.py
# Compiled at: 2009-08-14 17:29:30
"""This module defines the base event handle Subscription class."""
from zope.interface import implements
from boduch.interface import ISubscription
from boduch.type import Type

class Subscription(Type):
    """The Subscription class.  Instances of this class represent a
    specific handle subscribing to a specific event."""
    implements(ISubscription)

    def __init__(self, event, handle):
        """Constructor.  Initialize the event class and the handle class."""
        Type.__init__(self)
        self.event = event
        self.handle = handle

    def subscribe(self, handle):
        """Subscribe an additional handle to the event represented by this
        subscription instance."""
        return self.event.subscribe(handle)

    def unsubscribe(self, handle):
        """Unsubscribe a handle from the event represented by this
        subscription instance."""
        self.event.unsubscribe(handle)


__all__ = [
 'Subscription']