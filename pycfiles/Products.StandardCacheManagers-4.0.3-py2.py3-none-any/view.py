# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/SquareListing/view.py
# Compiled at: 2010-01-12 05:55:22
from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName
from Products.ATContentTypes.interface.topic import IATTopic

class SquareListing(BrowserView):
    """ """
    __module__ = __name__

    def hasLeadImageField(self, obj=None):
        """
        """
        if not obj:
            return False
        ptool = getToolByName(self.context, 'portal_properties')
        try:
            props = ptool.cli_properties
            allowed_types = props.allowed_types
            if obj.Type() in allowed_types:
                return True
            return False
        except:
            return False

    def isGallery(self, obj):
        """docstring for isGallery"""
        try:
            from Products.galleriffic.interfaces import IGallerifficView
            return IGallerifficView.providedBy(obj) and obj.getLayout() == 'galleriffic_view'
        except:
            return False

    def getImageExample(self, obj):
        """ """
        if IATTopic.providedBy(obj):
            images = obj.queryCatalog()
        else:
            ct_tool = getToolByName(self.context, 'portal_catalog')
            images = ct_tool(Type='Image', path=('/').join(obj.getPhysicalPath()))
        if len(images) > 0:
            return images[0].getURL()
        return