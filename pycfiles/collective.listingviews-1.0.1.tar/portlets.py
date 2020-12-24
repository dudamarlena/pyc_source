# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/browser/portlets.py
# Compiled at: 2009-11-27 05:18:01
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlet.static import static
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.linkedin.browser.company_info import CompanyInfo
from collective.linkedin.browser.profile_info import ProfileInfo
from collective.linkedin.browser.interfaces import ICompanyInfoPortlet, IProfileInfoPortlet
from collective.linkedin import LinkedInMessageFactory as _

class CompanyInfoRenderer(static.Renderer, CompanyInfo):
    """ Overrides static.pt in the rendering of the portlet. """
    __module__ = __name__
    render = ViewPageTemplateFile('templates/company_info.pt')


class CompanyInfoAssignment(static.Assignment):
    """ Assigner for company info portlet. """
    __module__ = __name__
    implements(ICompanyInfoPortlet)

    @property
    def title(self):
        return _('Company Info portlet')


class CompanyInfoAddForm(base.NullAddForm):
    """ Make sure that add form creates instances of our custom portlet instead
    of the base class portlet. """
    __module__ = __name__

    def create(self):
        return CompanyInfoAssignment()


class CompanyInfoEditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields()
    label = _('Edit Company Info')
    description = _('This portlet displays Company Info.')


class ProfileInfoRenderer(base.Renderer, ProfileInfo):
    """ Overrides static.pt in the rendering of the portlet. """
    __module__ = __name__
    render = ViewPageTemplateFile('templates/profile_info.pt')


class ProfileInfoAssignment(base.Assignment):
    """ Assigner for profile info portlet. """
    __module__ = __name__
    implements(IProfileInfoPortlet)
    profile_id = ''
    name = ''

    def __init__(self, name='', profile_id=''):
        self.name = name
        self.profile_id = profile_id

    @property
    def title(self):
        return _('Profile Info portlet')


class ProfileInfoAddForm(base.AddForm):
    """ Make sure that add form creates instances of our custom
    portlet instead of the base class portlet. """
    __module__ = __name__
    form_fields = form.Fields(IProfileInfoPortlet)
    label = _('Add LinkedIn Profile Portlet')
    description = _('This portlet display a LinkedIn profile.')

    def create(self, data):
        return ProfileInfoAssignment(name=data.get('name', ''), profile_id=data.get('profile_id', ''))


class ProfileInfoEditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(IProfileInfoPortlet)
    label = _('Edit Profile Info')
    description = _('This portlet displays Profile Info.')