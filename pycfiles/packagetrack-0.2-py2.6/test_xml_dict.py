# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/packagetrack/tests/test_xml_dict.py
# Compiled at: 2010-06-16 06:04:37
from unittest import TestCase
from packagetrack import xml_dict
test_xml = '<?xml version="1.0"?>\n<foo>\n  <bar>\n    <baz>what</baz>\n    <quux>hello</quux>\n  </bar>\n  <sup>yeah</sup>\n  <goodbye>no</goodbye>\n</foo>'
test_dict = {'foo': {'bar': {'baz': 'what', 'quux': 'hello'}, 
           'sup': 'yeah', 
           'goodbye': 'no'}}

class TestXMLDict(TestCase):

    def test_xml_to_dict(self):
        assert xml_dict.xml_to_dict(test_xml) == test_dict

    def test_roundtrip(self):
        assert xml_dict.xml_to_dict(xml_dict.dict_to_xml(test_dict)) == test_dict

    def test_attribute(self):
        xml = xml_dict.dict_to_xml(test_dict, {'xml:lang': 'en-US'})
        assert '<foo xml:lang="en-US">' in xml