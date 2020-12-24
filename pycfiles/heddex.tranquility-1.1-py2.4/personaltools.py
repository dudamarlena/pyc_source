# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/heddex/tranquility/portlets/personaltools.py
# Compiled at: 2009-06-04 17:33:35
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from urllib import quote_plus
from AccessControl import getSecurityManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class IPersonaltoolsPortlet(IPortletDataProvider):
    """A portlet which renders a personal tools for logged in users.
    """
    __module__ = __name__


class Assignment(base.Assignment):
    __module__ = __name__
    implements(IPersonaltoolsPortlet)
    title = _('heading_personal_tools', default='Personal tools')


class Renderer(base.Renderer):
    __module__ = __name__

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request), name='plone_context_state')
        self.tools = getMultiAdapter((self.context, self.request), name='plone_tools')
        self.sm = getSecurityManager()
        self.portal_url = self.portal_state.portal_url()
        self.user_actions = self.context_state.actions().get('user', None)
        self.anonymous = self.portal_state.anonymous()
        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor
        return

    @property
    def available(self):
        return not self.anonymous

    def homelink_url(self):
        member = self.portal_state.member()
        userid = member.getId()
        if self.sm.checkPermission('Portlets: Manage own portlets', self.context):
            self.homelink_url = self.portal_url + '/dashboard'
        else:
            self.homelink_url = self.portal_url + '/author/' + quote_plus(userid)
        return self.homelink_url

    def user_name(self):
        member = self.portal_state.member()
        userid = member.getId()
        member_info = self.tools.membership().getMemberInfo(member.getId())
        fullname = member_info.get('fullname', '')
        if fullname:
            self.user_name = fullname
        else:
            self.user_name = userid
        return self.user_name

    def update(self):
        pass

    render = ViewPageTemplateFile('personaltools.pt')


class AddForm(base.NullAddForm):
    __module__ = __name__

    def create(self):
        return Assignment()