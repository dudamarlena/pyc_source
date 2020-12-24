# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/z3c/resourcecollector/zcml.py
# Compiled at: 2008-07-29 15:59:13
import zope.interface, zope.configuration.fields, zope.component, zope.schema
from zope.app import zapi
from zope.app.publisher.browser import metaconfigure
from interfaces import ICollectorUtility
from browser import CollectorResource
from utility import CollectorUtility

class ICollectorDirective(zope.interface.Interface):
    name = zope.schema.TextLine(title='The name of the resource library', description='        This is the name used to disambiguate resource libraries.  No two\n        libraries can be active with the same name.', required=True)
    type = zope.configuration.fields.GlobalInterface(title='Request type', required=True)
    content_type = zope.schema.TextLine(title='Content type', required=False)


def handleCollector(_context, name, type, content_type=None):
    zapi.getGlobalSiteManager().registerUtility(CollectorUtility(content_type), name=name)
    class_ = CollectorResource
    for_ = (zope.interface.Interface,)
    provides = zope.interface.Interface
    metaconfigure.resource(_context, name, layer=type, factory=class_)


class ICollectorItemDirective(zope.interface.Interface):
    collector = zope.schema.TextLine(title='The name of the resource library', description='        The name of the resourcelibrary where we want to add our resources', required=True)
    item = zope.schema.TextLine(title='The resource to add to the resource library', description='        The resource', required=True)
    weight = zope.schema.Int(title='The position of the resource in the library', description='        The position of the resource in the library', required=True)


def handleCollectorItem(_context, collector, item, weight):
    _context.action(discriminator=(
     collector, item), callable=addCollectorItem, args=(
     collector, item, weight))


def addCollectorItem(collector, item, weight):
    rs = zope.component.getUtility(ICollectorUtility, collector)
    resource = {}
    resource['weight'] = weight
    resource['resource'] = item
    rs.resources[item] = resource