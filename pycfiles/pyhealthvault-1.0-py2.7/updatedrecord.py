# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/updatedrecord.py
# Compiled at: 2016-01-06 14:03:10
from healthvaultlib.utils.xmlutils import XmlUtils

class UpdatedRecord:
    """
        Attributes:
            record_id   Record id
            update_date Date in which the record was last updated
    """

    def __init__(self, xml=None):
        self.record_id = None
        self.update_date = None
        if xml is not None:
            self.parse_xml(xml)
        return

    def parse_xml(self, xml):
        xmlutils = XmlUtils(xml)
        self.record_id = xmlutils.get_string_by_xpath('record-id')
        self.update_date = xmlutils.get_datetime('update-date')