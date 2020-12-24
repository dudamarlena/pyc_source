# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/events.py
# Compiled at: 2012-06-20 11:46:34
from zope.catalog.interfaces import ICatalog
from zope.lifecycleevent.interfaces import IObjectCopiedEvent, IObjectAddedEvent, IObjectRemovedEvent
from ztfy.i18n.interfaces import II18nFilePropertiesContainer, II18nFilePropertiesContainerAttributes
from ZODB.blob import Blob
from zope.lifecycleevent import ObjectRemovedEvent
from zope.component import adapter, getUtilitiesFor
from zope.event import notify
from zope.location import locate
from ztfy.extfile.blob import BaseBlobFile
from ztfy.utils import catalog

@adapter(II18nFilePropertiesContainer, IObjectAddedEvent)
def handleAddedI18nFilePropertiesContainer(object, event):
    if not hasattr(object, '_v_copied_file'):
        return
    else:
        for _name, catalog_util in getUtilitiesFor(ICatalog):
            for attr in II18nFilePropertiesContainerAttributes(object).attributes:
                for value in getattr(object, attr, {}).values():
                    if value is not None:
                        locate(value, object, value.__name__)
                        catalog.indexObject(value, catalog_util)

        delattr(object, '_v_copied_file')
        return


@adapter(II18nFilePropertiesContainer, IObjectRemovedEvent)
def handleRemovedI18nFilePropertiesContainer(object, event):
    for _name, catalog_util in getUtilitiesFor(ICatalog):
        for attr in II18nFilePropertiesContainerAttributes(object).attributes:
            for value in getattr(object, attr, {}).values():
                if value is not None:
                    notify(ObjectRemovedEvent(value))
                    catalog.unindexObject(value, catalog_util)

    return


@adapter(II18nFilePropertiesContainer, IObjectCopiedEvent)
def handleCopiedI18nFilePropertiesContainer(object, event):
    object._v_copied_file = True
    source = event.original
    for attr in II18nFilePropertiesContainerAttributes(source).attributes:
        for key, value in getattr(source, attr, {}).items():
            if isinstance(value, BaseBlobFile):
                getattr(object, attr)[key]._blob = Blob()
                getattr(object, attr)[key].data = value.data