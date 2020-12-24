# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/events.py
# Compiled at: 2012-06-20 11:31:01
from zope.catalog.interfaces import ICatalog
from zope.lifecycleevent.interfaces import IObjectCopiedEvent, IObjectAddedEvent, IObjectRemovedEvent
from ztfy.file.interfaces import IFilePropertiesContainer, IFilePropertiesContainerAttributes
from ZODB.blob import Blob
from zope.component import adapter, getUtilitiesFor
from zope.event import notify
from zope.lifecycleevent import ObjectRemovedEvent
from zope.location import locate
from ztfy.extfile.blob import BaseBlobFile
from ztfy.utils import catalog

@adapter(IFilePropertiesContainer, IObjectCopiedEvent)
def handleCopiedFilePropertiesContainer(object, event):
    """When a file properties container is copied, we have to tag it for indexation and update it's blobs
    
    Effective file indexation will be done only after content have been added to it's new parent container"""
    object._v_copied_file = True
    source = event.original
    for attr in IFilePropertiesContainerAttributes(source).attributes:
        value = getattr(source, attr, None)
        if isinstance(value, BaseBlobFile):
            getattr(object, attr)._blob = Blob()
            getattr(object, attr).data = value.data

    return


@adapter(IFilePropertiesContainer, IObjectAddedEvent)
def handleAddedFilePropertiesContainer(object, event):
    """When a file properties container is added, we must index it's attributes"""
    if not hasattr(object, '_v_copied_file'):
        return
    else:
        for _name, catalog_util in getUtilitiesFor(ICatalog):
            for attr in IFilePropertiesContainerAttributes(object).attributes:
                value = getattr(object, attr, None)
                if value is not None:
                    locate(value, object, value.__name__)
                    catalog.indexObject(value, catalog_util)

        delattr(object, '_v_copied_file')
        return


@adapter(IFilePropertiesContainer, IObjectRemovedEvent)
def handleRemovedFilePropertiesContainer(object, event):
    """When a file properties container is added, we must index it's attributes"""
    for _name, catalog_util in getUtilitiesFor(ICatalog):
        for attr in IFilePropertiesContainerAttributes(object).attributes:
            value = getattr(object, attr, None)
            if value is not None:
                notify(ObjectRemovedEvent(value))
                catalog.unindexObject(value, catalog_util)

    return