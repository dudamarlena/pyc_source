# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/groupmembershipactivity.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class GroupMembershipActivity(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(GroupMembershipActivity, self).__init__()
        self.type_id = 'e75fa095-31ed-4b30-b5f7-463963b5e734'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'GroupMembershipActivity'

    def parse_thing(self):
        super(GroupMembershipActivity, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(GroupMembershipActivity, self).write_xml()
        data_xml = etree.Element('data-xml')
        groupmembershipactivity = etree.Element('groupmembershipactivity')
        data_xml.append(groupmembershipactivity)
        thing.append(data_xml)
        return thing