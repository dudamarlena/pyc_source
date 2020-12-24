# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/servicedefinition.py
# Compiled at: 2015-12-15 14:26:13
from healthvaultlib.objects.shell import Shell
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.objects.instance import Instance
from healthvaultlib.objects.platform import Platform
from healthvaultlib.objects.xmlmethod import XmlMethod
from healthvaultlib.objects.meaningfuluse import MeaningfulUse

class ServiceDefinition:

    def __init__(self, definition_xml=None):
        self.platform = None
        self.shell = None
        self.xml_method = []
        self.common_schema = []
        self.instances = []
        self.meaningful_use = None
        self.updated_date = None
        if definition_xml is not None:
            self.parse_xml(definition_xml)
        return

    def parse_xml(self, definition_xml):
        xmlutils = XmlUtils(definition_xml)
        platform = definition_xml.xpath('platform')
        if platform != []:
            self.platform = Platform(platform[0])
        shell = definition_xml.xpath('shell')
        if shell != []:
            self.shell = Shell(shell[0])
        xml_method = definition_xml.xpath('xml-method')
        for i in xml_method:
            self.xml_method.append(XmlMethod(i))

        common_schema = definition_xml.xpath('common-schema')
        for i in common_schema:
            self.common_schema.append(i.xpath('text()')[0])

        instance_list = definition_xml.xpath('instances')
        for i in instance_list:
            self.instances.append(Instance(i))

        meaningful_use = definition_xml.xpath('meaningful-use')
        if meaningful_use != []:
            self.meaningful_use = MeaningfulUse(meaningful_use[0])
        self.updated_date = xmlutils.get_datetime_by_xpath('updated-date/text()')