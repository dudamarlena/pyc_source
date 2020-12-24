# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/espen/Plone4b3/zinstance/src/medialog.portlet.sitemap/medialog/portlet/sitemap/sitemapportlet.py
# Compiled at: 2010-05-20 18:09:14
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from medialog.portlet.sitemap import SitemapPortletMessageFactory as _

class ISitemapPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    sitemaptitle = schema.TextLine(title=_('Title'), description=_('The title of the sitemap portlet'), required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(ISitemapPortlet)
    sitemaptitle = ''

    def __init__(self, sitemaptitle=None):
        self.sitemaptitle = sitemaptitle

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'Sitemap Portlet'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    render = ViewPageTemplateFile('sitemapportlet.pt')


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ISitemapPortlet)

    def create(self, data):
        return Assignment(**data)


class AddForm(base.AddForm):
    form_fields = form.Fields(ISitemapPortlet)
    label = _('Add the Sitemap Portlet')
    description = _('This portlet whows the sitemap in a portlet (suprise). You should also install jquery / jquery ui.')

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ISitemapPortlet)