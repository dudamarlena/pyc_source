# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/groupmembership.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class GroupMembership(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(GroupMembership, self).__init__()
        self.type_id = '66ac44c7-1d60-4e95-bb5b-d21490e91057'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'GroupMembership'

    def parse_thing(self):
        super(GroupMembership, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(GroupMembership, self).write_xml()
        data_xml = etree.Element('data-xml')
        groupmembership = etree.Element('groupmembership')
        data_xml.append(groupmembership)
        thing.append(data_xml)
        return thing