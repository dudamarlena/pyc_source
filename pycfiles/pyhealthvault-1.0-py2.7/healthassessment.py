# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/healthassessment.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class HealthAssessment(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(HealthAssessment, self).__init__()
        self.type_id = '58fd8ac4-6c47-41a3-94b2-478401f0e26c'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'HealthAssessment'

    def parse_thing(self):
        super(HealthAssessment, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(HealthAssessment, self).write_xml()
        data_xml = etree.Element('data-xml')
        healthassessment = etree.Element('healthassessment')
        data_xml.append(healthassessment)
        thing.append(data_xml)
        return thing