# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/contraindication.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class Contraindication(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(Contraindication, self).__init__()
        self.type_id = '046d0ad7-6d7f-4bfd-afd4-4192ca2e913d'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'Contraindication'

    def parse_thing(self):
        super(Contraindication, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(Contraindication, self).write_xml()
        data_xml = etree.Element('data-xml')
        contraindication = etree.Element('contraindication')
        data_xml.append(contraindication)
        thing.append(data_xml)
        return thing