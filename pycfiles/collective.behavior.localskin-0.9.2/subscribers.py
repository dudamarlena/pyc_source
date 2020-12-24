# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.localregistry/src/collective/behavior/localregistry/subscribers.py
# Compiled at: 2014-03-12 09:41:21
from collective.behavior.localregistry.events import LocalRegistryCreatedEvent
from collective.behavior.localregistry.proxy import LocalRegistry
from collective.behavior.localregistry.proxy import REGISTRY_NAME
from five.localsitemanager import make_objectmanager_site
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getSiteManager
from zope.component.interfaces import ISite
from zope.container.interfaces import IObjectAddedEvent
from zope.container.interfaces import IObjectRemovedEvent
import zope.event

def enableChildRegistry(context, event):
    """
    """
    if not ISite.providedBy(context):
        make_objectmanager_site(context)
    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexObject(context, idxs=[
     'object_provides'])
    sm = getSiteManager(context=context)
    if REGISTRY_NAME not in context.objectIds():
        context[REGISTRY_NAME] = LocalRegistry(REGISTRY_NAME).__of__(context)
    sm.registerUtility(component=context[REGISTRY_NAME], provided=IRegistry)
    zope.event.notify(LocalRegistryCreatedEvent(context))


def reconfigureChildRegistry(context, event):
    """ Upon moving or renaming an object, the registry must be reconfigured.

    Under the hood, this will re-register compoents with the correct paths
    to prevent errors.
    """
    if not IObjectRemovedEvent.providedBy(event) and not IObjectAddedEvent.providedBy(event):
        enableChildRegistry(context, event)