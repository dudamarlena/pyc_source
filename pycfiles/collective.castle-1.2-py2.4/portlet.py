# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/castle/portlet.py
# Compiled at: 2010-08-09 05:35:03
from zope.interface import Interface, implements
from zope.formlib import form
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.castle import util
from Products.CMFCore.utils import getToolByName

class IPortlet(Interface):
    __module__ = __name__


class Assignment(base.Assignment):
    __module__ = __name__
    implements(IPortlet)
    title = 'CAS Log in'


class Renderer(base.Renderer):
    __module__ = __name__
    render = ViewPageTemplateFile('login_portlet.pt')

    @property
    def submit_url(self):
        if self.is_logged_in():
            return 'castle_logout'
        else:
            return util.login_URL(self.context)

    @property
    def submit_name(self):
        if self.is_logged_in():
            return 'CAS Log out'
        else:
            return 'CAS Log in'

    def is_logged_in(self):
        mt = getToolByName(self.context, 'portal_membership')
        return not mt.isAnonymousUser()


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(IPortlet)

    def create(self, data):
        return Assignment()