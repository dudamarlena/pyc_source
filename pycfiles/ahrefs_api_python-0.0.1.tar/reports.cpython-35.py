# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ahqapiclient/resources/reports.py
# Compiled at: 2017-10-20 08:22:58
# Size of source mod 2**32: 593 bytes
from ahqapiclient.resources import Resource
from six import text_type

class Reports(Resource):

    def __init__(self, http_client):
        super(Reports, self).__init__('/reports', http_client)

    def create_report(self, report_type, value=None, s3_data=None):
        data = {}
        if value:
            if not isinstance(value, text_type):
                value = value.encode('utf-8')
            data['value'] = value
        if s3_data:
            data['s3_data'] = s3_data
        return self.post(path=self.rurl(report_type), data=data)