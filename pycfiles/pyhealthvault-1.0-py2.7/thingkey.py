# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/thingkey.py
# Compiled at: 2015-12-15 14:23:55
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils

class ThingKey:

    def __init__(self, key_xml=None):
        self.thing_id = None
        self.version_stamp = None
        if key_xml is not None:
            self.parse_xml(key_xml)
        return

    def parse_xml(self, key_xml):
        xmlutils = XmlUtils(key_xml)
        self.thing_id = xmlutils.get_string_by_xpath('text()')
        self.version_stamp = xmlutils.get_string_by_xpath('@version-stamp')

    def write_xml(self):
        thingid = etree.Element('thing-id')
        thingid.text = self.thing_id
        thingid.set('version-stamp', self.version_stamp)
        return thingid