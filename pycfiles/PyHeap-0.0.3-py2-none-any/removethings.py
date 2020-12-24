# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/removethings.py
# Compiled at: 2015-12-30 12:53:58
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.objects.thingkey import ThingKey
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase

class RemoveThingsRequest(RequestBase):

    def __init__(self, keys):
        super(RemoveThingsRequest, self).__init__()
        self.name = 'RemoveThings'
        self.version = 1
        self.keys = keys

    def get_info(self):
        info = etree.Element('info')
        for key in self.keys:
            info.append(key.write_xml())

        return info


class RemoveThingsResponse(ResponseBase):

    def __init__(self):
        super(RemoveThingsResponse, self).__init__()
        self.thing_keys = []
        self.name = 'RemoveThings'
        self.version = 1
        self.NSMAP = {'wc': 'urn:com.microsoft.wc.methods.response.any'}

    def parse_response(self, response):
        return


class RemoveThings(Method):

    def __init__(self, items):
        self.request = RemoveThingsRequest(items)
        self.response = RemoveThingsResponse()