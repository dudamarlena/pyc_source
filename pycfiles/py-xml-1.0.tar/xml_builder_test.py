# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\MyWork\python\pinae\py-xml\py_xml_test\xml_builder_test.py
# Compiled at: 2016-02-11 23:13:05
import unittest
from py_xml import xml_parser
from py_xml import xml_builder

class XmlBuilderTest(unittest.TestCase):

    def test_to_xml(self):
        parser = xml_parser.XmlParser()
        result = parser.parse('test.xml')
        builder = xml_builder.XmlBuilder()
        print builder.to_xml(result)