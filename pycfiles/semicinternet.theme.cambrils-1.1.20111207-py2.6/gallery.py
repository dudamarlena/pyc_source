# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/browser/gallery.py
# Compiled at: 2011-09-15 07:57:22
from zope import schema
from plone.app.portlets.portlets import base
from zope.formlib import form
from zope.interface import implements
from semicinternet.theme.cambrils.browser.interfaces import IGalleryPortlet
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from semicinternet.theme.cambrils import cambrilsMessageFactory as _

class Assignment(base.Assignment):
    implements(IGalleryPortlet)

    def __init__(self, image_count=5, image_root_folder='', path_depth=0):
        self.image_count = image_count
        self.image_root_folder = image_root_folder
        self.path_depth = path_depth

    @property
    def title(self):
        return _('Gallery portlet for Cambrils Theme')


class AddForm(base.AddForm):
    form_fields = form.Fields(IGalleryPortlet)
    label = _('Add Gallery Portlet')
    description = _('This portlet displays an inline image gallery.')

    def create(self, data):
        return Assignment(image_count=data.get('image_count', 5), image_root_folder=data.get('image_root_folder', ''), path_depth=data.get('path_depth', 0))


class EditForm(base.EditForm):
    form_fields = form.Fields(IGalleryPortlet)
    label = _('Edit Gallery Portlet')
    description = _('This portlet displays an inline image gallery.')


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('templates/gallery.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name='plone_portal_state')
        self.anonymous = portal_state.anonymous()
        self.portal_url = portal_state.portal_url()
        self.typesToShow = portal_state.friendly_types()
        plone_tools = getMultiAdapter((context, self.request), name='plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()

    def gallery_items(self):
        return self._data()

    def recently_modified_link(self):
        return '%s/recently_modified' % self.portal_url

    @memoize
    def _data(self):
        limit = self.data.image_count
        folder = self.data.image_root_folder
        depth = self.data.path_depth
        urltool = getToolByName(self.context, 'portal_url')
        catalog = getToolByName(self.context, 'portal_catalog')
        section_path = urltool.getPortalPath() + folder
        return self.catalog({'Type': {'query': ['Image', 'ATImage']}, 'path': {'query': section_path, 'level': 0, 'depth': depth}})[:limit]