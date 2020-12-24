# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/c2/app/fbpage/browser/listing.py
# Compiled at: 2011-03-24 04:54:12
"""
listing.py

Created by Manabu Terada on 2011-03-24.
Copyright (c) 2011 CMScom. All rights reserved.
"""
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