# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stxnext/flashgallery/browser/simpleviewer_view.py
# Compiled at: 2008-07-17 02:22:12
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

class SimpleViewerView(BrowserView):
    """
    SimpleViewer view class.
    """
    __module__ = __name__

    def getThumb(self):
        """
        Return thumb.
        """
        image_id = self.request.get('id', '')
        size = self.request.get('size', '')
        try:
            return self.context.restrictedTraverse('%s/image_%s' % (image_id, size)).data
        except:
            return