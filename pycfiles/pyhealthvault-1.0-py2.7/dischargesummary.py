# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/dischargesummary.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class DischargeSummary(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(DischargeSummary, self).__init__()
        self.type_id = '02ef57a2-a620-425a-8e92-a301542cca54'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'DischargeSummary'

    def parse_thing(self):
        super(DischargeSummary, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(DischargeSummary, self).write_xml()
        data_xml = etree.Element('data-xml')
        dischargesummary = etree.Element('dischargesummary')
        data_xml.append(dischargesummary)
        thing.append(data_xml)
        return thing