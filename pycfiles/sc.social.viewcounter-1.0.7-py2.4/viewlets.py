# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-fat/egg/sc/social/viewcounter/browser/viewlets.py
# Compiled at: 2010-08-18 13:21:09
from Products.CMFPlone.utils import getToolByName
from plone.app.layout.viewlets import ViewletBase

class ViewCounterViewlet(ViewletBase):
    """A simple viewlet which renders an image used to track users
    """
    __module__ = __name__

    def render(self):
        marker = '<!-- viewcounter -->'
        if self.isEnabled():
            self.context.restrictedTraverse('@@vc_view')()
            return marker
        else:
            return ''

    def isEnabled(self):
        context = self.context
        aViews = [ name for (name, title) in context.getAvailableLayouts() ]
        if self._currentView() not in aViews:
            return
        try:
            portal_type = context.portal_type
        except AttributeError:
            return False

        self._pp = getToolByName(context, 'portal_properties', None)
        if hasattr(self._pp, 'sc_social_viewcounter'):
            blacklisted_types = list(self._pp.sc_social_viewcounter.getProperty('blacklisted_types') or []) + ['Discussion Item']
            valid_wf_states = list(self._pp.sc_social_viewcounter.getProperty('valid_wf_states') or [])
        else:
            blacklisted_types = []
            valid_wf_states = []
        wt = getToolByName(context, 'portal_workflow', None)
        wf_state = wt.getInfoFor(context, 'review_state', '')
        return portal_type not in blacklisted_types and wf_state in valid_wf_states

    def _currentView(self):
        request = self.request
        if 'PUBLISHED' in request.keys():
            cur_view = getattr(request['PUBLISHED'], '__name__', None) or getattr(request['PUBLISHED'].view, '__name__', None)
            return cur_view
        return