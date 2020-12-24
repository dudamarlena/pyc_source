# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plonetheme/mimbo/browser/viewlets.py
# Compiled at: 2009-12-03 13:27:27
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName

class PersonalBarViewlet(ViewletBase):
    render = ViewPageTemplateFile('personal_bar.pt')

    def update(self):
        super(PersonalBarViewlet, self).update()
        context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name='plone_tools')
        sm = getSecurityManager()
        self.user_actions = context_state.actions().get('user', None)
        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor
        self.anonymous = self.portal_state.anonymous()
        if not self.anonymous:
            member = self.portal_state.member()
            userid = member.getId()
            if sm.checkPermission('Portlets: Manage own portlets', self.context):
                self.homelink_url = self.site_url + '/dashboard'
            elif userid.startswith('http:') or userid.startswith('https:'):
                self.homelink_url = self.site_url + '/author/?author=' + userid
            else:
                self.homelink_url = self.site_url + '/author/' + quote_plus(userid)
            member_info = tools.membership().getMemberInfo(member.getId())
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
                self.user_name = userid
        return


class FooterViewlet(ViewletBase):
    render = ViewPageTemplateFile('footer.pt')