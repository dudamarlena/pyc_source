# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/getupdatedrecordsforapplication.py
# Compiled at: 2016-01-06 14:02:36
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.objects.updatedrecord import UpdatedRecord
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase

class GetUpdatedRecordsForApplicationRequest(RequestBase):
    """
        Gets a list of records for an application with things that have
        been updated since a specified date.

        Attributes:
            updated_date    Optionally provide an updated since date,
                            of type datetime.datetime
    """

    def __init__(self):
        super(GetUpdatedRecordsForApplicationRequest, self).__init__()
        self.name = 'GetUpdatedRecordsForApplication'
        self.version = 1
        self.update_date = None
        return

    def get_info(self):
        info = etree.Element('info')
        if self.update_date is not None:
            update_date = etree.Element('update-date')
            update_date.text = self.update_date.isoformat()
            info.append(update_date)
        return info


class GetUpdatedRecordsForApplicationResponse(ResponseBase):

    def __init__(self):
        super(GetUpdatedRecordsForApplicationResponse, self).__init__()
        self.name = 'GetUpdatedRecordsForApplication'
        self.version = 1
        self.updated_records = []

    def parse_response(self, response):
        self.parse_info(response)
        for i in self.info.xpath('record-id'):
            self.updated_records.append(UpdatedRecord(i))


class GetUpdatedRecordsForApplication(Method):

    def __init__(self):
        self.request = GetUpdatedRecordsForApplicationRequest()
        self.response = GetUpdatedRecordsForApplicationResponse()