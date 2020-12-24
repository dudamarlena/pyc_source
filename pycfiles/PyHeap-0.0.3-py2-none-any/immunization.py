# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/immunization.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class Immunization(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(Immunization, self).__init__()
        self.type_id = 'cd3587b5-b6e1-4565-ab3b-1c3ad45eb04f'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'Immunization'

    def parse_thing(self):
        super(Immunization, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(Immunization, self).write_xml()
        data_xml = etree.Element('data-xml')
        immunization = etree.Element('immunization')
        data_xml.append(immunization)
        thing.append(data_xml)
        return thing