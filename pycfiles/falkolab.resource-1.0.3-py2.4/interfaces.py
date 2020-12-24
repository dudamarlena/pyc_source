# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/interfaces.py
# Compiled at: 2009-03-11 04:29:09
"""
$Id: interfaces.py 200 2009-03-11 08:29:13Z falko $
"""
from zope import interface, schema

class IResourceFactory(interface.Interface):
    __module__ = __name__

    def __init__(path, checker, name):
        pass

    def __call__(request):
        """Create resource"""
        pass


class IExtensibleResourceFactory(IResourceFactory):
    __module__ = __name__
    properties = schema.Dict(title='Resource properties', description='Resource specific properties dictionary', key_type=schema.TextLine(), value_type=schema.TextLine(), default={})


class IResourceContainerFactory(IExtensibleResourceFactory):
    __module__ = __name__
    types = schema.List(title='Types', description='List of allowed types for contained resources', required=False, unique=True, value_type=schema.Choice(vocabulary='falkolab.resource.AvailableResourceTypes'), default=[])


class IResource(interface.Interface):
    __module__ = __name__

    def renderHtmlEmbeding(request, **kwargs):
        pass


class IResourceType(interface.Interface):
    __module__ = __name__

    def __init__(factory, name, mask=None):
        pass

    def __call__(path, checker, name):
        """ create resource factory """
        pass

    def matchName(name):
        pass

    def getName():
        pass

    def getMasks():
        pass


class IAvailableResourceTypes(interface.Interface):
    __module__ = __name__
    resourceTypes = schema.Iterable(title='Registered resource types', description='A list of registered resource types')


class IResourcePropertyManager(interface.Interface):
    """Set up property value from zcml property subdirective"""
    __module__ = __name__

    def setProperty(name, stringValue):
        """Set raw string property value"""
        pass