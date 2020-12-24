# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_getservicedefinition.py
# Compiled at: 2015-12-15 14:09:47
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.getservicedefinition import GetServiceDefinition

class TestGetServiceDefinition(TestBase):

    def test_getservicedefinition(self):
        method = GetServiceDefinition(['platform', 'shell', 'topology',
         'xml-over-http-methods', 'meaningful-use'])
        method.execute(self.connection)
        self.assertIsNotNone(method.response)
        self.assertIsNotNone(method.response.service_definition.platform)
        self.assertIsNotNone(method.response.service_definition.shell)
        self.assertNotEqual(len(method.response.service_definition.xml_method), 0)
        self.assertNotEqual(len(method.response.service_definition.common_schema), 0)
        self.assertNotEqual(len(method.response.service_definition.instances), 0)
        self.assertIsNotNone(method.response.service_definition.meaningful_use)
        self.assertIsNotNone(method.response.service_definition.updated_date)