# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\util\tests\test_xml.py
# Compiled at: 2010-12-23 17:42:44
import unittest, codecs
from seishub.core.util.xml import parseXMLDeclaration, toUnicode, applyMacros
TEST_BASE = '<seishub xml:base="http://localhost:8080" xmlns:xlink="http://www.w3.org/1999/xlink">\n    <mapping xlink:type="simple" xlink:href="/seishub/schema/browser">browser</mapping>\n    <resource xlink:type="simple" xlink:href="/seishub/schema/3">/seishub/schema/3</resource>\n    <resource xlink:type="simple" xlink:href="/seishub/schema/4">/seishub/schema/4</resource>\n</seishub>'
TEST_W_ENC = '<?xml version="1.0" encoding="%s"?>' + TEST_BASE
TEST_WO_ENC = '<?xml version="1.0" ?>' + TEST_BASE

class XMLUtilTest(unittest.TestCase):
    """Test case for various XML helper tools."""

    def test_parseXMLDeclaration_unicode(self):
        """Tests parsing the XML declaration of an unicode object."""
        data, enc = parseXMLDeclaration(unicode(TEST_W_ENC % 'UTF-8'), True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(unicode(TEST_WO_ENC), True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(unicode(TEST_W_ENC % 'UTF-8'), False)
        assert data == TEST_W_ENC % 'UTF-8'
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(unicode(TEST_WO_ENC), False)
        assert data == TEST_WO_ENC
        assert enc == 'utf-8'

    def test_parseXMLDeclaration_str(self):
        """Tests parsing the XML declaration of a str object."""
        data, enc = parseXMLDeclaration(TEST_W_ENC % 'UTF-8', True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(TEST_WO_ENC, True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(TEST_W_ENC % 'UTF-8', False)
        assert data == TEST_W_ENC % 'UTF-8'
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(TEST_WO_ENC, False)
        assert data == TEST_WO_ENC
        assert enc == 'utf-8'

    def test_toUnicode_utf8(self):
        """Tests converting and parsing an utf-8 encoded string."""
        temp = codecs.BOM_UTF8 + unicode(TEST_W_ENC % 'UTF-8').encode('UTF-8')
        data, enc = toUnicode(temp, True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = toUnicode(temp, False)
        assert data == TEST_W_ENC % 'UTF-8'
        assert enc == 'utf-8'
        temp = codecs.BOM_UTF8 + unicode(TEST_WO_ENC).encode('UTF-8')
        data, enc = toUnicode(temp, True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = toUnicode(temp, False)
        assert data == TEST_WO_ENC
        assert enc == 'utf-8'
        temp = unicode(TEST_W_ENC % 'UTF-8').encode('UTF-8')
        data, enc = parseXMLDeclaration(temp, True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(temp, False)
        assert data == TEST_W_ENC % 'UTF-8'
        assert enc == 'utf-8'
        temp = unicode(TEST_WO_ENC).encode('UTF-8')
        data, enc = parseXMLDeclaration(temp, True)
        assert data == TEST_BASE
        assert enc == 'utf-8'
        data, enc = parseXMLDeclaration(temp, False)
        assert data == TEST_WO_ENC
        assert enc == 'utf-8'

    def test_toUnicode_UTF16(self):
        """Tests converting and parsing an utf-16 encoded string."""
        temp = codecs.BOM_UTF16_LE + unicode(TEST_W_ENC % 'UTF-16').encode('UTF-16le')
        data, enc = toUnicode(temp, True)
        assert enc == 'utf-16le'
        assert data == TEST_BASE
        data, enc = toUnicode(temp, False)
        assert enc == 'utf-16le'
        assert data == TEST_W_ENC % 'UTF-16'
        temp = codecs.BOM_UTF16_BE + unicode(TEST_W_ENC % 'UTF-16').encode('UTF-16be')
        data, enc = toUnicode(temp, True)
        assert enc == 'utf-16be'
        assert data == TEST_BASE
        data, enc = toUnicode(temp, False)
        assert enc == 'utf-16be'
        assert data == TEST_W_ENC % 'UTF-16'
        temp = unicode(TEST_W_ENC % 'UTF-16').encode('UTF-16le')
        data, enc = toUnicode(temp, True)
        assert enc == 'utf-8'

    def test_applyMacros(self):
        res = applyMacros('{test=world, blub=!} hello {test}{blub}')
        self.assertEquals(res, 'hello world!')
        res = applyMacros('{\n test = world ,   blub\n=!} hello\n{test}{blub}')
        self.assertEquals(res, 'hello world!')
        res = applyMacros('{test=/muh/blub/nn, blub=!} hello {test}{blub}')
        self.assertEquals(res, 'hello /muh/blub/nn!')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XMLUtilTest, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')