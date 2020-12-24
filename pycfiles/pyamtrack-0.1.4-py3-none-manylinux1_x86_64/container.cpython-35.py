# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/container.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 5160 bytes
__doc__ = 'PyAMS_utils.container module\n\nThis module provides several classes, adapters and functions about containers.\n'
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
    """BTreeOrderedContainer"""

    def __init__(self):
        self._data = OOBTree()
        self._order = PersistentList()


class ParentSelector:
    """ParentSelector"""

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
    """ContainerSublocationsAdapter"""

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