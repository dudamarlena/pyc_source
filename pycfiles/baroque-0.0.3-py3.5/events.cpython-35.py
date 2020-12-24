# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/defaults/events.py
# Compiled at: 2017-03-28 18:07:28
# Size of source mod 2**32: 556 bytes
from baroque.entities.event import Event
from .eventtypes import GenericEventType

class EventFactory:
    __doc__ = 'A factory class that exposes methods to quickly create useful\n    :obj:`baroque.entities.event.Event` instances'

    @classmethod
    def new(cls, **kwargs):
        """Factory method returning a generic type event.
    
        Args:
            **kwargs: positional arguments for `Event` instantiation
    
        Returns:
            :obj:`baroque.entities.event.Event`
    
        """
        return Event(GenericEventType(), **kwargs)