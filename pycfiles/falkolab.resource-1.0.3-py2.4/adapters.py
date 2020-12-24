# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/adapters.py
# Compiled at: 2009-03-16 09:58:28
from warnings import warn
from zope import interface, component
from falkolab.resource.interfaces import IResourcePropertyManager, IResourceContainerFactory, IExtensibleResourceFactory, IResourceType
from zope.configuration.exceptions import ConfigurationError

class DefaultResourceTypePropertyAdapter(object):
    __module__ = __name__
    interface.implements(IResourcePropertyManager)
    component.adapts(IExtensibleResourceFactory)

    def __init__(self, context):
        if context == None:
            raise ValueError("Can't be None")
        self.context = context
        return

    def setProperty(self, name, stringValue):
        if not name:
            raise ValueError("Property name can't be empty or None")
        if not stringValue:
            raise ValueError("Property value can't be empty or None")
        resourceFactory = self.context
        if resourceFactory.properties == None:
            resourceFactory.properties = {}
        resourceFactory.properties[name] = stringValue
        return


class ResourceTypePropertyAdapter(object):
    __module__ = __name__
    interface.implements(IResourcePropertyManager)
    component.adapts(IResourceContainerFactory)
    propertyName = 'types'

    def __init__(self, context):
        if context == None:
            raise ValueError("Can't be None")
        self.context = context
        return

    def setProperty(self, name, stringValue):
        if self.propertyName != name:
            return
        resourceFactory = self.context
        if not stringValue:
            resourceFactory.types = []
            return
        if resourceFactory.types == None:
            resourceFactory.types = []
        types = []
        for typeName in stringValue.split():
            if component.queryUtility(IResourceType, typeName) == None:
                raise ConfigurationError("Can't find resource type '%s'" % typeName)
            if typeName not in types:
                types.append(typeName)

        resourceFactory.types = types
        return