# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/portlet/generichtml/generichtmlportlet.py
# Compiled at: 2009-05-19 09:23:41
from urllib import quote, quote_plus
from string import Template
from zope import schema
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from quintagroup.portlet.generichtml import GenericHTMLPortletMessageFactory as _
DEFAULT_CONTENT = 'Here can be your content'

class IGenericHTMLPortlet(IPortletDataProvider):
    __module__ = __name__
    content = schema.Text(title=_('Generic HTML Portlet content'), description=_('content_field_description', default="Enter your html code here. Please use '$categories', '$enc_categories' or '$encplus_categories' \nvariables to use categories from current context in your code.\nFor example: $categories will be substituted for 'some category1,some category2', \n$enc_categories will be substituted for 'some%20category1%2Csome%20category2', \n$encplus_categories will be substituted for 'some+category1%2Csome+category2',\nwhere some category1, some category2 are categories of your current content."), required=True)


class Assignment(base.Assignment):
    __module__ = __name__
    implements(IGenericHTMLPortlet)

    def __init__(self, content=DEFAULT_CONTENT):
        self.content = content

    @property
    def title(self):
        return _('Generic HTML Portlet')


class Renderer(base.Renderer):
    __module__ = __name__
    _template = ViewPageTemplateFile('generichtmlportlet.pt')

    def render(self):
        return xhtml_compress(self._template())

    def ptcontent(self):
        content = Template(self._data())
        return content.substitute(**self.context_categories())

    def context_categories(self):
        categories = self.context.Subject()
        return {'categories': (',').join(categories), 'enc_categories': quote((',').join(categories)), 'encplus_categories': quote_plus((',').join(categories))}

    @memoize
    def _data(self):
        return self.data.content


class AddForm(base.AddForm):
    __module__ = __name__
    form_fields = form.Fields(IGenericHTMLPortlet)
    label = _('Add Generic HTML Portlet')
    description = _('This portlet displays html content.')

    def create(self, data):
        return Assignment(content=data.get('content', DEFAULT_CONTENT))


class EditForm(base.EditForm):
    __module__ = __name__
    form_fields = form.Fields(IGenericHTMLPortlet)
    label = _('Edit Generic HTML Portlet')
    description = _('This portlet displays html content.')