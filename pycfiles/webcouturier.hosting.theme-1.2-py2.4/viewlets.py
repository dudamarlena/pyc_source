# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/webcouturier/hosting/theme/browser/viewlets.py
# Compiled at: 2008-07-25 04:13:55
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class TopNavigationViewlet(common.ViewletBase):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/webcouturier_topnavigation.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        self.top_navigation = self.context_state.actions().get('top_navigation', None)
        self.width = str(768 / len(self.top_navigation)) + 'px'
        return


class WebcouturierPersonalBarViewlet(common.PersonalBarViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/personal_bar.pt')


class WebcouturierSearchBoxViewlet(common.SearchBoxViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/searchbox.pt')


class WebcouturierGlobalSectionsViewlet(common.GlobalSectionsViewlet):
    __module__ = __name__
    render = ViewPageTemplateFile('templates/sections.pt')