# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/browser/product_zoom_view.py
# Compiled at: 2008-09-03 11:14:28
from Products.Five.browser import BrowserView
from easyshop.core.interfaces import IImageManagement

class ProductZoomView(BrowserView):
    """
    """
    __module__ = __name__

    def getCurrentImage(self):
        """
        """
        ord = self.request.get('ord', 0)
        try:
            ord = int(ord)
        except ValueError:
            ord = 0

        try:
            return self.getImageUrls()[ord]
        except IndexError:
            return self.getImageUrls()[0]

    def getImageUrls(self):
        """
        """
        pm = IImageManagement(self.context)
        result = []
        for image in pm.getImages():
            result.append({'small': '%s/image_thumb' % image.absolute_url(), 'large': '%s/image_large' % image.absolute_url()})

        return result