# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/zrt/zrtresourcetype.py
# Compiled at: 2009-03-16 09:58:28
"""
$Id: zrtresourcetype.py 207 2009-03-16 13:58:27Z falko $
"""
from zope import interface
from falkolab.resource.interfaces import IExtensibleResourceFactory, IResource
from z3c.zrtresource import ZRTFileResource, ZRTFileResourceFactory
from falkolab.resource.resourcetypes import FileResource, File
from zope.schema.fieldproperty import FieldProperty
from z3c.zrtresource import processor, replace
from zope.app.component.hooks import getSite

class ZRTResource(ZRTFileResource, FileResource):
    __module__ = __name__
    interface.implements(IResource)

    def GET(self):
        data = self._commands + '\n' + super(FileResource, self).GET()
        p = processor.ZRTProcessor(data, commands={'replace': replace.Replace})
        return p.process(getSite(), self.request)


class ZRTResourceFactory(ZRTFileResourceFactory):
    __module__ = __name__
    interface.implements(IExtensibleResourceFactory)
    properties = FieldProperty(IExtensibleResourceFactory['properties'])

    def __init__(self, path, checker, name):
        self.__file = File(path, name)
        self.__checker = checker
        self.__name = name
        self.properties = {}

    def __call__(self, request):
        resource = ZRTResource(self.__file, request)
        resource.__Security_checker__ = self.__checker
        resource.__name__ = self.__name
        resource._commands = self.properties and self.properties.get('zrt-commands', '') or ''
        return resource