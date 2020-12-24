# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/bloodglucose.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class BloodGlucose(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(BloodGlucose, self).__init__()
        self.type_id = '879e7c04-4e8a-4707-9ad3-b054df467ce4'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'BloodGlucose'

    def parse_thing(self):
        super(BloodGlucose, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(BloodGlucose, self).write_xml()
        data_xml = etree.Element('data-xml')
        bloodglucose = etree.Element('bloodglucose')
        data_xml.append(bloodglucose)
        thing.append(data_xml)
        return thing