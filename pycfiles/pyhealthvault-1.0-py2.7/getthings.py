# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/getthings.py
# Compiled at: 2015-11-17 12:40:40
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase
from healthvaultlib.objects.thinggroupresponse import ThingGroupResponse

class GetThingsRequest(RequestBase):

    def __init__(self, groups):
        super(GetThingsRequest, self).__init__()
        self.name = 'GetThings'
        self.version = 3
        self.groups = groups

    def get_info(self):
        info = etree.Element('info')
        for group in self.groups:
            info.append(group.write_xml())

        return info


class GetThingsResponse(ResponseBase):

    def __init__(self):
        super(GetThingsResponse, self).__init__()
        self.groups = []
        self.name = 'GetThings'
        self.version = 3

    def parse_response(self, response):
        self.parse_info(response)
        for group in self.info.xpath('group'):
            self.groups.append(ThingGroupResponse(group))


class GetThings(Method):

    def __init__(self, groups):
        self.request = GetThingsRequest(groups)
        self.response = GetThingsResponse()