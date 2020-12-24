# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/z3c/pluggabletemplates/zcml.py
# Compiled at: 2006-11-01 08:19:33
__docformat__ = 'reStructuredText'
import os
from zope import interface
from zope import schema
from zope.component import zcml
from zope.configuration.exceptions import ConfigurationError
import zope.configuration.fields
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.pagetemplate.interfaces import IPageTemplate
from zope.configuration.fields import GlobalObject
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('zope')

class IPluggableTemplatesDirective(interface.Interface):
    """Parameters for the template directive."""
    __module__ = __name__
    for_ = GlobalObject(title=_('View'), description=_('The view for which the template should be used'), required=False, default=interface.Interface)
    layer = GlobalObject(title=_('Layer'), description=_('The layer for which the template should be used'), required=False, default=IDefaultBrowserLayer)


class IPluggableTemplate(interface.Interface):
    __module__ = __name__
    file = zope.configuration.fields.Path(title=_('Content-generating template.'), description=_('Refers to a file containing a page template (should end in extension ``.pt`` or ``.html``).'), required=False)
    name = schema.TextLine(title=_('Name'), description=_('\n                The name to be used.\n                Allows named adapter lookups so multiple templates can be assigned to one view.\n                '), required=False, default='')
    contentType = schema.BytesLine(title=_('Content Type'), description=_('The content type identifies the type of data.'), default='text/html', required=False)
    layer = GlobalObject(title=_('Layer'), description=_('The layer for which the template should be used'), required=False, default=IDefaultBrowserLayer)


class TemplateFactory(object):
    __module__ = __name__

    def __init__(self, filename, contentType):
        self.filename = filename
        self.contentType = contentType

    def __call__(self, view, request):
        template = ViewPageTemplateFile(self.filename, content_type=self.contentType)
        return template


def templateDirective(_context, file, name, for_=interface.Interface, layer=IDefaultBrowserLayer, contentType='text/html', **kwargs):
    file = os.path.abspath(str(_context.path(file)))
    if not os.path.isfile(file):
        raise ConfigurationError('No such file', file)
    factory = TemplateFactory(file, contentType)
    zcml.adapter(_context, (factory,), IPageTemplate, (for_, layer), name=name)


class PluggableTemplatesDirective(object):
    __module__ = __name__

    def __init__(self, _context, for_, layer=IDefaultBrowserLayer):
        self._context = _context
        self.for_ = for_
        self.layer = layer

    def template(self, _context, file, name, contentType='text/html', layer=None, *args, **kw):
        file = os.path.abspath(str(self._context.path(file)))
        if not layer:
            layer = self.layer
        return templateDirective(self._context, file, name, self.for_, layer, contentType)

    def __call__(self):
        pass