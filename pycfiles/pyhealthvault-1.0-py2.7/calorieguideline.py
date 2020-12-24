# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/calorieguideline.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class CalorieGuideline(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(CalorieGuideline, self).__init__()
        self.type_id = 'd3170d30-a41b-4bde-a116-87698c8a001a'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'CalorieGuideline'

    def parse_thing(self):
        super(CalorieGuideline, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(CalorieGuideline, self).write_xml()
        data_xml = etree.Element('data-xml')
        calorieguideline = etree.Element('calorieguideline')
        data_xml.append(calorieguideline)
        thing.append(data_xml)
        return thing