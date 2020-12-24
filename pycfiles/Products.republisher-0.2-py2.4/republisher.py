# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/republisher/republisher.py
# Compiled at: 2010-10-11 11:49:05
import string
from uploadr import Uploadr
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_base
from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from plone.registry.interfaces import IRegistry
from Products.republisher.interfaces import IRepublisherTokenKeeper, IRepublisherSettings
from zope.component import getUtility
from zope.component import queryUtility
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
    from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
    from collective.contentleadimage.interfaces import ILeadImageable
    LEADIMAGE_EXISTS = True
except ImportException:
    LEADIMAGE_EXISTS = False

class Republisher:
    __module__ = __name__
    flickr = None
    allowed_types = ('Image', 'Document', 'Event', 'Work', 'Person', 'Organization')

    def getAllowedTypes(self):
        return self.allowed_types

    def uploadImageToFlickr(self, item):
        registry = queryUtility(IRegistry)
        tokenkeeper = registry.forInterface(IRepublisherTokenKeeper)
        settings = registry.forInterface(IRepublisherSettings)
        self.flickr = Uploadr(frob=str(tokenkeeper.flickr_frob), token=str(tokenkeeper.flickr_token))
        self.flickr.setAPIKeyAndSecret(settings.api_key, settings.api_secret)
        print 'Republisher upload started for: ' + item.id
        filename = 'None.jpg'
        data = ''
        if item.portal_type in self.allowed_types:
            if hasattr(item, 'getObject'):
                itemObj = item.getObject()
            else:
                itemObj = item
            ann = IAnnotations(itemObj)
            if self.isPublic(itemObj):
                if ann.get('republisher_flickr', None) == None:
                    if item.portal_type == 'Image':
                        filename = itemObj.id
                        data = itemObj.get_data()
                    else:
                        filename = itemObj.id + '.jpg'
                        if LEADIMAGE_EXISTS and ILeadImageable.providedBy(itemObj):
                            field = aq_inner(itemObj).getField(IMAGE_FIELD_NAME)
                            if field is not None:
                                lead = field.get(itemObj)
                                data = lead.data
                                if type(data).__name__ == 'ImplicitAcquirerWrapper':
                                    data = str(aq_base(data))
                            else:
                                print 'Republisher upload failed: No LeadImage on item'
                                return
                        else:
                            print 'Republisher upload failed: LeadImage not present or not provided by item type'
                            return
                else:
                    return
                if hasattr(itemObj, 'Title'):
                    self.flickr.setTitle(itemObj.Title())
                else:
                    self.flickr.setTitle(itemObj.title)
                self.flickr.setDescription(itemObj.Description() + ' -- ' + itemObj.absolute_url() + '/view')
                self.flickr.setTag(string.join(itemObj.Subject(), ' '))
                print 'Republisher starting to upload data now... for item: ' + itemObj.id
                try:
                    newFlickrId = self.flickr.uploadImageFromData(data, filename)
                    if newFlickrId != 0:
                        ann['republisher_flickr'] = newFlickrId
                except:
                    print 'Could not upload file: '
                    traceback.print_exc()

            else:
                print 'Republisher did not upload: item is not public.'
        else:
            print 'Republisher did not upload: item is not allowed.'
        return

    def isPublic(self, item):
        """Check if an item is public (Visible to Anonymous user)"""
        if item.portal_type != 'Image' and item.portal_type != 'File':
            for p in item.rolesOfPermission('View'):
                if p['name'] == 'Anonymous' and p['selected'] != 'SELECTED':
                    print 'Not public because of item: ' + item.id
                    return False

        if type(aq_base(item.getParentNode())).__name__ == 'PloneSite':
            for p in item.rolesOfPermission('View'):
                if p['name'] == 'Anonymous' and p['selected'] == 'SELECTED':
                    return True

            print 'Not public because of item: ' + item.id
            return False
        else:
            return self.isPublic(item.getParentNode())