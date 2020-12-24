# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/method_inspector.py
# Compiled at: 2015-12-19 03:25:20
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase

class InspectorRequest(RequestBase):

    def __init__(self, parameters):
        super(InspectorRequest, self).__init__()
        self.name = 'GetAuthorizedPeople'
        self.version = 1
        self.parameters = parameters

    def get_info(self):
        info = etree.Element('info')
        info.append(self.parameters.get_info())
        return info


class InspectorResponse(ResponseBase):

    def __init__(self):
        super(InspectorResponse, self).__init__()
        self.name = 'GetAuthorizedPeople'
        self.version = 1

    def parse_response(self, response):
        self.parse_info(response)


class Inspector(Method):

    def __init__(self, parameters):
        self.request = InspectorRequest(parameters)
        self.response = InspectorResponse()