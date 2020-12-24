# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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