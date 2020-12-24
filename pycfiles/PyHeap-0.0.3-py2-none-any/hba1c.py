# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/hba1c.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class Hba1c(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(Hba1c, self).__init__()
        self.type_id = '62160199-b80f-4905-a55a-ac4ba825ceae'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'Hba1c'

    def parse_thing(self):
        super(Hba1c, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(Hba1c, self).write_xml()
        data_xml = etree.Element('data-xml')
        hba1c = etree.Element('hba1c')
        data_xml.append(hba1c)
        thing.append(data_xml)
        return thing