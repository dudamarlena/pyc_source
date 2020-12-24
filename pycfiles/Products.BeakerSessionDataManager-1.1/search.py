# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/browser/portlets/search.py
# Compiled at: 2011-01-11 16:22:56
from zope import schema
from zope.formlib import form
from zope.interface import implements
from Acquisition import aq_get, aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName

class ISearchPortlet(IPortletDataProvider):
    """  zentinel navigation portlet """
    __module__ = __name__
    base = schema.ASCIILine(title=_('Base URL'), description=_('The url of the Zentinel as dispatched via ZWindow.'), required=True, default='zentinel/show_window?url=/zport/dmd/deviceSearchResults')


class Renderer(base.Renderer):
    """ Overrides static.pt in the rendering of the portlet. """
    __module__ = __name__
    render = ViewPageTemplateFile('search.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return True

    def site_url(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()

    def base_url(self):
        """
        the search url as recognised by Zenoss
        """
        return self.data.base

    def zen_search_url(self):
        """
        the search url as recognised by Zenoss
        """
        return '/zport/dmd/deviceSearchResults?query='

    def search_url(self):
        """
        the search URL
        """
        return '%s/zentinel/show_window' % self.site_url()

    def query(self):
        """
        return the ip/query the user typed in
        """
        return self.request.has_key('form.button.Query') and request.get('query', '') or ''


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    __module__ = __name__
    implements(ISearchPortlet)
    title = _('Zenoss Device/IP Search')

    def __init__(self, base):
        self.base = base


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(ISearchPortlet)
    label = _('Add Zenoss Device Search Portlet')
    description = _('This portlet provides your Zenoss device/ip search.')

    def create(self, data):
        return Assignment(data.get('base', ''))


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(ISearchPortlet)
    label = _('Edit Zenoss Device Search Portlet')
    description = _('This portlet provides your Zenoss device/ip search.')