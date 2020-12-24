# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/appskin/tal/api.py
# Compiled at: 2013-09-23 02:47:06
__docformat__ = 'restructuredtext'
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.appskin.interfaces import IApplicationBase, IApplicationResources
from ztfy.appskin.tal.interfaces import IApplicationTalesAPI
from ztfy.skin.interfaces import IPresentationTarget
from zope.component import queryMultiAdapter, queryAdapter
from zope.interface import implements
from ztfy.utils.traversing import getParent, resolve

class ApplicationTalesAPI(object):
    implements(IApplicationTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def application(self):
        return getParent(self.context, IApplicationBase)

    def resources(self):
        resources = queryMultiAdapter((self.context, self.request), IApplicationResources)
        if resources is None:
            resources = queryAdapter(self.context, IApplicationResources)
        if resources is not None:
            for resource_item in resources.resources:
                if isinstance(resource_item, basestring):
                    module_name, resource_name = resource_item.rsplit('.', 1)
                    module = resolve(module_name)
                    resource = getattr(module, resource_name)
                else:
                    resource = resource_item
                resource.need()

        return

    def presentation(self):
        app = self.application()
        if app is not None:
            adapter = queryMultiAdapter((app, self.request), IPresentationTarget)
            if adapter is not None:
                interface = adapter.target_interface
                return interface(app)
        return