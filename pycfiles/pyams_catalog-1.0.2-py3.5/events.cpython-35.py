# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/events.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 1955 bytes
"""PyAMS_catalog.events module

This module register events subscribers which are automatically used to index, reindex or
unindex a content during it's lifecycle when it is added, modified or removed.
"""
from hypatia.interfaces import ICatalog
from persistent import IPersistent
from pyramid.events import subscriber
from zope.intid.interfaces import IIntIdRemovedEvent
from zope.lifecycleevent import IObjectAddedEvent, IObjectModifiedEvent
from pyams_catalog.utils import index_object, reindex_object, unindex_object
from pyams_utils.registry import get_utilities_for
__docformat__ = 'restructuredtext'

@subscriber(IObjectAddedEvent, context_selector=IPersistent)
def handle_new_object(event):
    """Index new persistent object"""
    for _, catalog in get_utilities_for(ICatalog):
        index_object(event.object, catalog, ignore_notyet=True)


@subscriber(IObjectModifiedEvent, context_selector=IPersistent)
def handle_modified_object(event):
    """Update catalog for modified persistent object"""
    for _, catalog in get_utilities_for(ICatalog):
        reindex_object(event.object, catalog)


@subscriber(IIntIdRemovedEvent, context_selector=IPersistent)
def handle_removed_object(event):
    """Un-index removed persistent object

    Don't use IObjectRemovedEvent to avoid objects from being already unregistered
    from IIntId utility!!!
    """
    for _, catalog in get_utilities_for(ICatalog):
        unindex_object(event.object, catalog)