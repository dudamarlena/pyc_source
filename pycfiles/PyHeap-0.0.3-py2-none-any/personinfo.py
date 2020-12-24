# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/personinfo.py
# Compiled at: 2015-12-19 03:54:48
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.objects.record import Record

class PersonInfo:

    def __init__(self, info_element=None):
        self.personid = None
        self.name = None
        self.selected_record_id = None
        self.records = []
        if info_element is not None:
            self.parse_xml(info_element)
        return

    def parse_xml(self, info_element):
        xmlutils = XmlUtils(info_element)
        self.personid = xmlutils.get_string_by_xpath('person-id/text()')
        self.name = xmlutils.get_string_by_xpath('name/text()')
        self.selected_record_id = xmlutils.get_string_by_xpath('selected-record-id/text()')
        records = info_element.xpath('record')
        for i in records:
            self.records.append(Record(i))