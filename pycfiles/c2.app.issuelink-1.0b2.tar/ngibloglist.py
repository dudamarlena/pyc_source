# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/c2/app/fbpage/browser/ngibloglist.py
# Compiled at: 2011-03-24 05:50:45
__doc__ = '\nngibloglist.py\n\nCreated by Manabu Terada on 2011-03-24.\nCopyright (c) 2011 CMScom. All rights reserved.\n'
from DateTime import DateTime
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.ZCatalog.Catalog import CatalogError

class NgiBlogListView(BrowserView):
    template = ViewPageTemplateFile('ngibloglist.pt')

    def __call__(self):
        return self.template()

    def get_items(self):
        limit = 10
        path = self.context.getPhysicalPath()
        catalog = getToolByName(self, 'portal_catalog')
        query = {}
        query['portal_type'] = 'Entry'
        query['path'] = {'query': ('/').join(path), 'depth': 1}
        query['sort_on'] = 'pub_date'
        query['sort_order'] = 'reverse'
        query['limit'] = limit
        try:
            return catalog(query)[:limit]
        except CatalogError:
            query['sort_on'] = 'Date'
            return catalog(query)[:limit]

    def trans_pub_date(self, pub_date):
        if not isinstance(pub_date, DateTime):
            pub_date = DateTime(pub_date)
        return pub_date.strftime('%Y-%m-%d')