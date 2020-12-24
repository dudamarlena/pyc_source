# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/package/resourcepackage.py
# Compiled at: 2009-03-11 04:29:09
"""
$Id: resourcepackage.py 200 2009-03-11 08:29:13Z falko $
"""
from zope import interface, component
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.publisher.browser.resource import Resource
from zope.app.publisher.browser.resources import empty
from zope.publisher.interfaces import NotFound
from zope.interface.verify import verifyObject
from falkolab.resource.interfaces import IResource, IExtensibleResourceFactory
from zope.schema.fieldproperty import FieldProperty

class Package(object):
    __module__ = __name__
    resources = []

    def __init__(self, include, name):
        self.resources = list(include)
        self.__name__ = name


_marker = object()

class PackageResource(BrowserView, Resource):
    __module__ = __name__
    interface.implements(IBrowserPublisher, IResource)

    def publishTraverse(self, request, name):
        """See interface IBrowserPublisher"""
        return self.get(name)

    def browserDefault(self, request):
        """See interface IBrowserPublisher"""
        return (
         empty, ())

    def __getitem__(self, name):
        res = self.get(name, None)
        if res is None:
            raise KeyError(name)
        return res

    def get(self, name, default=_marker):
        resources = self.context.resources
        if name not in resources:
            if default is _marker:
                raise NotFound(None, name)
            return default
        resource = component.getAdapter(self.request, interface.Interface, name=name)
        if resource is None:
            raise NotFound(None, name)
        return resource

    def renderHtmlEmbeding(self, request, **kwargs):
        exceptions = kwargs.get('exceptions', [])
        resources = self.context.resources
        html = ''
        for resName in resources:
            if resName in exceptions:
                continue
            resource = component.getAdapter(self.request, interface.Interface, name=resName)
            if resource is None:
                raise NotFound(None, resName)
            try:
                verifyObject(IResource, resource)
            except:
                raise TypeError("Resource '%s' must implement falkolab.resource.interfaces.IResource for html embeding" % resName)

            html += resource.renderHtmlEmbeding(self.request, exceptions=exceptions)
            exceptions.append(resName)
            if not html.endswith('\n'):
                html += '\n'

        return html


class ResourcePackageFactory(object):
    __module__ = __name__
    interface.implements(IExtensibleResourceFactory)
    properties = FieldProperty(IExtensibleResourceFactory['properties'])

    def __init__(self, include, checker, name):
        super(ResourcePackageFactory, self).__init__()
        self.__pkg = Package(include, name)
        self.__checker = checker
        self.__name = name
        self.properties = {}

    def __call__(self, request):
        resource = PackageResource(self.__pkg, request)
        resource.__Security_checker__ = self.__checker
        resource.__name__ = self.__name
        return resource