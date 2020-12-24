# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/itemtypes/basicdemographicinformation.py
# Compiled at: 2016-01-05 13:17:04
from lxml import etree
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.objects.codedvalue import CodedValue
from healthvaultlib.itemtypes.healthrecorditem import HealthRecordItem

class BasicDemographicInformation(HealthRecordItem):

    def __init__(self, thing_xml):
        self.thing_xml = thing_xml
        self.gender = None
        self.birthyear = None
        self.country = None
        self.postcode = None
        self.parse_thing()
        return

    def parse_thing(self):
        super(BasicDemographicInformation, self).parse_thing()
        if self.thing_xml.xpath('data-xml') != []:
            xmlutils = XmlUtils(self.thing_xml)
            self.gender = xmlutils.get_string_by_xpath('data-xml/basic/gender/text()')
            self.birthyear = xmlutils.get_int_by_xpath('data-xml/basic/birthyear/text()')
            country_node = self.thing_xml.xpath('data-xml/basic/country')
            if country_node:
                self.country = CodedValue(country_node[0])
            self.postcode = xmlutils.get_string_by_xpath('data-xml/basic/postcode/text()')
        else:
            self.is_partial = True

    def write_xml(self):
        thing = super(BasicDemographicInformation, self).write_xml()
        data_xml = etree.Element('data-xml')
        basic = etree.Element('basic')
        if self.gender is not None:
            gender = etree.Element('gender')
            gender.text = self.gender
            basic.append(gender)
        if self.country is not None:
            birthyear = etree.Element('birthyear')
            birthyear = str(self.birthyear)
            basic.append(birthyear)
        if self.country is not None:
            basic.append(self.country.write_xml('country'))
        if self.postcode is not None:
            postcode = etree.Element('postcode')
            postcode.text = self.postcode
            basic.append(postcode)
        data_xml.append(basic)
        thing.append(data_xml)
        return thing