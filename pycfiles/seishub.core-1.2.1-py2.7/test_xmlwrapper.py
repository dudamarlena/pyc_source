# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\util\tests\test_xmlwrapper.py
# Compiled at: 2010-12-23 17:42:44
from seishub.core.exceptions import InvalidObjectError
from seishub.core.util.xmlwrapper import XmlSchema, XmlTreeDoc, InvalidXPathExpression
import unittest
TEST_SCHEMA = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n<xsd:element name="a" type="AType"/>\n<xsd:complexType name="AType">\n    <xsd:sequence>\n        <xsd:element name="b" maxOccurs="2" type="xsd:string" />\n    </xsd:sequence>\n</xsd:complexType>\n</xsd:schema>'
GOOD_XML = '<a><b>A string</b>\n<b>Another string</b>\n</a>'
BAD_XML = '<a><b><an_element></an_element></b></a>'

class XmlSchemaTest(unittest.TestCase):

    def setUp(self):
        self.test_schema = TEST_SCHEMA
        self.good_xml = GOOD_XML
        self.bad_xml = BAD_XML

    def testValidate(self):
        validDoc = XmlTreeDoc(self.good_xml)
        invalidDoc = XmlTreeDoc(self.bad_xml)
        schema = XmlSchema(self.test_schema)
        schema.validate(validDoc)
        self.assertRaises(InvalidObjectError, schema.validate, invalidDoc)


class XmlTreeTest(unittest.TestCase):

    def testEvalXPath(self):
        tree_doc = XmlTreeDoc(xml_data=GOOD_XML)
        self.assertRaises(InvalidXPathExpression, tree_doc.evalXPath, '//')
        self.assertEquals(tree_doc.evalXPath('/a/b')[1].getStrContent(), 'Another string')
        self.assertEquals(tree_doc.evalXPath('/a')[0].getStrContent(), '<a><b>A string</b>\n<b>Another string</b>\n</a>')
        ns_doc = XmlTreeDoc(xml_data=TEST_SCHEMA)
        self.assertEquals(ns_doc.evalXPath('/xsd:schema/xsd:element/@name')[0].getStrContent(), 'a')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XmlSchemaTest, 'test'))
    suite.addTest(unittest.makeSuite(XmlTreeTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')