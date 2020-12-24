# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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