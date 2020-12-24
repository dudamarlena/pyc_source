# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/tal/api.py
# Compiled at: 2015-01-08 11:51:43
from z3c.json.interfaces import IJSONWriter
from zope.tales.interfaces import ITALESFunctionNamespace
from ztfy.myams.interfaces import IMyAMSApplication, IObjectData
from ztfy.myams.interfaces.configuration import IMyAMSConfiguration, IMyAMSStaticConfiguration, MYAMS_CONFIGURATION_NAME_KEY
from ztfy.myams.tal.interfaces import IMyAMSTalesAPI
from zope.component import getUtility, queryUtility
from zope.interface import implements
from zope.security.proxy import removeSecurityProxy
from ztfy.utils.request import getRequestData
from ztfy.utils.traversing import getParent

class MyAMSTalesAdapter(object):
    """myams: TALES adapter"""
    implements(IMyAMSTalesAPI, ITALESFunctionNamespace)

    def __init__(self, context):
        self.context = context

    def setEngine(self, engine):
        self.request = engine.vars['request']

    def data(self):
        data = IObjectData(self.context, None)
        if data is not None and data.object_data:
            writer = getUtility(IJSONWriter)
            return writer.write(data.object_data)
        else:
            return

    @property
    def application(self):
        return getParent(self.context, IMyAMSApplication)

    def configuration(self):
        application = self.application
        if application is not None:
            return IMyAMSConfiguration(application, None)
        else:
            return

    def static_configuration(self):
        configuration_name = getRequestData(MYAMS_CONFIGURATION_NAME_KEY, self.request)
        if configuration_name:
            configuration = queryUtility(IMyAMSStaticConfiguration, name=configuration_name)
            if configuration is not None:
                return configuration
        configuration = self.configuration()
        if configuration is not None:
            return configuration.static_configuration
        else:
            return

    def resources(self):
        application = getParent(self.context, IMyAMSApplication)
        if application is not None:
            for resource in application.resources:
                removeSecurityProxy(resource).need()

        return