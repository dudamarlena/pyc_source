# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stxnext/flashgallery/browser/simpleviewer_config.py
# Compiled at: 2008-07-17 02:22:12
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

class SimpleViewerConfig(BrowserView):
    """
    Base view class for simpleviewer and autoviewer XML configure data. 
    """
    __module__ = __name__

    def getImagesInFolder(self):
        """
        Return list of images.
        """
        pc = getToolByName(self.context, 'portal_catalog')
        return pc(object_provides='Products.ATContentTypes.interface.image.IATImage', path={'query': ('/').join(self.context.getPhysicalPath()), 'depth': 1}, sort_on='getObjPositionInParent')

    def getImageCaption(self, image):
        """
        Return caption of given image.
        """
        result = []
        if image.Title:
            result.append('<B>%s</B><BR />' % image.Title)
        if image.Description:
            result.append(image.Description.replace('\r', ''))
            result.append('<BR />')
        result.append('<A href="%s" target="_blank"><U>Original size</U></A>' % image.getURL())
        return ('<BR />').join(result)