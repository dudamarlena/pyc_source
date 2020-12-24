# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/weightgoal.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class WeightGoal(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(WeightGoal, self).__init__()
        self.type_id = 'b7925180-d69e-48fa-ae1d-cb3748ca170e'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'WeightGoal'

    def parse_thing(self):
        super(WeightGoal, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(WeightGoal, self).write_xml()
        data_xml = etree.Element('data-xml')
        weightgoal = etree.Element('weightgoal')
        data_xml.append(weightgoal)
        thing.append(data_xml)
        return thing