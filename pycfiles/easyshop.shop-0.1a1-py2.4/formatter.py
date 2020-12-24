# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/shop/migrations/formatter.py
# Compiled at: 2008-09-03 11:15:26
from zope.annotation.interfaces import IAnnotations
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
KEY = 'EASYSHOP_FORMAT'

class FormatterView(BrowserView):
    """
    """
    __module__ = __name__

    def addTitle(self):
        """Adds title to IFormatables
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(object_provides='easyshop.core.interfaces.catalog.IFormatable')
        for brain in brains:
            object = brain.getObject()
            annotations = IAnnotations(object)
            if annotations.has_key(KEY) == True:
                annotations[KEY]['title'] = 'title'
                annotations[KEY]['chars'] = '0'