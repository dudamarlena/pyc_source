# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/c2/app/fbpage/browser/listing.py
# Compiled at: 2011-03-24 04:54:12
__doc__ = '\nlisting.py\n\nCreated by Manabu Terada on 2011-03-24.\nCopyright (c) 2011 CMScom. All rights reserved.\n'
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ListView(BrowserView):
    template = ViewPageTemplateFile('listing.pt')

    def __call__(self):
        return self.template()

    def get_items(self):
        limit = 10
        path = self.context.getPhysicalPath()
        catalog = getToolByName(self, 'portal_catalog')
        query = {}
        query['path'] = {'query': ('/').join(path), 'depth': 1}
        query['sort_on'] = 'Date'
        query['sort_order'] = 'reverse'
        query['limit'] = limit
        return catalog(query)[:limit]