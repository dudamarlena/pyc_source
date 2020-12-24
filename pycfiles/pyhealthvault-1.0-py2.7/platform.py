# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/platform.py
# Compiled at: 2015-12-15 13:20:52
from healthvaultlib.utils.xmlutils import XmlUtils

class Platform:

    def __init__(self, platform_xml=None):
        self.url = None
        self.version = None
        self.configuration = {}
        if platform_xml is not None:
            self.parse_xml(platform_xml)
        return

    def parse_xml(self, platform_xml):
        xmlutils = XmlUtils(platform_xml)
        self.url = xmlutils.get_string_by_xpath('url/text()')
        self.version = xmlutils.get_string_by_xpath('version/text()')
        for i in platform_xml.xpath('configuration'):
            self.configuration[i.get('key')] = i.xpath('text()')[0]