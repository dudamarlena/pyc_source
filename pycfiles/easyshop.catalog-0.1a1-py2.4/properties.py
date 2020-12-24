# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/ajax/properties.py
# Compiled at: 2008-09-01 03:09:55
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager
from Products.Five.browser import BrowserView

class PropertiesView(BrowserView):
    """
    """
    __module__ = __name__

    def selectProperties(self):
        """
        """
        renderer = getMultiAdapter((self.context, self.request, self), IViewletManager, name='easyshop.product-manager')
        renderer = renderer.__of__(self.context)
        renderer.update()
        return renderer.render()