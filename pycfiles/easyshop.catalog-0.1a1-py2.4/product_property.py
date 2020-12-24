# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/content/product_property.py
# Compiled at: 2008-09-03 11:14:29
from zope.interface import implements
from Products.Archetypes.atapi import *
from easyshop.core.config import PROJECTNAME
from easyshop.core.interfaces import IProperty

class ProductProperty(OrderedBaseFolder):
    """Product properties hold selectable options.
    """
    __module__ = __name__
    implements(IProperty)

    def getOptions(self):
        """
        """
        result = []
        for option in self.objectValues():
            if len(option.getImage()) > 0:
                image_url = option.absolute_url() + '/image_listing'
            else:
                image_url = None
            result.append({'id': option.getId(), 'name': option.Title(), 'url': option.absolute_url(), 'path': ('/').join(option.getPhysicalPath()), 'image_url': image_url, 'price': str(option.getPrice())})

        return result

    def base_view(self):
        """Overwritten to redirect to manage-properties-view of parent product 
        or group.
        """
        parent = self.aq_inner.aq_parent
        url = parent.absolute_url() + '/' + 'manage-properties-view'
        self.REQUEST.RESPONSE.redirect(url)


registerType(ProductProperty, PROJECTNAME)