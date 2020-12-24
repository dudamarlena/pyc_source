# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ubcpi/test/test_serialize.py
# Compiled at: 2015-08-31 13:52:46
from lxml import etree
import unittest
from ddt import ddt, file_data
from ubcpi.serialize import parse_image_xml, parse_question_xml, parse_options_xml, ValidationError, parse_seeds_xml, parse_from_xml, UpdateFromXmlError

@ddt
class TestSerialize(unittest.TestCase):

    @file_data('data/parse_image_xml.json')
    def test_parse_image_xml(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        result = parse_image_xml(xml)
        self.assertEqual(result, data['expect'])

    @file_data('data/parse_question_xml.json')
    def test_parse_question_xml(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        result = parse_question_xml(xml)
        self.assertEqual(result, data['expect'])

    @file_data('data/parse_question_xml_errors.json')
    def test_parse_question_xml_errors(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        with self.assertRaises(ValidationError):
            parse_question_xml(xml)

    @file_data('data/parse_options_xml.json')
    def test_parse_options_xml(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        result = parse_options_xml(xml)
        self.assertEqual(result, (
         data['expect']['options'], data['expect']['correct'], data['expect']['rationale']))

    @file_data('data/parse_options_xml_errors.json')
    def test_parse_options_xml_errors(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        with self.assertRaises(ValidationError):
            parse_options_xml(xml)

    @file_data('data/parse_seeds_xml.json')
    def test_parse_seeds_xml(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        result = parse_seeds_xml(xml)
        self.assertEqual(result, data['expect'])

    @file_data('data/parse_seeds_xml_errors.json')
    def test_parse_seeds_xml_errors(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        with self.assertRaises(ValidationError):
            parse_seeds_xml(xml)

    @file_data('data/parse_from_xml.json')
    def test_parse_from_xml(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        result = parse_from_xml(xml)
        self.assertEqual(result, data['expect'])

    @file_data('data/parse_from_xml_errors.json')
    def test_parse_from_xml_errors(self, data):
        xml = etree.fromstring(('').join(data['xml']))
        with self.assertRaises(UpdateFromXmlError):
            parse_from_xml(xml)