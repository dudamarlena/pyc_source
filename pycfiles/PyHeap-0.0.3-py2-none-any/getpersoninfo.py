# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/getpersoninfo.py
# Compiled at: 2016-01-03 06:00:52
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.objects.personinfo import PersonInfo
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase

class GetPersonInfoRequest(RequestBase):

    def __init__(self):
        super(GetPersonInfoRequest, self).__init__()
        self.name = 'GetPersonInfo'
        self.version = 1

    def get_info(self):
        info = etree.Element('info')
        return info


class GetPersonInfoResponse(ResponseBase):

    def __init__(self):
        super(GetPersonInfoResponse, self).__init__()
        self.personinfo = None
        self.name = 'GetPersonInfo'
        self.version = 1
        return

    def parse_response(self, response):
        self.parse_info(response)
        self.personinfo = PersonInfo(self.info.xpath('person-info')[0])


class GetPersonInfo(Method):

    def __init__(self):
        self.request = GetPersonInfoRequest()
        self.response = GetPersonInfoResponse()