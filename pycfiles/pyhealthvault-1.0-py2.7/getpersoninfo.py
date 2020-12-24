# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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