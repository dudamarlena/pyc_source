# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jack/workspace/zope/ploomcake/src/redomino.seosupport/redomino/seosupport/browser/viewlets.py
# Compiled at: 2012-04-24 08:53:08
from cgi import escape
from zope.component import getMultiAdapter
from Products.CMFPlone.utils import safe_unicode
from plone.app.layout.viewlets.common import TitleViewlet as BaseViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TitleViewlet(BaseViewlet):

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        page_title = escape(safe_unicode(context_state.object_title()))
        portal_title = escape(safe_unicode(portal_state.navigation_root_title()))
        if page_title == portal_title:
            self.site_title = portal_title
        else:
            self.site_title = '%s &mdash; %s' % (portal_title, page_title)