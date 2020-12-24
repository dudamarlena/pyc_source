# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/intids.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 4173 bytes
__doc__ = 'PyAMS_utils.intids module\n\nThis module provides utility functions and helpers to help usage of IIntIds utilities.\nPyramid events subscribers are also declared to match Zope events with Pyramid IntIds related\nevents\n'
from persistent.interfaces import IPersistent
from pyramid.events import subscriber
from pyramid.threadlocal import get_current_registry
from zope.intid import intIdEventNotify
from zope.intid.interfaces import IIntIdEvent, IIntIds, IntIdAddedEvent, IntIdRemovedEvent
from zope.keyreference.interfaces import IKeyReference, NotYet
from zope.lifecycleevent import ObjectRemovedEvent
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectRemovedEvent
from zope.location.interfaces import ISublocations
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.interfaces.intids import IUniqueID
from pyams_utils.registry import get_all_utilities_registered_for, query_utility
__docformat__ = 'restructuredtext'

@adapter_config(context=IPersistent, provides=IUniqueID)
class UniqueIdAdapter(ContextAdapter):
    """UniqueIdAdapter"""

    @property
    def oid(self):
        """Get context ID in hexadecimal form"""
        intids = query_utility(IIntIds)
        if intids is not None:
            return hex(intids.queryId(self.context))[2:]


@subscriber(IObjectAddedEvent, context_selector=IPersistent)
def handle_added_object(event):
    """Notify IntId utility for added objects

    This subscriber is used for all persistent objects to be registered
    in all locally registered IIntIds utilities.
    """
    utilities = tuple(get_all_utilities_registered_for(IIntIds))
    if utilities:
        try:
            key = IKeyReference(event.object, None)
        except NotYet:
            pass
        else:
            if key is not None:
                idmap = {}
                for utility in utilities:
                    idmap[utility] = utility.register(key)

                get_current_registry().notify(IntIdAddedEvent(event.object, event, idmap))


@subscriber(IObjectRemovedEvent, context_selector=IPersistent)
def handle_removed_object(event):
    """Notify IntId utility for removed objects

    This subscriber is used for all persistent objects to be unregistered
    from all locally registered IIntIds utilities.
    """
    registry = get_current_registry()
    locations = ISublocations(event.object, None)
    if locations is not None:
        for location in locations.sublocations():
            registry.notify(ObjectRemovedEvent(location))

    utilities = tuple(get_all_utilities_registered_for(IIntIds))
    if utilities:
        key = IKeyReference(event.object, None)
        if key is not None:
            registry.notify(IntIdRemovedEvent(event.object, event))
            for utility in utilities:
                try:
                    utility.unregister(key)
                except KeyError:
                    pass


@subscriber(IIntIdEvent)
def handle_intid_event(event):
    """IntId event subscriber

    This event is used to dispatch all IIntIdEvent events using Pyramid events subscribers
    to matching subscribers using Zope events
    """
    intIdEventNotify(event)