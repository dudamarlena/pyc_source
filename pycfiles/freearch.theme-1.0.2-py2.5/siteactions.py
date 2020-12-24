# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/freearch/theme/browser/siteactions.py
# Compiled at: 2008-06-19 07:06:52
from zope.interface import implements, alsoProvides
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from plone.app.layout.globals.interfaces import IViewView
from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from cgi import escape
from urllib import quote_plus
from plone.app.layout.viewlets.common import ViewletBase

class SiteActionsViewlet(ViewletBase):
    """SiteActions and SeachBox all together.
    
    Overridden to use our custom template.
    """
    render = ViewPageTemplateFile('templates/site_actions.pt')

    def __init__(self, context, request, *args, **kw):
        ViewletBase.__init__(self, context, request, *args, **kw)
        utool = getToolByName(context, 'portal_url')
        self.url = utool()

    def update(self):
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        self.site_actions = context_state.actions().get('site_actions', None)
        return