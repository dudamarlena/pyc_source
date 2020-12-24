# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/republisher/events.py
# Compiled at: 2010-10-11 11:47:26
from Products.CMFCore.utils import getToolByName
from republisher import Republisher
from plone.registry.interfaces import IRegistry
from Products.republisher.interfaces import IRepublisherTokenKeeper, IRepublisherSettings
from zope.component import queryUtility

def uploadEventHandler(ob, event):
    """Event that fires when an Item changes state"""
    print 'uploadEventHandler called for: ' + ob.id
    republisher = Republisher()
    plone_utils = getToolByName(ob, 'plone_utils')
    registry = queryUtility(IRegistry)
    tokenkeeper = registry.forInterface(IRepublisherTokenKeeper)
    settings = registry.forInterface(IRepublisherSettings)
    republisherOn = settings.republisher_toggle
    if event.action == 'publish' and ob.id != 'cmf_uid' and (ob.portal_type in republisher.allowed_types or plone_utils.isStructuralFolder(ob)) and republisherOn:
        itemsAffected = []
        if plone_utils.isStructuralFolder(ob):
            catalog = getToolByName(ob, 'portal_catalog')
            folder_url = ('/').join(ob.getPhysicalPath())
            results = catalog.searchResults(path={'query': folder_url, 'depth': 5}, sort_on='getObjPositionInParent', portal_type=republisher.getAllowedTypes())
            for item in results:
                itemsAffected.append(item)

        else:
            itemsAffected.append(ob)
        print 'Uploading images......'
        for item in itemsAffected:
            republisher.uploadImageToFlickr(item)

        print 'image upload finished'


def statelessUploadEventHandler(ob, event):
    """Event that fires when an Item changes state"""
    print 'statelessUploadEventHandler called'
    portal_workflow = getToolByName(ob, 'portal_workflow')
    if portal_workflow.getChainForPortalType(ob.portal_type) == ():
        republisher = Republisher()
        print 'Uploading image......'
        republisher.uploadImageToFlickr(ob)
        print 'image upload finished'