# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\browser\viewlets.py
# Compiled at: 2010-04-08 08:46:15
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.viewlets.common import TitleViewlet as TitleViewletBase
from plone.app.layout.navigation.root import getNavigationRootObject
from collective.phantasy.browser.viewlets import PhantasySearchBoxViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TitleViewlet(TitleViewletBase):
    __module__ = __name__

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        self.page_title = self.context_state.object_title
        root = getNavigationRootObject(self.context, self.portal_state.portal())
        self.portal_title = root.title_or_id


class CornersTopViewlet(ViewletBase):
    """
    return the corners top (rounded corners + png transparency)
    """
    __module__ = __name__

    def index(self):
        return '<div class="corners-wrapper" id="corners-top-wrapper">&nbsp;</div>'


class CornersBottomViewlet(ViewletBase):
    """
    return the corners bottom (rounded corners + png transparency)
    """
    __module__ = __name__

    def index(self):
        return '<div class="corners-wrapper" id="corners-bottom-wrapper">&nbsp;</div>'


class MiniSiteSearchBoxViewlet(PhantasySearchBoxViewlet):
    """
    overload the phantasy searchbox viewlet with another browser root
    """
    __module__ = __name__
    newindex = ViewPageTemplateFile('templates/minisite-searchbox.pt')

    def update(self):
        if self.displayViewlet():
            self.index = self.newindex
            ViewletBase.update(self)
            context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
            portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
            props = getToolByName(self.context, 'portal_properties')
            livesearch = props.site_properties.getProperty('enable_livesearch', False)
            if livesearch:
                self.search_input_id = 'searchGadget'
            else:
                self.search_input_id = ''
            root = getNavigationRootObject(self.context, portal_state.portal())
            self.root_path = ('/').join(root.getPhysicalPath())
        else:
            self.index = self.emptyindex