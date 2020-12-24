# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/newapplicationcreationinfo.py
# Compiled at: 2016-01-12 13:40:28
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase

class NewApplicationCreationInfoRequest(RequestBase):

    def __init__(self):
        super(NewApplicationCreationInfoRequest, self).__init__()
        self.name = 'NewApplicationCreationInfo'
        self.version = 1

    def get_info(self):
        info = etree.Element('info')
        return info


class NewApplicationCreationInfoResponse(ResponseBase):

    def __init__(self):
        super(NewApplicationCreationInfoResponse, self).__init__()
        self.name = 'NewApplicationCreationInfo'
        self.version = 1
        self.app_id = None
        self.shared_secret = None
        self.app_token = None
        return

    def parse_response(self, response):
        self.parse_info(response)
        xmlutils = XmlUtils(self.info)
        self.app_id = xmlutils.get_string_by_xpath('app-id/text()')
        self.shared_secret = xmlutils.get_string_by_xpath('shared-secret/text()')
        self.app_token = xmlutils.get_string_by_xpath('app-token/text()')


class NewApplicationCreationInfo(Method):

    def __init__(self):
        self.request = NewApplicationCreationInfoRequest()
        self.response = NewApplicationCreationInfoResponse()