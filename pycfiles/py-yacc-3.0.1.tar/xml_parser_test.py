# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\MyWork\python\pinae\py-xml\py_xml_test\xml_parser_test.py
# Compiled at: 2016-02-11 23:13:53
from py_xml import xml_parser
import unittest

class XmlParserTest(unittest.TestCase):

    def test_parse(self):
        parser = xml_parser.XmlParser()
        result = parser.parse('test.xml')
        self.assertEqual(len(result.get('root').get('group').get('family')), 2)
        self.assertEqual(result.get('root').get('group').get('family')[0].get('_node_'), 'green')
        self.assertEqual(result.get('root').get('group').get('family')[1].get('_node_'), 'cooker')
        self.assertEqual(len(result.get('root').get('parent')[0].get('child')), 3)
        self.assertEqual(len(result.get('root').get('parent')[1].get('child')), 2)
        self.assertEqual(result.get('root').get('parent')[0].get('child')[0].get('name').get('_attr_'), 'jim')
        self.assertEqual(result.get('root').get('parent')[0].get('child')[0].get('age').get('_attr_'), '23')
        self.assertEqual(result.get('root').get('parent')[0].get('child')[0].get('address').get('_node_'), 'Shenzhen')
        self.assertEqual(result.get('root').get('parent')[0].get('child')[0].get('phone').get('_node_'), '18607578001')
        self.assertEqual(result.get('root').get('parent')[1].get('child')[1].get('name').get('_attr_'), 'tom')
        self.assertEqual(result.get('root').get('parent')[1].get('child')[1].get('age').get('_attr_'), '45')
        self.assertEqual(result.get('root').get('parent')[1].get('child')[1].get('address').get('_node_'), 'Shanghai')
        self.assertEqual(result.get('root').get('parent')[1].get('child')[1].get('phone').get('_node_'), '13391562334')