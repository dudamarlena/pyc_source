# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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