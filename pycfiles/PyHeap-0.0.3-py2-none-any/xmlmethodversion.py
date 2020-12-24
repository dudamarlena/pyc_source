# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/xmlmethodversion.py
# Compiled at: 2015-12-15 13:46:15
from healthvaultlib.utils.xmlutils import XmlUtils

class XmlMethodVersion:

    def __init__(self, version_xml=None):
        self.number = None
        self.request_schema_url = None
        self.response_schema_url = None
        if version_xml is not None:
            self.parse_xml(version_xml)
        return

    def parse_xml(self, version_xml):
        xmlutils = XmlUtils(version_xml)
        self.number = version_xml.get('number')
        self.request_schema_url = xmlutils.get_string_by_xpath('request-schema-url/text()')
        self.response_schema_url = xmlutils.get_string_by_xpath('response-schema-url/text()')