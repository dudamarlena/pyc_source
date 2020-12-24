# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/applicationdatareference.py
# Compiled at: 2015-11-16 13:57:41
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class ApplicationDataReference(HealthRecordItem):

    def __init__(self, thing_xml=None):
        super(ApplicationDataReference, self).__init__()
        self.type_id = '9ad2a94f-c6a4-4d78-8b50-75b65be0e250'
        if thing_xml is not None:
            self.thing_xml = thing_xml
            self.parse_thing()
        return

    def __str__(self):
        return 'ApplicationDataReference'

    def parse_thing(self):
        super(ApplicationDataReference, self).parse_thing()
        xmlutils = XmlUtils(self.thing_xml)

    def write_xml(self):
        thing = super(ApplicationDataReference, self).write_xml()
        data_xml = etree.Element('data-xml')
        applicationdatareference = etree.Element('applicationdatareference')
        data_xml.append(applicationdatareference)
        thing.append(data_xml)
        return thing