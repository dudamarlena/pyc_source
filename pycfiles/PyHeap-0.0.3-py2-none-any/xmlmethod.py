# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/xmlmethod.py
# Compiled at: 2015-12-15 14:22:50
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.objects.xmlmethodversion import XmlMethodVersion

class XmlMethod:

    def __init__(self, method_xml=None):
        self.name = None
        self.version = []
        if method_xml is not None:
            self.parse_xml(method_xml)
        return

    def parse_xml(self, method_xml):
        xmlutils = XmlUtils(method_xml)
        self.name = xmlutils.get_string_by_xpath('name/text()')
        for i in method_xml.xpath('version'):
            self.version.append(XmlMethodVersion(i))