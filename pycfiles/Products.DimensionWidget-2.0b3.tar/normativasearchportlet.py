# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/portlets/normativasearchportlet.py
# Compiled at: 2009-04-26 22:17:24
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Acquisition import aq_inner
from Products.DigestoContentTypes import DigestoContentTypesMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class INormativaSearchPortlet(IPortletDataProvider):
    """ A portlet displaying a (live) search box
    """
    __module__ = __name__
    enableLivesearch = schema.Bool(title=_('Enable LiveSearch'), description=_('Enables the LiveSearch feature, which shows live results if the browser supports JavaScript.'), default=True, required=False)


class Assignment(base.Assignment):
    __module__ = __name__
    implements(INormativaSearchPortlet)

    def __init__(self, enableLivesearch=True):
        self.enableLivesearch = True

    @property
    def title(self):
        return _('Search')


class Renderer(base.Renderer):
    __module__ = __name__
    render = ViewPageTemplateFile('normativasearchportlet.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        portal_state = getMultiAdapter((context, request), name='plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.typestools = getMultiAdapter((context, request), name='typestools')

    def enable_livesearch(self):
        return self.data.enableLivesearch

    def search_form(self):
        return '%s/normativa_search_form' % self.portal_url

    def search_action(self):
        return '%s/normativa_search' % self.portal_url

    def years(self):
        return self.typestools.get_years()

    def areas(self):
        return self.typestools.get_areas()


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(INormativaSearchPortlet)
    label = _('Add Search Portlet')
    description = _('This portlet shows a search box.')

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(INormativaSearchPortlet)
    label = _('Edit Search Portlet')
    description = _('This portlet shows a search box.')