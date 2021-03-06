# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/medicationfill.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class MedicationFill(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(MedicationFill, self).__init__()
        self.type_id = '167ecf6b-bb54-43f9-a473-507b334907e0'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'MedicationFill'

    def parse_thing(self):
        super(MedicationFill, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(MedicationFill, self).write_xml()
        data_xml = etree.Element('data-xml')
        medicationfill = etree.Element('medicationfill')
        data_xml.append(medicationfill)
        thing.append(data_xml)
        return thing