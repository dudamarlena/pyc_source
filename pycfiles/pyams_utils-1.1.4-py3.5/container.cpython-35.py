# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/container.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 5160 bytes
"""PyAMS_utils.container module

This module provides several classes, adapters and functions about containers.
"""
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry
from zope.container.interfaces import IContained, IContainer
from zope.container.ordered import OrderedContainer
from zope.lifecycleevent.interfaces import IObjectMovedEvent
from zope.location.interfaces import ISublocations
from pyams_utils.adapter import ContextAdapter, adapter_config
__docformat__ = 'restructuredtext'

class BTreeOrderedContainer(OrderedContainer):
    __doc__ = "BTree based ordered container\n\n    This container maintain a manual order of it's contents\n    "

    def __init__(self):
        self._data = OOBTree()
        self._order = PersistentList()


class ParentSelector:
    __doc__ = "Interface based parent selector\n\n    This selector can be used as a subscriber predicate on IObjectAddedEvent to define\n    an interface that the new parent must support for the event to be applied:\n\n    .. code-block:: python\n\n        from pyams_utils.interfaces.site import ISiteRoot\n\n        @subscriber(IObjectAddedEvent, parent_selector=ISiteRoot)\n        def siteroot_object_added_event_handler(event):\n            '''This is an event handler for an ISiteRoot object added event'''\n    "

    def __init__(self, ifaces, config):
        if not isinstance(ifaces, (list, tuple, set)):
            ifaces = (
             ifaces,)
        self.interfaces = ifaces

    def text(self):
        """Predicate string output"""
        return 'parent_selector = %s' % str(self.interfaces)

    phash = text

    def __call__(self, event):
        if not IObjectMovedEvent.providedBy(event):
            return False
        for intf in self.interfaces:
            try:
                if intf.providedBy(event.newParent):
                    return True
            except (AttributeError, TypeError):
                if isinstance(event.newParent, intf):
                    return True

        return False


@adapter_config(context=IContained, provides=ISublocations)
class ContainerSublocationsAdapter(ContextAdapter):
    __doc__ = 'Contained object sub-locations adapter\n\n    This adapter checks for custom ISublocations interface adapters which can\n    be defined by any component to get access to inner locations, defined for\n    example via annotations.\n    '

    def sublocations(self):
        """See `zope.location.interfaces.ISublocations` interface"""
        context = self.context
        registry = get_current_registry()
        for name, adapter in registry.getAdapters((context,), ISublocations):
            if not name:
                pass
            else:
                yield from adapter.sublocations()

        if IContainer.providedBy(context):
            yield from context.values()


def find_objects_matching(root, condition, ignore_root=False):
    """Find all objects in root that match the condition

    The condition is a Python callable object that takes an object as
    argument and must return a boolean result.

    All sub-objects of the root will also be searched recursively.

    :param object root: the parent object from which search is started
    :param callable condition: a callable object which may return true for a given
        object to be selected
    :param boolean ignore_root: if *True*, the root object will not be returned, even if it matches
        the given condition
    :return: an iterator for all root's sub-objects matching condition
    """
    if not ignore_root and condition(root):
        yield root
    locations = ISublocations(root, None)
    if locations is not None:
        for location in locations.sublocations():
            if condition(location):
                yield location
            yield from find_objects_matching(location, condition, ignore_root=True)


def find_objects_providing(root, interface):
    """Find all objects in root that provide the specified interface

    All sub-objects of the root will also be searched recursively.

    :param object root: object; the parent object from which search is started
    :param Interface interface: interface; an interface that sub-objects should provide
    :return: an iterator for all root's sub-objects that provide the given interface
    """
    yield from find_objects_matching(root, interface.providedBy)