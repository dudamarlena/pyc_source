# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/bodydimension.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class BodyDimension(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(BodyDimension, self).__init__()
        self.type_id = 'dd710b31-2b6f-45bd-9552-253562b9a7c1'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'BodyDimension'

    def parse_thing(self):
        super(BodyDimension, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(BodyDimension, self).write_xml()
        data_xml = etree.Element('data-xml')
        bodydimension = etree.Element('bodydimension')
        data_xml.append(bodydimension)
        thing.append(data_xml)
        return thing