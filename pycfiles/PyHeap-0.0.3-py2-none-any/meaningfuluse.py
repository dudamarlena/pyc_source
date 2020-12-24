# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/meaningfuluse.py
# Compiled at: 2015-12-15 13:36:36
from healthvaultlib.utils.xmlutils import XmlUtils

class MeaningfulUse:

    def __init__(self, meaningful_use_xml=None):
        self.enabled = None
        self.configuration = {}
        if meaningful_use_xml is not None:
            self.parse_xml(meaningful_use_xml)
        return

    def parse_xml(self, meaningful_use_xml):
        xmlutils = XmlUtils(meaningful_use_xml)
        self.enabled = xmlutils.get_bool_by_xpath('enabled/text()')
        for i in meaningful_use_xml.xpath('configuration'):
            self.configuration[i.get('key')] = i.xpath('text()')[0]