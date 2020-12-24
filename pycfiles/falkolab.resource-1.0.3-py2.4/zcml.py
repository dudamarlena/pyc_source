# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/zcml.py
# Compiled at: 2009-03-16 09:58:28
"""
$Id: zcml.py 207 2009-03-16 13:58:27Z falko $
"""
from falkolab.resource.util import _findResourceType
from warnings import warn
from zope.component import queryUtility
from zope.component.interfaces import ComponentLookupError
from zope import schema, interface, component
from zope.configuration import fields
from zope.component.zcml import handler
from zope.interface.verify import verifyObject
from zope.app.publisher.browser.metadirectives import IBasicResourceInformation
from zope.app.publisher.browser.resourcemeta import allowed_names
from zope.publisher.interfaces.browser import IDefaultBrowserLayer, IBrowserRequest
from zope.security.checker import CheckerPublic, NamesChecker
from falkolab.resource.interfaces import IResourceType, IResourceFactory, IResourcePropertyManager, IExtensibleResourceFactory
from falkolab.resource.resourcetypes import ResourceType

class IResourceDirective(IBasicResourceInformation):
    """ falkolab:resource directive """
    __module__ = __name__
    name = schema.TextLine(title='The name of the resource', description='\n        This is the name used in resource urls. Resource urls are of\n        the form site/@@/resourcename, where site is the url of\n        "site", a folder with a site manager.\n\n        We make resource urls site-relative (as opposed to\n        content-relative) so as not to defeat caches.\n        Can\'t be two resources with same name.', required=True)
    type = schema.TextLine(title='Resource type', required=False)
    src = fields.Path(title='Resource source', description='Resource source specific for resource type (for example file path for file resource)', required=True)


class IResourcePropertyDirective(interface.Interface):
    __module__ = __name__
    name = schema.TextLine(title='Resource option name', required=True)
    value = schema.TextLine(title='Resource option value', required=True)


class IResourceTypeDirective(interface.Interface):
    """ Resource type factory """
    __module__ = __name__
    name = schema.TextLine(title='Resource type name', description='Used for type field of resource directive', required=True)
    description = schema.TextLine(title='Resource type description', description='Used for describe type of resource directive', required=False)
    mask = fields.Tokens(title='Specifications this names are the reserved for', description='List of strings is the file name extension or file name that the handler processes (e.g: *_res.pt *.jpg my[0-9].resource)', value_type=schema.TextLine(), required=False, unique=True)
    factory = fields.GlobalObject(title='Resource Type Factory', description='Custom resource type factory', required=True)


def _setProperty(resourceFactory, name, value):
    resmgr = component.queryAdapter(resourceFactory, IResourcePropertyManager, name, default=None)
    if not resmgr:
        resmgr = IResourcePropertyManager(resourceFactory)
    if resmgr:
        resmgr.setProperty(name, value)
    else:
        warn("Can't find IResourcePropertyManager adapter for resource '%s' to set property '%s'.%s %s" % (self.name, name, str(self.resourceFactory), str(resmgr)))
    return


class ResourceDirective(object):
    __module__ = __name__

    def __init__(self, _context, name, src, layer=IDefaultBrowserLayer, permission='zope.Public', type=''):
        if permission == 'zope.Public':
            permission = CheckerPublic
        checker = NamesChecker(allowed_names, permission)
        resourceType = None
        self.name = name
        self.layer = layer
        if type:
            resourceType = queryUtility(IResourceType, name=type)
        else:
            resourceType = _findResourceType(src, default='file')
        if resourceType == None:
            raise ComponentLookupError("Can't find resource type for resource '%s' from source '%s'" % (name, src))
        resourceFactory = resourceType(src, checker, name)
        resourceFactory.typeName = resourceType.getName()
        if not verifyObject(IResourceFactory, resourceFactory):
            raise TypeError('Resource factory must provide IResourceFactory interface')
        _context.action(discriminator=('resource', name, IBrowserRequest, layer), callable=handler, args=('registerAdapter', resourceFactory, (layer,), interface.Interface, name, _context.info))
        self.resourceFactory = resourceFactory
        return

    def property(self, _context, name, value):
        if IExtensibleResourceFactory.providedBy(self.resourceFactory):
            _context.action(discriminator=('resource.property', self.name, name, IBrowserRequest, self.layer), callable=_setProperty, args=(self.resourceFactory, name, value))
        else:
            warn("Resource factory for resource '%s' must implement IExtensibleResourceFactory" % self.name)


def resourceTypeDirective(_context, name, factory, description='', mask=None):
    if not IResourceFactory.implementedBy(factory):
        raise TypeError('Must implement IResourceFactory')
    resourceType = ResourceType(factory, name, mask)
    handler('registerUtility', resourceType, IResourceType, name)