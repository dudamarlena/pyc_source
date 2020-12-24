# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/instance.py
# Compiled at: 2015-12-15 14:29:24
from healthvaultlib.utils.xmlutils import XmlUtils

class Instance:

    def __init__(self, instance_xml=None):
        self.id = None
        self.name = None
        self.description = None
        self.platform_url = None
        self.shell_url = None
        if instance_xml is not None:
            self.parse_xml(instance_xml)
        return

    def parse_xml(self, instance_xml):
        xmlutils = XmlUtils(instance_xml)
        self.id = xmlutils.get_string_by_xpath('id/text()')
        self.name = xmlutils.get_string_by_xpath('name/text()')
        self.description = xmlutils.get_string_by_xpath('description/text()')
        self.platform_url = xmlutils.get_string_by_xpath('platform-url/text()')
        self.shell_url = xmlutils.get_string_by_xpath('shell-url/text()')