# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/operun/linkportlet/events.py
# Compiled at: 2009-04-08 09:06:23
from zope.component import adapter, getMultiAdapter, getUtility
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent import ObjectCopiedEvent
from Products.Archetypes.interfaces import IEditBegunEvent, IObjectInitializedEvent
from Products.Archetypes.event import ObjectInitializedEvent
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from zope.app.container.interfaces import INameChooser
from interfaces import IOperunUnique
import re

@adapter(IOperunUnique, IObjectCreatedEvent)
def operunContentUniquenessPolice(operun_unique_obj, event):
    """To make sure that just one instance of the IOperunUnique exists
    we look in the catalog for other objects of that content type
    """
    plone_site = getSite()
    if isinstance(event, ObjectCopiedEvent):
        CopyError = 'Copy Error'
        try:
            catalog = getToolByName(plone_site, 'portal_catalog')
        except AttributeError:
            return
        else:
            results = catalog(portal_type=operun_unique_obj.portal_type)
            if len(results) > 0:
                raise CopyError
    else:
        assert operun_unique_obj == event.object
        catalog = getToolByName(plone_site, 'portal_catalog')
        results = catalog(portal_type=operun_unique_obj.portal_type)
        if len(results) > 0:
            instance = results[0].getObject()
            instance.REQUEST.RESPONSE.redirect(instance.absolute_url())