# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/record.py
# Compiled at: 2016-01-06 13:07:14
from healthvaultlib.utils.xmlutils import XmlUtils

class Record:

    def __init__(self, record_xml=None):
        self.id = None
        self.record_custodian = False
        self.rel_type = None
        self.rel_name = None
        self.auth_expires = None
        self.auth_expired = False
        self.display_name = None
        self.date_created = None
        if record_xml is not None:
            self.parse_xml(record_xml)
        return

    def parse_xml(self, record_xml):
        xmlhelper = XmlUtils(record_xml)
        self.id = xmlhelper.get_string('id')
        self.record_custodian = xmlhelper.get_bool('record-custodian')
        self.rel_type = xmlhelper.get_int('rel-type')
        self.rel_name = xmlhelper.get_string('rel-name')
        self.auth_expires = xmlhelper.get_datetime('auth-expires')
        self.auth_expired = xmlhelper.get_bool('auth-expired')
        self.display_name = xmlhelper.get_string('display-name')
        self.date_created = xmlhelper.get_datetime('date-created')