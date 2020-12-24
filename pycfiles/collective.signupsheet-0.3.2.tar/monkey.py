# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/monkey.py
# Compiled at: 2011-07-29 07:55:08
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from plone.app.portlets.portlets.events import Renderer
from DateTime.DateTime import DateTime

def _data(self):
    context = aq_inner(self.context)
    catalog = getToolByName(context, 'portal_catalog')
    limit = self.data.count
    state = self.data.state
    path = self.navigation_root_path
    return catalog(portal_type=('Event', 'SignableEvent'), review_state=state, end={'query': DateTime(), 'range': 'min'}, path=path, sort_on='start', sort_limit=limit)[:limit]


Renderer._data = _data